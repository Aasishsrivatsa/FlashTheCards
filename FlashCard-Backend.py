from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import random
from DataCSV import DataHandler

csv_path = 'flashcards.csv'

class Backend:
    def __init__(self, path=csv_path) -> None:
        self.csv_file_path = path
        self.app = Flask(__name__)
        CORS(self.app)
        self.questions = []
        self.data_handler = DataHandler()
        asyncio.run(self.load_flashcards())

        self.app.route('/')(self.homepage)
        self.app.route('/add-card')(self.add_card)
        self.app.route('/start-app')(self.start)
        self.app.route('/flashcard', methods=['GET'])(self.get_flashcard)
        self.app.route('/save_flashcard', methods=['POST'])(self.save_flashcard)
        self.app.route('/update_flashcard', methods=['POST'])(self.update_flashcard)

    def homepage(self):
        return render_template("homepage.html")

    def add_card(self):
        return render_template("add-card.html")

    def start(self):
        return render_template("start-app.html")

    def get_flashcard(self):
        if len(self.questions) == 0:
            self.load_flashcards()

        flashcard1 = self.questions[random.randint(0, 2)]
        flashcard2 = random.choice(self.questions)

        flashcard = random.choice([flashcard1, flashcard2])

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
            self.data_handler.append_data(question_list, self.csv_file_path)
            self.questions.append(question_list)
            return jsonify({"success": True, "message": "Flashcard saved!"})

    def update_flashcard(self):
        question = request.form.get("question")
        time_taken = request.form.get("time")
        correctness = request.form.get("correctness")

        data = [question, time_taken, correctness]
        self.data_handler.update_flashcard(data, self.csv_file_path)

        return jsonify({"success": True, "message": "Response collected"})

    def load_flashcards(self):
        self.questions = self.data_handler.read_csv(self.csv_file_path)

if __name__ == "__main__":
    server = Backend()
    server.app.run(host="0.0.0.0", debug=False)
