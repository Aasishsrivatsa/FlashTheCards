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

        self.app.route('/')(self.homepage)
        self.app.route('/add-card')(self.add_card)
        self.app.route('/start-app')(self.start)
        self.app.route('/flashcard', methods=['GET'])(self.get_flashcard)
        self.app.route('/save_flashcard', methods=['POST'])(self.save_flashcard)
        self.app.route('/update_flashcard', methods=['POST'])(self.update_flashcard)

    def run_in_thread(self, func):
        def wrapper(*args, **kwargs):
            threading.Thread(target=func, args=args, kwargs=kwargs).start()
        return wrapper

    def homepage(self):
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

        flashcard1 = self.questions[random.randint(0, 2]
        flashcard2 = random.choice(self.questions)

        flashcard_chooser = []
        flashcard_chooser.append(flashcard1)
        flashcard_chooser.append(flashcard2)

        flashcard = random.choice(flashcard_chooser)

        response = {
            'question': flashcard[0],
            'answer': flashcard[1]
        }
        return jsonify(response)

    def save_flashcard(self):
        question = request.form.get("question")
        answer = request.form.get("answer")
        time_taken = 0
        correctness = True
        number_of_times_seen = 0

        question = question.replace(",", "|")
        answer = answer.replace(",", "|")

        question_list = [question, answer, time_taken, correctness, number_of_times_seen]

        if not question or not answer:
            return jsonify({"success": False, "message": "An error occurred while saving the flashcard."})
        else:
            append = DataHandler.append_data(question_list, self.csv_file_path)
            self.run_in_thread(append)
            self.questions.append(question_list)
            return jsonify({"success": True, "message": "Flashcard saved!"})

    def update_flashcard(self):
        question = request.form.get("question")
        time_taken = request.form.get("time")
        correctness = request.form.get("correctness")
        
        data = [question, time_taken, correctness]
        update = DataHandler.update_flashcard(data, self.csv_file_path)
        
        self.run_in_thread(update)
        
        return jsonify({"success": True, "message": "Response collected"})


if __name__ == "__main__":
    server = Backend()
    server.load_flashcards()
    server.app.run(host="0.0.0.0", debug=True)
