from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import random

class Backend:
    app = Flask(__name__)
    CORS(app)

    flashcards = [
        { 'question': 'What is the capital of France?', 'answer': 'Paris' },
        { 'question': 'Who painted the Mona Lisa?', 'answer': 'Leonardo da Vinci' },
        # Add more flashcards here
    ]

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/flashcard', methods=['GET'])
    def get_flashcard():
        flashcard = random.choice(Backend.flashcards)
        return jsonify(flashcard)

if __name__ == "__main__":
    Server = Backend()
    Server.app.run(host="0.0.0.0", debug=True)
