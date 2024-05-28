import io
from google.oauth2 import service_account
from google.cloud import speech

def transcribe_audio(audio_file):
  client_file = "./key.json"
  credentials = service_account.Credentials.from_service_account_file(client_file)
  client = speech.SpeechClient(credentials=credentials)

  with io.open(audio_file, 'rb') as f:
    content = f.read()
    audio = speech.RecognitionAudio(content=content)

  config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    # sample_rate_hertz=16000,
    sample_rate_hertz=44100,
    language_code='mn-MN'
  )

  response = client.recognize(config=config, audio=audio)

  transcription = ""
  for result in response.results:
    transcription += result.alternatives[0].transcript + "\n"

  return transcription