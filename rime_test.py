import os
import base64
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("RIME_API_KEY")

url = "https://users.rime.ai/v1/rime-tts"

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "text": "Great job! Your last bench press was 50 kilograms for 8 reps.",
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

print("Status:", status_code)

if status_code != 200:
    print(response_body.decode("utf-8"))
    exit()

result = json.loads(response_body.decode("utf-8"))

# Rime returns audio as base64
audio_base64 = result["audioContent"]

audio_data = base64.b64decode(audio_base64)

with open("rime_test.wav", "wb") as f:
    f.write(audio_data)

print("Rime voice generated successfully!")
print("Saved as rime_test.wav")
