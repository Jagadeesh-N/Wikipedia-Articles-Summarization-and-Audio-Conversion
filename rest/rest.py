import base64
import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
import json
import logging
from flask import make_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("REST_API")

app = Flask(__name__)

# Enable CORS
# CORS(app, resources={r"/*": {"origins": "http://35.224.159.154"}}, supports_credentials=True)
# CORS(app, resources={r"/*": {"origins": "http://35.224.159.154","methods": ["GET", "POST", "OPTIONS"],"allow_headers": ["Content-Type", "Authorization"]}}, supports_credentials=True)
CORS(app, resources={r"/*": {"origins": ["http://35.224.159.154", "http://34.8.205.9"]}}, supports_credentials=True)


# Redis connection
redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "redis-service"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

SUMMARIZER_URL = "http://summarizer-service:5000/summarize"
TTS_URL = "http://tts-service:5000/tts"
STORAGE_URL = "http://storage-handler-service:5000/upload"
STORAGE_RETRIEVE_URL = "http://storage-handler-service:5000/retrieve"
METADATA_URL = "http://metadata-service:5000/save_metadata"
METADATA_UPDATE_URL = "http://metadata-service:5000/update_rating"

@app.route('/health', methods=['GET'])
def health_check():
    logger.info("Health check called.")
    return jsonify({"status": "healthy"}), 200

@app.route('/process', methods=['OPTIONS', 'POST'])
def process_request():
    if request.method == "OPTIONS":
        logger.info(f"Processing request:CROS OPTIONS METHOD IN process_request")
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "http://35.224.159.154"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        # # logger.info(f"Response headers: {response.headers}")
        return response
    data = request.json
    logger.info(f"Processing request....: {data}")
    article_input = data.get('input')
    target_length = data.get('target_length', 100)

    if not article_input:
        logger.error("Invalid input provided.")
        response = jsonify({"status": "error", "message": "Invalid input provided"})
        response.headers["Access-Control-Allow-Origin"] = "http://35.224.159.154"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        # # logger.info(f"Response headers: {response.headers}")
        return response,400

    is_url = article_input.startswith("http")
    formatted_title = article_input.title() if not is_url else article_input.split("/")[-1].replace("_", " ").title()
    cache_key = f"{formatted_title}:{target_length}"
    # Prepare GCS folder and filenames
    main_folder = formatted_title.replace(" ", "_")
    subfolder = f"target_length_{target_length}"
    audio_filename = f"{main_folder}.mp3"
    summary_filename = f"{main_folder}_summary.txt"
    
    files_check_playlod_in_storage = {
        "main_folder": main_folder,
        "subfolder": subfolder,
        "summary_filename": summary_filename,
        "audio_filename": audio_filename
    }

    # Check Redis cache
    cached_data = redis_client.get(cache_key)
    if cached_data:
        logger.info("Cache hit! Returning cached data.")
        cached_response = json.loads(cached_data)
        cached_response["metadata"] = {
            "article_title": formatted_title,
            "user_desired_length": target_length
        }
        response = jsonify(cached_response)
        response.headers["Access-Control-Allow-Origin"] = "http://35.224.159.154"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        # logger.info(f"Response headers: {response.headers}")
        return response
    #Storage Check
    storage_response = requests.post(STORAGE_RETRIEVE_URL,json=files_check_playlod_in_storage)
    if(storage_response.status_code==200):
        logger.info("Storage hit! Returning Storage data.")
        files_data = storage_response.json()
        storage_response_data = {
            "summary": base64.b64decode(files_data["summary_text"]).decode('utf-8'),
            "audio_base64": files_data["audio_base64"]
        }
        storage_response_data["metadata"] = {
            "article_title": formatted_title,
            "user_desired_length": target_length
        }
        response = jsonify(storage_response_data)
        response.headers["Access-Control-Allow-Origin"] = "http://35.224.159.154"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response
    
    logger.info("Cache and Storage miss. Processing request through all backend services...")
    
    # Call summarization service
    logger.info(f"Sending request to summarizer: {SUMMARIZER_URL}")
    summarization_payload = {"input": article_input, "is_url": is_url, "target_length": target_length}
    # summary_response = requests.post(SUMMARIZER_URL, json=summarization_payload)
    with requests.Session() as session:
        summary_response = session.post(SUMMARIZER_URL, json=summarization_payload)
    if summary_response.status_code != 200:
        logger.error("Error in summarization service.")
        response = jsonify({"status": "error", "message": "Error in summarization"})
        response.headers["Access-Control-Allow-Origin"] = "http://35.224.159.154"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        # logger.info(f"Response headers: {response.headers}")
        return response, 500
    logger.info(f"Received Reponse from summarization service: {SUMMARIZER_URL}")
    summary = summary_response.json().get("summary")
    original_article_length = summary_response.json().get("original_article_length")

    # Call TTS service
    logger.info(f"Sending request to tts service: {TTS_URL}")
    tts_payload = {"summary": summary, "title": formatted_title}
    tts_response = requests.post(TTS_URL, json=tts_payload)
    if tts_response.status_code != 200:
        logger.error("Error in TTS service.")
        response = jsonify({"status": "error", "message": "Error in TTS service"})
        response.headers["Access-Control-Allow-Origin"] = "http://35.224.159.154"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        # logger.info(f"Response headers: {response.headers}")
        return response, 500
    logger.info(f"Recieved Response from tts service: {TTS_URL}")
    audio_base64 = tts_response.json().get("audio_base64")
    audio_duration = tts_response.json().get("audio_duration_minutes")

    # Upload audio file to GCS
    audio_storage_payload = {
        "folder": f"{main_folder}/{subfolder}",
        "filename": audio_filename,
        "file_content": audio_base64
    }
    logger.info(f"Sending request to Storage service to add audio..")
    storage_response_audio = requests.post(STORAGE_URL, json=audio_storage_payload)
    if storage_response_audio.status_code != 200:
        logger.error("Error uploading audio file to storage service.")
        response = jsonify({"status": "error", "message": "Error uploading audio file to storage service"})
        response.headers["Access-Control-Allow-Origin"] = "http://35.224.159.154"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        # logger.info(f"Response headers: {response.headers}")
        return response, 500

    # Upload summary file to GCS
    summary_storage_payload = {
        "folder": f"{main_folder}/{subfolder}",
        "filename": summary_filename,
        "file_content": base64.b64encode(summary.encode()).decode()
    }
    logger.info(f"Sending request to Storage service to add summary..")
    storage_response_summary = requests.post(STORAGE_URL, json=summary_storage_payload)
    if storage_response_summary.status_code != 200:
        logger.error("Error uploading summary file to storage service.")
        response = jsonify({"status": "error", "message": "Error uploading summary file to storage service"})
        response.headers["Access-Control-Allow-Origin"] = "http://35.224.159.154"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        # logger.info(f"Response headers: {response.headers}")
        return response, 500

    logger.info(f"Recieved Response from storage service..")
    gcs_folder_url = storage_response_audio.json().get("gcs_url")

    # Save metadata
    metadata = {
        "article_title": formatted_title,
        "original_article_length": original_article_length,
        "user_desired_length": target_length,
        "summary_length": len(summary.split()),
        "audio_file": f"{main_folder}/{subfolder}/{audio_filename}",
        "summary_file": f"{main_folder}/{subfolder}/{summary_filename}",
        "wikipedia_url": article_input if is_url else f"https://en.wikipedia.org/wiki/{article_input.title().replace(' ', '_')}",
        "GCS_storage_url": gcs_folder_url,
        "user_rating": None,
        "audio_duration_minutes": audio_duration
    }
    logger.info(f"Sending request to Database service: {METADATA_URL}")
    metadata_response = requests.post(METADATA_URL, json=metadata)
    if metadata_response.status_code != 200:
        logger.error("Error in metadata service.")
        response = jsonify({"status": "error", "message": "Error in metadata service"})
        response.headers["Access-Control-Allow-Origin"] = "http://35.224.159.154"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        # logger.info(f"Response headers: {response.headers}")
        return response, 500

    # Cache the response
    logger.info(f"Cahching the encoded data....")
    response_data = {"summary": summary, "audio_base64": audio_base64}
    redis_client.set(cache_key, json.dumps(response_data), ex=3600)
    logger.info(f"Data cached for {formatted_title}.")

    logger.info(f"Adding metadata field in the response data....")
    response_data["metadata"] = {
        "article_title": formatted_title,
        "user_desired_length": target_length
    }
    logger.info(f"Returning to the response to frontend....")
    response_f = jsonify(response_data)
    response_f.headers["Access-Control-Allow-Origin"] = "http://35.224.159.154"
    response_f.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response_f.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response_f.headers["Access-Control-Allow-Credentials"] = "true"
    # logger.info(f"Response headers: {response_f.headers}")
    return response_f

@app.route('/submit_rating', methods=['POST','OPTIONS'])
def submit_rating():
    if request.method == "OPTIONS":
        logger.info(f"Processing request: CROS OPTIONS METHOD IN submit_rating")
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "http://35.224.159.154"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        # logger.info(f"Response headers: {response.headers}")
        return response
    data = request.json
    logger.info(f"Processing request: {data}")
    article_title = data.get("article_title")
    user_desired_length = data.get("user_desired_length")
    user_rating = data.get("user_rating")

    if not article_title or not user_desired_length or user_rating is None:
        logger.error("Invalid input for updating rating.")
        response = jsonify({"status": "error", "message": "Invalid input for updating rating"})
        response.headers["Access-Control-Allow-Origin"] = "http://35.224.159.154"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        # logger.info(f"Response headers: {response.headers}")
        return response, 400

    update_payload = {
        "article_title": article_title,
        "user_desired_length": user_desired_length,
        "user_rating": user_rating
    }
    response = requests.post(METADATA_UPDATE_URL, json=update_payload)
    if response.status_code != 200:
        logger.error("Error updating rating in metadata.")
        response = jsonify({"status": "error", "message": "Error updating rating in metadata"})
        response.headers["Access-Control-Allow-Origin"] = "http://35.224.159.154"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        # logger.info(f"Response headers: {response.headers}")
        return response, 500

    logger.info("User feedback successfully submitted.")
    response = jsonify({"status": "success", "message": "Thank you for your feedback!"})
    response.headers["Access-Control-Allow-Origin"] = "http://35.224.159.154"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    # logger.info(f"Response headers: {response.headers}")
    return response

@app.route('/process', methods=['OPTIONS'])
def handle_options():
    logger.info(f"Processing request CROS, handle_options()")
    response = make_response()
    response.headers["Access-Control-Allow-Origin"] = "http://35.224.159.154"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    # logger.info(f"Response headers: {response.headers}")
    return response

@app.after_request
def add_cors_headers(response):
    logger.info(f"Processing request: CROS add_cors_headers")
    response.headers["Access-Control-Allow-Origin"] = "http://35.224.159.154"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    # logger.info(f"Response headers: {response.headers}")
    return response
    
@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all exceptions with CORS-compliant error response."""
    logger.error(f"Unhandled exception: {e}")
    response = jsonify({"error": str(e)})
    response.status_code = 500
    return add_cors_headers(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)