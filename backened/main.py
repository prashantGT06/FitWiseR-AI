from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from ai import ask_coach, generate_voice


app = FastAPI()


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# HOME
# =========================

@app.get("/")
def home():

    return {
        "message": "FitWiseR AI Backend is running!"
    }


# =========================
# HEALTH
# =========================

@app.get("/health")
def health():

    return {
        "status": "OK"
    }


# =========================
# CHAT
# =========================

@app.get("/chat")
def chat(message: str):

    answer = ask_coach(message)

    return {
        "user_message": message,
        "coach_response": answer
    }


# =========================
# COACH
# =========================

@app.get("/coach")
def coach(message: str):

    # Gemini response
    answer = ask_coach(message)

    # Rime voice
    audio_data = generate_voice(answer)

    # Save audio
    audio_path = "coach_response.wav"

    with open(audio_path, "wb") as audio_file:
        audio_file.write(audio_data)

    return {
        "user_message": message,
        "coach_response": answer,
        "audio": "/audio"
    }


# =========================
# AUDIO
# =========================

@app.get("/audio")
def audio():

    return FileResponse(
        "coach_response.wav",
        media_type="audio/wav"
    )
    