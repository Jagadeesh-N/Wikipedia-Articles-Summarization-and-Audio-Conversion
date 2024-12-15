from flask import Flask, request, jsonify
from transformers import pipeline
from bs4 import BeautifulSoup
import requests
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Summarizer")

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

def scrape_wikipedia_article(input_value, is_url=False):
    url = input_value if is_url else f"https://en.wikipedia.org/wiki/{input_value.title().replace(' ', '_')}"
    logger.info(f"Fetching Wikipedia article from URL: {url}")
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article = ""
        for paragraph in soup.find_all('p'):
            text = paragraph.get_text()
            clean_text = re.sub(r'\[\d+\]|\[\w+\]', '', text)  # Remove references
            article += clean_text
        logger.info("Article successfully fetched and cleaned.")
        return article
    else:
        logger.error(f"Failed to fetch article with status code {response.status_code}")
        return None

def summarize_text(text, target_length, max_chunk_length=1000):
    logger.info("Starting text summarization.")
    summarizer = pipeline('summarization', model="facebook/bart-large-cnn", device=-1)
    chunks = [text[i:i+max_chunk_length] for i in range(0, len(text), max_chunk_length)]
    summary = ""
    current_length = 0

    for chunk in chunks:
        chunk_summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
        summary += chunk_summary[0]['summary_text'] + " "
        current_length = len(summary.split())
        if current_length >= target_length:
            break

    # Ensure the final summary ends with complete sentences
    summary_sentences = re.split(r'(?<=[.!?]) +', summary.strip())
    final_summary = ""
    for sentence in summary_sentences:
        if len(final_summary.split()) + len(sentence.split()) > target_length + 50:
            break
        final_summary += sentence + " "

    logger.info(f"Summary generated with length: {len(final_summary.split())} words.")
    return final_summary.strip()

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    article_input = data.get("input")
    target_length = int(data.get("target_length", 100))
    is_url = data.get("is_url", False)

    if not article_input:
        logger.error("No input provided for summarization.")
        return jsonify({"error": "No input provided"}), 400

    article = scrape_wikipedia_article(article_input, is_url)
    if not article:
        logger.error("Failed to fetch article.")
        return jsonify({"error": "Failed to fetch article", "original_article_length": 0}), 500

    original_article_length = len(article.split())
    logger.info(f"Original Article Length: {original_article_length} words")
    summary = summarize_text(article, target_length=target_length)
    summary_length = len(summary.split())
    logger.info(f"Summary generated successfully. Length: {summary_length} words")

    return jsonify({
        "summary": summary,
        "original_article_length": original_article_length
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
