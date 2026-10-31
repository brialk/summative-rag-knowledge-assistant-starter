from flask import Flask, jsonify, request
from flask_cors import CORS

from config import Config
from rag_service import answer_question
from vector_store import ModelServiceError

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": Config.CLIENT_ORIGIN}})


@app.get("/api/health")
def health():
    """Confirm that the backend is running."""
    return jsonify(
        {
            "status": "ok",
            "message": "Backend is running.",
        }
    ), 200


@app.post("/api/ask")
def ask_question():
    """
    Receive a question from the frontend and return an answer with sources.

    Steps:
    1. Read the JSON body.
    2. Check that a non-blank question was sent (otherwise return 400).
    3. Call answer_question(question) to run the RAG workflow.
    4. Return the answer and sources as JSON (or a 502 if the model service fails).
    """
    data = request.get_json(silent=True)

    # The body must be a JSON object like {"question": "..."}.
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be JSON with a 'question' field.", "sources": []}), 400

    question = data.get("question")
    if not isinstance(question, str) or not question.strip():
        return jsonify({"error": "Question is required.", "sources": []}), 400

    try:
        result = answer_question(question.strip())
    except ModelServiceError as error:
        # The model service (Ollama) is down or failed: a 502 means
        # "the service behind me had a problem".
        return jsonify({"error": str(error), "sources": []}), 502

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(debug=True, port=5555)
