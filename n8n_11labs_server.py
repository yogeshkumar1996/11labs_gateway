from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from elevenlabs.client import ElevenLabs
import os
import uvicorn

# -----------------------------
# CONFIG
# -----------------------------
ELEVENLABS_API_KEY = "sk_3b98d8ce13673dbaa871a04c858b37f6c37f54d52c8d8291"

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

app = FastAPI(title="ElevenLabs Gateway API")


# -----------------------------
# Request model
# -----------------------------
class TTSRequest(BaseModel):
    text: str
    voice_id: str


# -----------------------------
# Gateway endpoint
# -----------------------------
@app.post("/tts")
def text_to_speech(request: TTSRequest):
    try:
        response = client.text_to_speech.with_raw_response.convert(
            text=request.text,
            voice_id=request.voice_id
        )

        char_cost = response.headers.get("x-character-count")
        request_id = response.headers.get("request-id")

        audio_data = response.data

        return Response(
            content=audio_data,
            media_type="audio/mpeg",
            headers={
                "x-character-count": char_cost or "unknown",
                "x-request-id": request_id or "unknown",
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Run with: python3.11 script.py
# -----------------------------
if __name__ == "__main__":
    uvicorn.run(
        "n8n_11labs_server:app",
        host="0.0.0.0",
        port=8040,
        reload=False
    )
