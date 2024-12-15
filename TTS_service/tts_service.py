from flask import Flask, request, jsonify
from gtts import gTTS
from pydub import AudioSegment
import base64
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TTS_Service")

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    logger.debug("Readiness probe called.")
    return jsonify({"status": "healthy"}), 200

def text_to_audio(summary, title):
    try:
        formatted_title = title.title().replace(" ", "_")
        filename = f"{formatted_title}.mp3"

        logger.info("Generating audio...")
        tts = gTTS(summary)
        tts.save(filename)
        logger.info(f"Audio saved as {filename}")

        with open(filename, "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')

        audio = AudioSegment.from_mp3(filename)
        audio_duration = len(audio) / (1000 * 60)
        logger.info(f"Audio generated successfully. Duration: {audio_duration} minutes.")

        return {"audio_base64": audio_base64, "audio_duration_minutes": round(audio_duration, 2)}
    except Exception as e:
        logger.error(f"Error during TTS processing: {str(e)}")
        return {"error": f"Error during TTS processing: {str(e)}"}

@app.route('/tts', methods=['POST'])
def tts_endpoint():
    data = request.json
    summary = data.get('summary')
    title = data.get('title')

    if not summary or not title:
        logger.error("Invalid input for TTS service.")
        return jsonify({"error": "Summary or title not provided"}), 400

    tts_result = text_to_audio(summary, title)
    if "error" in tts_result:
        return jsonify(tts_result), 500

    logger.info("TTS service completed successfully.")
    return jsonify(tts_result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
