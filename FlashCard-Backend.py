from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import random
import csv

csv_path = 'flashcards.csv'

class Backend:

    def __init__(self,path = csv_path) -> None:
        self.csv_file_path = path
        self.app = Flask(__name__)
        CORS(self.app)
        self.questions = []
        self.load_flashcards()

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
            database.append_data([question, answer, time_taken, correctness, number_of_times_seen])
            return jsonify({"success": True})


class DataHandler:
    def __init__(self,path=csv_path) -> None:
        self.csv_file_path = path
    
    def append_data(self, data):
        try:
            self.question = data[0]
            self.answer = data[1]
            self.time_taken = data[2]
            self.correctness = data[3]
            self.number_of_times_seen = data[4]

            # Save the data to the CSV file

            with open(self.csv_file_path, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([self.question, self.answer, self.time_taken, self.correctness, self.number_of_times_seen])
                self.questions.append([self.question, self.answer, self.time_taken, self.correctness, self.number_of_times_seen])

        except Exception as e:

            # Handle the exception, e.g., print an error message or log the exception
            print(f"An error occurred while saving the flashcard: {e}")
            return jsonify({"success": False})

if __name__ == "__main__":
    server = Backend()
    database = DataHandler()
    server.app.run(host="0.0.0.0", debug=True)
