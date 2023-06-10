# Download and analyze Granicus Video File
Quickly threw this together using ChatGPT to program this script to download a video file from Granicus, export the audio, transcribe the audio with Google's speech-to-text API, then attempt summarizing with GPT3.

# Issues
The summary produced is terrible. I manually chopped the transcript into two relevant sections based on finding the end of a topic in the transcript where it says "thank you". I then pasted these into Chatgpt (GPT4). This create a much more relevant output than the Python program did.

However, providing it in case someone wants to modify or commit changes to make it better.

# Pre Requisites
install ffmpeg
```brew install ffmpeg``` on MacOS
setup virtualenv and install packages
```
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
