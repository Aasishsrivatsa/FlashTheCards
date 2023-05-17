from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import random
import csv

class Backend:
    csv_file_path = 'flashcards.csv'

    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.questions = []
        self.load_flashcards()

        self.app.route('/')(self.index)
        self.app.route('/add-card')(self.add_card)
        self.app.route('/start-app')(self.start)
        self.app.route('/flashcard', methods=['GET'])(self.get_flashcard)
        self.app.route('/save_flashcard', methods=['POST'])(self.save_flashcard)

    def index(self):
        return render_template("index.html")
    
    def add_card(self):
        return render_template("add-card.html")
    
    def start(self):
        return render_template("start-app.html")

    def load_flashcards(self):
        try:
            # Load flashcards from the CSV file
            with open(self.csv_file_path, 'r') as file:
                reader = csv.reader(file)
                self.questions = list(reader)
        except Exception as e:
            # Handle the exception, e.g., print an error message or log the exception
            print(f"An error occurred while loading flashcards: {e}")

    def get_flashcard(self):
        flashcard = random.choice(self.questions)
        return jsonify(flashcard)

    def save_flashcard(self):
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

        if not question or not answer:
            # Return an error response indicating missing question or answer
            return jsonify({'success': False, 'error': 'Question and answer are required.'})
        else:
            try:
                # Save the data to the CSV file
                with open(self.csv_file_path, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([question, answer, time_taken, correctness])
                    self.questions.append([question, answer, time_taken, correctness])
            except Exception as e:
                # Handle the exception, e.g., print an error message or log the exception
                print(f"An error occurred while saving the flashcard: {e}")
                return jsonify({"success": False})

            return jsonify({"success": True})

if __name__ == "__main__":
    server = Backend()
    server.app.run(host="0.0.0.0", debug=True)
