from DataCSV import DataHandler
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import random

csv_path = 'flashcards.csv'

class Backend:

    def __init__(self,path = csv_path) -> None:
        self.csv_file_path = path
        self.app = Flask(__name__)
        CORS(self.app)
        self.questions = []

        self.app.route('/')(self.hompage)
        self.app.route('/add-card')(self.add_card)
        self.app.route('/start-app')(self.start)
        self.app.route('/flashcard', methods=['GET'])(self.get_flashcard)
        self.app.route('/save_flashcard', methods=['POST'])(self.save_flashcard)

    def hompage(self):
        return render_template("homepage.html")
    
    def add_card(self):
        return render_template("add-card.html")
    
    def start(self):
        return render_template("start-app.html")

    def load_flashcards(self):
        DataHandler.read_csv(self.csv_file_path)

    def get_flashcard(self):
        flashcard = random.choice(self.questions)
        return jsonify(flashcard)

    def save_flashcard(self):
        # Get user inputs from the request
        question = request.form.get("question")
        answer = request.form.get("answer")
        time_taken = 0
        correctness = True
        number_of_times_seen = 0

        # Replace commas with pipes
        question = question.replace(",", "|")
        answer = answer.replace(",", "|")

        if not question or not answer:
            # Return an error response indicating missing question or answer
            return jsonify({'success': False, 'error': 'Question and answer are required.'})
        else:
            DataHandler.append_data([question, answer, time_taken, correctness, number_of_times_seen],self.csv_file_path)
            return jsonify({"success": True})


if __name__ == "__main__":
    server = Backend()
    server.app.run(host="0.0.0.0", debug=True)
