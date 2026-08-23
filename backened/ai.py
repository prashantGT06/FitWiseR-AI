import os
import base64
import json
import urllib.request
import urllib.error

from dotenv import load_dotenv
from google import genai
from qdrant_client import QdrantClient

load_dotenv()


# =========================
# GEMINI
# =========================

gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# =========================
# QDRANT
# =========================

qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION_NAME = "workout_memory"


def get_workout_memory():

    results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=[0.1, 0.2, 0.3, 0.4],
        limit=1
    )

    if not results.points:
        return "No previous workout found."

    point = results.points[0]

    return (
        f"Exercise: {point.payload['exercise']}, "
        f"Weight: {point.payload['weight']} kg, "
        f"Reps: {point.payload['reps']}, "
        f"Date: {point.payload['date']}"
    )


# =========================
# GEMINI COACH
# =========================

def ask_coach(user_message):

    memory = get_workout_memory()

    prompt = f"""
You are RepCoach AI, a friendly personal gym coach.

Previous workout memory:
{memory}

User says:
{user_message}

Answer naturally and briefly.

Use the previous workout memory when relevant.
Do not invent workout history.
"""

    response = gemini_client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text


# =========================
# RIME TEXT TO SPEECH
# =========================

def generate_voice(text):

    api_key = os.getenv("RIME_API_KEY")

    url = "https://users.rime.ai/v1/rime-tts"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "speaker": "cove",
        "modelId": "mistv2"
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:

        with urllib.request.urlopen(request) as response:

            response_body = response.read()
            status_code = response.getcode()

    except urllib.error.HTTPError as error:

        response_body = error.read()
        status_code = error.code

    if status_code != 200:
        raise Exception(
            response_body.decode("utf-8")
        )

    result = json.loads(
        response_body.decode("utf-8")
    )

    audio_base64 = result["audioContent"]

    audio_data = base64.b64decode(
        audio_base64
    )

    return audio_data
