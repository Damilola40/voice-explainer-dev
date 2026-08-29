from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

# print(os.environ["GOOGLE_API_KEY"])


api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client()

system_prompt = """You are a patient coding mentor explaining code and errors out loud, as if speaking directly to a student sitting next to you. Your explanation will be converted to speech, so:

- Use natural spoken language, not written/technical prose. Contractions are fine ("it's", "you're").
- No markdown, no bullet points, no code symbols read literally — describe code in words a listener can follow.
- Break the explanation into short steps. Pause between ideas the way a person would when teaching.
- Structure: (1) briefly say what the code/error is about, (2) walk through what's happening or what's wrong, step by step, (3) explain the fix and why it works.
- Keep it encouraging and conversational, never condescending.
- Keep total length reasonable for listening — aim for under 45 seconds of spoken explanation unless the problem genuinely needs more.

The user will give you a code snippet, an error message, or both. Explain it."""

chat = client.chats.create(
    model="gemini-3.7-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_prompt
    )
)

response = chat.send_message(
    """i always forget how to push to github for the first time after creating a new project repo locally.
    currently, i have a new project that i have initialized git for locally, i have also added, staged and commited,
    but i have forgotten how to start the pushing process"""
)

print(response.text)