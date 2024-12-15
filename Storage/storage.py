from flask import Flask, request, jsonify
from google.cloud import storage
import base64
import os
import logging
from io import BytesIO

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Storage_Service")

# Initialize GCS client
gcs_client = storage.Client()
bucket_name = os.getenv("GCS_BUCKET_NAME", "wikipedia-summarizer-storage")

def upload_to_gcs(bucket_name, folder, filename, file_data):
    """Upload a file to GCS."""
    try:
        bucket = gcs_client.bucket(bucket_name)
        blob = bucket.blob(f"{folder}/{filename}")
        blob.upload_from_file(BytesIO(file_data))
        logger.info(f"File {filename} uploaded to bucket {bucket_name} in folder {folder}.")
        return f"https://storage.googleapis.com/{bucket_name}/{folder}/{filename}"
    except Exception as e:
        logger.error(f"Error uploading to GCS: {e}")
        raise

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Uploads a file (audio or summary) to GCS.
    Accepts JSON payload with 'folder', 'filename', and 'file_content' (base64-encoded).
    """
    data = request.json
    folder = data.get("folder")
    filename = data.get("filename")
    file_content = data.get("file_content")

    if not all([folder, filename, file_content]):
        logger.error("Invalid payload received for upload.")
        return jsonify({"status": "error", "message": "Invalid payload"}), 400

    try:
        # Decode the base64 content
        file_data = base64.b64decode(file_content)

        # Upload to GCS
        gcs_url = upload_to_gcs(bucket_name, folder, filename, file_data)
        return jsonify({
            "status": "success",
            "object_name": f"{folder}/{filename}",
            "gcs_url": gcs_url
        }), 200
    except Exception as e:
        logger.error(f"Error during upload: {e}")
        return jsonify({"status": "error", "message": f"Error during upload: {e}"}), 500
        
@app.route('/retrieve', methods=['POST'])
def retrieve_files():
    """
    Retrieves a files (audio or summary) from GCS.
    Accepts JSON payload with 'main folder', 'sub folder','summary filename', and 'audio filename'
    """
    logging.info("Checking the files in GCS,{bucket_name}......")
    data = request.json
    main_folder = data.get('main_folder')
    subfolder = data.get('subfolder')
    summary_filename = data.get('summary_filename')
    audio_filename = data.get('audio_filename')
    bucket = gcs_client.bucket(bucket_name)
    summary_blob = bucket.blob(f"{main_folder}/{subfolder}/{summary_filename}")
    audio_blob = bucket.blob(f"{main_folder}/{subfolder}/{audio_filename}")
    if summary_blob.exists() and audio_blob.exists():
        summary_blob = summary_blob.download_as_bytes()
        audio_blob = audio_blob.download_as_bytes()
        logging.info("Summary and Audio file exists....Returning encoded files to rest")
        return jsonify({
            "summary_text": base64.b64encode(summary_blob).decode('utf-8'),
            "audio_base64": base64.b64encode(audio_blob).decode('utf-8')
        }), 200
    else:
        logging.info("Summary and Audio does not exists....Returning error message, 404")
        return jsonify({"error": "Files not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)