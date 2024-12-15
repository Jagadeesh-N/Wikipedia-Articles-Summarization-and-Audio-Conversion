from flask import Flask, request, jsonify
from google.cloud import bigquery
import os
import logging
from google.api_core.exceptions import BadRequest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Set up BigQuery client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/wikipedia-service-account-key.json"
client = bigquery.Client()

# Replace with your dataset and table
DATASET_ID = "wikipedia_summarizer_dataset"
TABLE_ID = "wikipedia_summarizer_table"


@app.route('/health', methods=['GET'])
def health_check():
    logger.info("Health check endpoint called.")
    return jsonify({"status": "healthy"}), 200


@app.route('/save_metadata', methods=['POST'])
def save_metadata():
    data = request.json
    try:
        table_id = f"{client.project}.{DATASET_ID}.{TABLE_ID}"
        
        # Convert the data into the required format for loading
        rows_to_insert = [data]  # BigQuery expects a list of row dictionaries
        
        # Load the data into the table
        job = client.load_table_from_json(
            rows_to_insert, table_id
        )
        job.result()  # Wait for the job to complete
        
        if job.errors:
            logger.error(f"BigQuery insertion errors: {job.errors}")
            return jsonify({"status": "error", "message": "Failed to save metadata to BigQuery"}), 500

        logger.info("Metadata saved successfully to BigQuery.")
        return jsonify({"status": "success", "message": "Metadata saved successfully"}), 200
    except Exception as e:
        logger.error(f"Error saving metadata: {str(e)}")
        return jsonify({"status": "error", "message": f"Error saving metadata: {str(e)}"}), 500


@app.route('/update_rating', methods=['POST'])
def update_rating():
    data = request.json
    article_title = data.get("article_title")
    user_desired_length = data.get("user_desired_length")
    user_rating = data.get("user_rating")

    if not article_title or not user_desired_length or user_rating is None:
        logger.error("Invalid input for updating rating.")
        return jsonify({"status": "error", "message": "Invalid input for updating rating"}), 400

    query = f"""
    UPDATE `{client.project}.{DATASET_ID}.{TABLE_ID}`
    SET user_rating = @user_rating
    WHERE article_title = @article_title
    AND user_desired_length = @user_desired_length
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_rating", "FLOAT", user_rating),
            bigquery.ScalarQueryParameter("article_title", "STRING", article_title),
            bigquery.ScalarQueryParameter("user_desired_length", "INTEGER", int(user_desired_length)),
        ]
    )

    try:
        logger.info("Updating BigQuery table with user rating...")
        client.query(query, job_config=job_config).result()
        logger.info("User rating updated successfully in BigQuery.")
        return jsonify({"status": "success", "message": "User rating updated successfully"}), 200
    except BadRequest as e:
        logger.error(f"Error updating rating: {str(e)}")
        return jsonify({"status": "error", "message": f"Error updating rating: {str(e)}"}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"status": "error", "message": f"Unexpected error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)