# import wave
import argparse
import sys
import time
import logging
import grpc
import os
from importlib.machinery import SourceFileLoader
import threading
from google.protobuf import text_format

import nuance_tts_pb2
import nuance_tts_pb2_grpc

thread_context = threading.local()
total_first_chunk_latency = 0
total_synthesis = 0

args = None


def send_get_voices_request(grpc_client, request):
    log.info("Sending GetVoices request")

    client_span = None
    get_voices_span = None
    metadata = []

    if args.jaeger:
        log.debug("Injecting Jaeger span context into request")
        client_span = tracer.start_span("Client.gRPC")
        get_voices_span = tracer.start_span(
            "Client.GetVoices", child_of=client_span)
        carrier = dict()
        tracer.inject(get_voices_span.context,
                      opentracing.propagation.Format.TEXT_MAP, carrier)
        metadata.append(('uber-trace-id', carrier['uber-trace-id']))

    response = grpc_client.GetVoices(request=request, metadata=metadata)

    for voice in response.voices:
        log.info("Voice: %s %s %s" % (voice.name, voice.model, voice.language))
    
    if get_voices_span:
        get_voices_span.finish()
    if client_span:
        client_span.finish()

def send_synthesis_request(grpc_client, request, metadata=None):
    log.info("Sending Synthesis request")

    audio_file = None
    audio_file_name = ""
    extension = ""
    num_chunks = 0
    metadata = []
    client_span = None
    synthesis_span = None
    received_first_audio_chunk = False
    call_credentials = None

    global total_synthesis
    total_synthesis = total_synthesis + 1

    global args

    thread_context.num_synthesis = thread_context.num_synthesis + 1

    if args.saveAudio or args.saveAudioChunks:
        if request.audio_params.audio_format.HasField("pcm"):
            extension = "pcm"
        elif request.audio_params.audio_format.HasField("alaw"):
            extension = "alaw"
        elif request.audio_params.audio_format.HasField("ulaw"):
            extension = "ulaw"
        else:
            extension = "ogg"

        if args.saveAudio:
            audio_file_name = "%s_i%d_s%d.%s" % (
                thread_context.file, num_iterations, thread_context.num_synthesis, extension)
            audio_file = open(audio_file_name, "wb")

    if args.nmaid:
        metadata.append(('x-nuance-client-id', args.nmaid))

    if args.jaeger:
        log.debug("Injecting Jaeger span context into request")
        client_span = tracer.start_span("Client.gRPC")
        synthesis_span = tracer.start_span(
            "Client.Synthesize", child_of=client_span)
        carrier = dict()
        tracer.inject(synthesis_span.context,
                      opentracing.propagation.Format.TEXT_MAP, carrier)
        metadata.append(('uber-trace-id', carrier['uber-trace-id']))

    start = time.monotonic()

    responses = grpc_client.Synthesize(
        request=request, metadata=metadata)

    for response in responses:
        if response.HasField("audio"):
            log.info("Received audio: %d bytes" % len(response.audio))
            if not received_first_audio_chunk:
                received_first_audio_chunk = True
                latency = time.monotonic() - start
                log.info("First chunk latency: {} seconds".format(latency))
                global total_first_chunk_latency
                total_first_chunk_latency = total_first_chunk_latency + latency
                log.info("Average first-chunk latency (over {} synthesis requests): {} seconds".format(
                    total_synthesis, total_first_chunk_latency/(total_synthesis)))

            if args.saveAudio:
                audio_file.write(response.audio)
            if args.saveAudioChunks:
                if request.audio_params.audio_format.HasField("opus"):
                    log.warn("Cannot save separate audio chunks for Ogg Opus, ignoring")
                else:
                    num_chunks = num_chunks + 1
                    chunk_file_name = "%s_i%d_s%d_c%d.%s" % (
                        thread_context.file, num_iterations, thread_context.num_synthesis, num_chunks, extension)
                    chunk_audio_file = open(chunk_file_name, "wb")
                    chunk_audio_file.write(response.audio)
                    chunk_audio_file.close()
                    log.info("Wrote audio chunk to %s" % chunk_file_name)
        elif response.HasField("events"):
            log.info("Received events")
            log.info(text_format.MessageToString(response.events))
        else:
            if response.status.code == 200:
                log.info("Received status response: SUCCESS")
            else:
                log.error("Received status response: FAILED")
                log.error("Code: {}, Message: {}".format(response.status.code, response.status.message))
                log.error('Error: {}'.format(response.status.details))

    if args.saveAudio:
        audio_file.close()
        log.info("Wrote audio to %s" % audio_file_name)

    if synthesis_span:
        synthesis_span.finish()
    if client_span:
        client_span.finish()


def parse_args():
    global args
    parser = argparse.ArgumentParser(
        prog="tts_client.py",
        usage="%(prog)s [-options]",
        add_help=False,
        formatter_class=lambda prog: argparse.HelpFormatter(
            prog, max_help_position=45, width=100)
    )

    options = parser.add_argument_group("options")
    options.add_argument("-h", "--help", action="help",
                         help="Show this help message and exit")
    options.add_argument("--nmaid", nargs="?", help=argparse.SUPPRESS)
    options.add_argument("--token", nargs="?", help=argparse.SUPPRESS)
    options.add_argument("-f", "--files", metavar="file", nargs="+",
                         help="List of flow files to execute sequentially, default=['flow.py']", default=['flow.py'])
    options.add_argument("-p", "--parallel", action="store_true",
                         help="Run each flow in a separate thread.")
    options.add_argument("-i", "--iterations", metavar="num", nargs="?",
                         help="Number of times to run the list of files, default=1", default=1, type=int)
    options.add_argument("-s", "--serverUrl", metavar="url", nargs="?",
                         help="NVC server URL, default=localhost:8080", default='localhost:8080')
    options.add_argument("--secure", action="store_true",
                         help="Connect to the server using a secure gRPC channel.")
    options.add_argument("--rootCerts",  metavar="file", nargs="?",
                         help="Root certificates when using secure channel.")
    options.add_argument("--privateKey",  metavar="file", nargs="?",
                         help="Certificate private key when using secure channel.")
    options.add_argument("--certChain",  metavar="file", nargs="?",
                         help="Certificate chain when using secure channel.")
    options.add_argument("--saveAudio", action="store_true",
                         help="Save audio to disk")
    options.add_argument("--saveAudioChunks", action="store_true",
                         help="Save each individual audio chunk to disk")
    options.add_argument("--jaeger", metavar="addr", nargs="?", const='udp://localhost:6831',
                         help="Send UDP opentrace spans, default addr=udp://localhost:6831")

    args = parser.parse_args()


def initialize_tracing():
    if args.jaeger:
        print("Enabling Jaeger traces")
        global opentracing
        import opentracing
        import jaeger_client

        from urllib.parse import urlparse
        agent_addr = urlparse(args.jaeger)
        if not agent_addr.netloc:
            raise Exception(
                "invalid jaeger agent address: {}".format(args.jaeger))
        if not agent_addr.hostname:
            raise Exception(
                "missing hostname in jaeger agent address: {}".format(args.jaeger))
        if not agent_addr.port:
            raise Exception(
                "missing port in jaeger agent address: {}".format(args.jaeger))
        tracer_config = {
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': agent_addr.hostname,
                'reporting_port': agent_addr.port
            },
            'logging': True
        }
        config = jaeger_client.Config(
            config=tracer_config, service_name='NVCClient', validate=True)
        global tracer
        tracer = config.initialize_tracer()

def create_channel():
    call_credentials = None
    channel = None


    if args.token:
        log.debug("Adding CallCredentials with token %s" % args.token)
        call_credentials = grpc.access_token_call_credentials(args.token)
        
    if args.secure:
        log.debug("Creating secure gRPC channel")
        root_certificates = None
        certificate_chain = None
        private_key = None
        if args.rootCerts:
            log.debug("Adding root certs")
            root_certificates = open(args.rootCerts, 'rb').read()
        if args.certChain:
            log.debug("Adding cert chain")
            certificate_chain = open(args.certChain, 'rb').read()
        if args.privateKey:
            log.debug("Adding private key")
            private_key = open(args.privateKey, 'rb').read()

        channel_credentials = grpc.ssl_channel_credentials(root_certificates=root_certificates, private_key=private_key, certificate_chain=certificate_chain)
        if call_credentials is not None:
            channel_credentials = grpc.composite_channel_credentials(channel_credentials, call_credentials)
        channel = grpc.secure_channel(args.serverUrl, credentials=channel_credentials)
    else:
        log.debug("Creating insecure gRPC channel")
        channel = grpc.insecure_channel(args.serverUrl)
    
    return channel


def run_one_file(file, list_of_requests):
    with create_channel() as channel:
        grpc_client = nuance_tts_pb2_grpc.SynthesizerStub(channel=channel)
        log.info("Running file [%s]" % file)
        log.debug(list_of_requests)

        thread_context.num_synthesis = 0
        thread_context.file = os.path.basename(file)

        for request in list_of_requests:
            if isinstance(request, nuance_tts_pb2.GetVoicesRequest):
                send_get_voices_request(grpc_client, request)
            elif isinstance(request, nuance_tts_pb2.SynthesisRequest):
                send_synthesis_request(grpc_client, request)
            elif isinstance(request, (int, float)):
                log.info("Waiting for {} seconds".format(request))
                time.sleep(request)
        log.info("Done running file [%s]" % file)


def run():
    parse_args()

    log_level = logging.DEBUG
    global log
    log = logging.getLogger('')
    logging.basicConfig(
        format='%(asctime)s %(levelname)-5s: %(message)s', level=log_level)

    initialize_tracing()

    for i in range(args.iterations):
        global num_iterations
        num_iterations = i + 1
        log.info("Iteration #{}".format(num_iterations))
        threads = []
        for file in args.files:
            absolute_path = os.path.abspath(file)
            module_name = os.path.splitext(absolute_path)[0]
            module = SourceFileLoader(module_name, absolute_path).load_module()

            # module = importlib.import_module(basename)
            if module.list_of_requests == None:
                raise Exception(
                        "Error importing [%s]: variable list_of_requests not defined" % file)
            if args.parallel:
                log.info("Running flows in parallel")
                thread = threading.Thread(target=run_one_file, args=[file, module.list_of_requests])
                threads.append(thread)
                thread.start()
            else:
                run_one_file(file, module.list_of_requests)
        for thread in threads:
            thread.join()
        log.info("Iteration #{} complete".format(num_iterations))

    if total_synthesis > 0:
        log.info("Average first-chunk latency (over {} synthesis requests): {} seconds".format(total_synthesis, total_first_chunk_latency/(total_synthesis)))

    if args.jaeger:
        tracer.close()
        # Need to give time to tracer to flush the spans: https://github.com/jaegertracing/jaeger-client-python/issues/50
        time.sleep(2)
    print("Done")


if __name__ == '__main__':
    run()
