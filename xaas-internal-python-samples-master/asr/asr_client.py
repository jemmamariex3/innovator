import argparse
import sys
import logging
import os
import grpc
import wave
from time import sleep
from google.protobuf import text_format

from nuance_asr_resource_pb2 import *
from nuance_asr_result_pb2 import *
from nuance_asr_pb2 import *
from nuance_asr_pb2_grpc import *

log = logging.getLogger(__name__)

status = 0

def init_recognizer(args):
  # Declare a DLM
  custom_dlm = RecognitionResource(
      external_reference = ResourceReference(
                            type='DOMAIN_LM', 
                            uri=args.dlmUrn,
                            reuse='HIGH_REUSE'),
                            weight_value=700)

  # Declare a wordset in that DLM 
  places_wordset = RecognitionResource(
      external_reference = ResourceReference(
                            type='WORDSET', 
                            uri='http://host/path/places-wordset.json',
                            reuse='HIGH_REUSE'))

  # Declare an inline wordset in that DLM 
  # places2_wordset = RecognitionResource(inline_wordset='{"PLACES":[{"literal":"Fordoun","spoken":["forden"]},{"literal":"Auchenblae"}]}')

  # Set reco parms, at a minimum language. Add 16kHz sample rate for transcribing 16kHz audio + immutable parm + resources. Add client_data array of key-value pairs. 
  init = RecognizeInitMessage(
    parameters = RecognitionParameters(
          language='eng-USA',
          audio_format = AudioFormat(pcm=PCM(sample_rate_hz=16000)),
          result_type='IMMUTABLE_PARTIAL', 
          recognition_flags = RecognitionFlags(auto_punctuate=True)
      ),
      resources = [ custom_dlm ], # names_places_dlm, places_wordset, places2_wordset
      client_data = {'company':'Aardvark','user':'Leslie'} 
    )

  return init

def parse_args():
    parser = argparse.ArgumentParser(
        prog="asr_client.py",
        usage="%(prog)s [-options]",
        add_help=False,
        formatter_class=lambda prog: argparse.HelpFormatter(
            prog, max_help_position=45, width=100)
    )

    options = parser.add_argument_group("options")
    options.add_argument("-h", "--help", action="help",
                         help="Show this help message and exit")
    options.add_argument("--audioFile", metavar="file", nargs="?",
                         help="Audio file to process (wav).")
    options.add_argument("--nmaid", nargs="?", help=argparse.SUPPRESS)
    options.add_argument("--token", nargs="?", help=argparse.SUPPRESS)
    options.add_argument("-s", "--serverUrl", metavar="url", nargs="?",
                         help="ASR server URL, default=localhost:8080", default='localhost:8080')
    options.add_argument('--dlmUrn', nargs="?", 
                         help="Custom DLM URN")
    options.add_argument("--secure", action="store_true",
                         help="Connect to the server using a secure gRPC channel.")
    options.add_argument("--rootCerts",  metavar="file", nargs="?",
                         help="Root certificates when using secure channel.")
    options.add_argument("--privateKey",  metavar="file", nargs="?",
                         help="Certificate private key when using secure channel.")
    options.add_argument("--certChain",  metavar="file", nargs="?",
                         help="Certificate chain when using secure channel.")

    return parser.parse_args()

def create_channel(args):
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


# Send the recognize request, first with parms, then with audio to transcribe
def stream_out(init, audioFn):
  try:
    wf = wave.open(audioFn, 'r')
    yield RecognizeRequest(recognize_init_message=init)
    samples = wf.readframes(wf.getnframes())
    wf.close()
    def chunks(l, n):
      """Yield successive n-sized chunks from l."""
      for i in range(0, len(l), n):
        yield l[i:i + n]
    for chunk in chunks(samples, 320):
      yield RecognizeRequest(audio=chunk)
      sleep(0.020)
    print('stream complete')
  except Exception as e:
    print(e)
    log.exception(e)
    exit(1)

# Print results on screen
def read_stream_in(stream_in):
  global status
  try:
    for message in stream_in:
      if message.HasField('status'):
        if message.status.details:
          print(f'{message.status.code} {message.status.message} - {message.status.details}')
        else:
          print(f'{message.status.code} {message.status.message}')
        status = message.status
      elif message.HasField('result'):
        if(message.result.result_type):
          print(f'partial : {message.result.hypotheses[0].formatted_text}')
        else:
          print(f'final : {message.result.hypotheses[0].formatted_text}')
  except Exception as e:
      print(e)
      log.exception(e)
      exit(1)


def main():
  args = parse_args()
  log_level = logging.DEBUG
  logging.basicConfig(
      format='%(lineno)d %(asctime)s %(levelname)-5s: %(message)s', level=log_level)
  with create_channel(args) as channel:
    stub = RecognizerStub(channel)
    init = init_recognizer(args)
    stream_in = stub.Recognize(stream_out(init, args.audioFile))
    read_stream_in(stream_in)
  print("Done")

if __name__ == '__main__':
  main()
