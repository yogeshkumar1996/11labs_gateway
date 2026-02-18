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


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tts")
def text_to_speech(payload: dict):
    try:
        print("inside the main handler")
        text = payload["text"]
        voice_id = payload["voice_id"]

       # Generate audio from ElevenLabs
        audio = client.text_to_speech.convert(
            text=request.text,
            voice_id=request.voice_id,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )

        # Return as downloadable MP3 file
        print("sending response")
        return Response(
            content=audio,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=voice.mp3"
            }
        )
        print("response sent")
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
