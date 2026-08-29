from pathlib import Path
from explainer import explain, save_audio

# print(os.environ["GOOGLE_API_KEY"])

text, audio = explain("What is an API?")
save_audio(audio, "output.mp3")
print(text)