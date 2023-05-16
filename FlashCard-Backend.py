from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import random
import csv

class Backend:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.csv_file_path = 'flashcards.csv'
        self.questions = []

        @self.app.route('/')
        def index():
            return render_template("index.html")
        
        @self.app.route('/add-card')
        def add_card():
            return render_template("add-card.html")
        
        @self.app.route('/start-app')
        def start():
            return render_template("start-app.html")

        @self.app.route('/flashcard', methods=['GET'])
        def get_flashcard():
            flashcard = random.choice(self.questions)
            return jsonify(flashcard)

        @self.app.route('/save_flashcard', methods=['POST'])
        def save_flashcard():
            # Get user inputs from the request
            question = request.form.get("question")
            answer = request.form.get("answer")
            time_taken = request.form.get("time")
            correctness = request.form.get("correctness")

            # Replace commas with pipes
            question = question.replace(",", "|")
            answer = answer.replace(",", "|")
            time_taken = time_taken.replace(",", "|")
            correctness = correctness.replace(",", "|")

            try:
                # Save the data to the CSV file
                with open(self.csv_file_path, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([question, answer, time_taken, correctness])
            except Exception as e:
                # Handle the exception, e.g., print an error message or log the exception
                print(f"An error occurred while saving the flashcard: {e}")
                return jsonify({"success": False})

            return jsonify({"success": True})

if __name__ == "__main__":
    Server = Backend()
    Server.app.run(host="0.0.0.0", debug=True)
