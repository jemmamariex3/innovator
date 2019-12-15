import nuance_tts_pb2
import nuance_tts_pb2_grpc

list_of_requests = []

# GetVoices request
request = nuance_tts_pb2.GetVoicesRequest()
request.voice.name = "Evan"

# Add request to list
list_of_requests.append(request)

# ---

# Synthesis request
request = nuance_tts_pb2.SynthesisRequest()

request.voice.name = "Evan"
request.voice.model = "xpremium-high"

pcm = nuance_tts_pb2.PCM(sample_rate_hz=22050)
request.audio_params.audio_format.pcm.CopyFrom(pcm)

request.audio_params.volume_percentage = 80
request.audio_params.speaking_rate_percentage = 50
request.audio_params.audio_chunk_duration_ms = 2000

request.input.type = "text/plain;charset=utf-8"
request.input.body = "Hello, User. I'm Evan. How is your day going?"

request.event_params.send_log_events = True

#Add request to list
list_of_requests.append(request)

# ---

