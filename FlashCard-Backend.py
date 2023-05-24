from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import random
import threading
from DataCSV import DataHandler

csv_path = 'flashcards.csv'

class Backend:

    def __init__(self, path=csv_path) -> None:
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

    def run_in_thread(self, func):
        def wrapper(*args, **kwargs):
            threading.Thread(target=func, args=args, kwargs=kwargs).start()
        return wrapper

    def hompage(self):
        return render_template("homepage.html")

    def add_card(self):
        return render_template("add-card.html")

    def start(self):
        return render_template("start-app.html")

    def load_flashcards(self):
        self.questions = DataHandler.read_csv(self.csv_file_path)

    def get_flashcard(self):
        if len(self.questions) == 0:
            self.load_flashcards()

        flashcard1_selc= random.randint(0,3)
        flashcard1 = self.questions[flashcard1_selc]
        flashcard2 = random.choice(self.questions)

        flashcard_chooser = []
        flashcard_chooser.append(flashcard1)
        flashcard_chooser.append(flashcard2)

        flashcard = random.choice(flashcard_chooser)

        response = {
            'question' : flashcard[0],
            'answer' : flashcard[1]
        }
        return jsonify(response)

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

        question_list = [question,answer,time_taken,correctness,number_of_times_seen]

        if not question or not answer:
            # Return an error response indicating missing question or answer
            return jsonify({"success": False, "message": "An error occurred while saving the flashcard."})
        else:
            append = DataHandler.append_data(question_list, self.csv_file_path)

            self.run_in_thread(append)
            self.questions.append(question_list)
            return jsonify({"success": True, "message": "Flashcard saved!"})


if __name__ == "__main__":
    server = Backend()
    server.load_flashcards()
    server.app.run(host="0.0.0.0", debug=True)
