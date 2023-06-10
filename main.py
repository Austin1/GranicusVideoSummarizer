import requests
from moviepy.editor import VideoFileClip
from google.cloud import speech_v1p1beta1 as speech
from pydub import AudioSegment
import openai
import os


os.environ["OPEN_API_KEY"] = "add_openai_api.key"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "add_google_service_acct_key.json"

# The path where you want to save the video
video_path = 'video.mp4'

# Download the video if it doesn't already exist
if not os.path.exists(video_path):
    video_url = "https://archive-video.granicus.com/tnga/tnga_d0b91c00-0200-4a90-b148-57eefa357c8e.mp4"
    response = requests.get(video_url)
    with open(video_path, 'wb') as f:
        f.write(response.content)

# Extract the audio
video = VideoFileClip(video_path)
audio_path = 'audio.wav'
video.audio.write_audiofile(audio_path)

# Convert the audio to mono
audio = AudioSegment.from_wav(audio_path)
audio = audio.set_channels(1)
audio_mono_path = 'audio_mono.wav'
audio.export(audio_mono_path, format='wav')

# Transcribe the audio if the transcript file is not already populated
transcript_path = 'transcript.txt'
if not os.path.exists(transcript_path) or os.path.getsize(transcript_path) == 0:
    client = speech.SpeechClient()
    transcript = ''
    chunk_size = 16000 * 60  # One minute chunks
    with open(audio_mono_path, 'rb') as audio_file:
        while True:
            chunk = audio_file.read(chunk_size)
            if not chunk:
                break
            audio = speech.RecognitionAudio(content=chunk)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=44100,
                language_code="en-US",
            )
            response = client.recognize(config=config, audio=audio)
            transcript += ' '.join([result.alternatives[0].transcript for result in response.results])

    # Write the transcript to a file
    with open(transcript_path, 'w') as f:
        f.write(transcript)
else:
    # Load the transcript from the file
    with open(transcript_path, 'r') as f:
        transcript = f.read()

# Summarize the last part of the transcript that fits within the token limit
max_tokens = 4097 - 100  # Leave some room for the completion
transcript = transcript[-max_tokens:]

response = openai.Completion.create(
  engine="text-davinci-002",
  prompt="Summarize: " + transcript,
  temperature=0.3,
  max_tokens=3337
)
summary = response.choices[0].text.strip()
# Write the summary to a file
with open('summary.txt', 'w') as f:
    f.write(summary)