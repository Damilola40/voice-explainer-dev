import base64
from rest_framework.decorators import api_view
from rest_framework.response import Response
from explainer import explain

@api_view(['POST'])
def explain_view(request):
    user_input = request.data.get("user_input", "")
    if not user_input:
        return Response({"error": "No user input provided."}, status=400)

    explanation_text, audio_data = explain(user_input)

    if not audio_data:
        return Response({"error": "Could not generate audio."}, status=500)

    # Consume the generator into raw bytes
    audio_bytes = b"".join(chunk for chunk in audio_data)

    # Encode those bytes as a base64 string so they're safe to put in JSON
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

    return Response({
        "explanation": explanation_text,
        "audio_base64": audio_base64
    })