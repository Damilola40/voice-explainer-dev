from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
from openai import audio, chat
import time

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)

client = genai.Client()

def explain(user_input: str, max_retries=3):

    system_prompt = """You are a patient coding mentor explaining code and errors out loud, as if speaking directly to a student sitting next to you. 
    Your explanation will be converted to speech, so:
    - Use natural spoken language, not written/technical prose. Contractions are fine ("it's", "you're").
    - No markdown, no bullet points, no code symbols read literally — describe code in words a listener can follow.
    - Break the explanation into short steps. Pause between ideas the way a person would when teaching.
    - Structure: (1) briefly say what the code/error is about, (2) walk through what's happening or what's wrong, step by step, (3) explain the fix and why it works.
    - Keep it encouraging and conversational, never condescending.
    - Keep total length reasonable for listening — aim for under 45 seconds of spoken explanation unless the problem genuinely needs more.
    The user will give you a code snippet, an error message, or both. Explain it."""

    chat = client.chats.create(
        model="gemini-3.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        )
    )

    response = None
    for attempt in range(max_retries):
        try:
            response = chat.send_message(user_input)
            break
        except Exception as e:
            print(f"Gemini attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)  # wait 2 seconds before trying again
            else:
                return "Sorry, I couldn't generate an explanation right now.", None

            
    try:
        audio = elevenlabs.text_to_speech.convert(
            text=response.text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_v3",
            output_format="mp3_44100_128",
        )
        return response.text, audio

    except Exception as e:
        print(f"Error generating audio: {e}")
        return response.text, None
    

def save_audio(audio_generator, filename="output.mp3"):
    try:
        with open(filename, "wb") as f:
            for chunk in audio_generator:
                f.write(chunk)
        return filename
    
    except Exception as e:
        print(f"Error saving audio: {e}")
        return None