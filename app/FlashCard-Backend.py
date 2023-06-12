import atexit
import csv
import random
import threading
import json

from Data import DataHandler

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

class Server:
    def __init__(self,) -> None:

        self.settings = DataHandler.settings()
        self.questions = []
        self.load_flashcards()

        atexit.register(self.shutdown)  # Register shutdown hook


    def homepage(self):
        return render_template("homepage.html")

    def add_card(self):
        return render_template("add-card.html")

    def start(self):
        return render_template("start-app.html")

    def run(self):
        self.app = Flask(__name__)
        CORS(self.app)

        self.app.route('/')(self.homepage)
        self.app.route('/add-card')(self.add_card)
        self.app.route('/start-app')(self.start)
        self.app.route('/flashcard', methods=['GET'])(self.get_flashcard)
        self.app.route('/save_flashcard', methods=['POST'])(self.save_flashcard)
        self.app.route('/update_flashcard', methods=['POST'])(self.update_flashcard)

        self.app.run(host=self.settings["ip"], threaded=True)



class Backend:
    def load_flashcards(self):
        try:
            self.questions = DataHandler.read_csv(self.csv_file_path)
        except Exception as e:
            return jsonify({"success": False, "message": f"An error occurred while loading flashcards: {e}"})
        
    def shutdown(self):
        try:
            threading.Thread(target=DataHandler.sort_flashcards, args=(self.csv_file_path,)).start()
        except Exception as e:
            print(f"An error occurred while sorting flashcards: {e}")
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
            try:
                threading.Thread(target=DataHandler.append_data, args=(question_list, self.csv_file_path)).start()
                self.questions.append(question_list)
                return jsonify({"success": True, "message": "Flashcard saved!"})
            except Exception as e:
                return jsonify({"success": False, "message": f"An error occurred while saving the flashcard: {e}"})

    def update_flashcard(self):
        question = request.form.get("question")
        time_taken = request.form.get("time")
        correctness = request.form.get("correctness")

        data = [question, time_taken, correctness]

        try:
            threading.Thread(target=DataHandler.update_flashcard, args=(data, self.csv_file_path)).start()

            return jsonify({"success": True, "message": "Response collected"})
        except Exception as e:
            return jsonify({"success": False, "message": f"An error occurred while updating the flashcard: {e}"})

    def get_flashcard(self):
        if len(self.questions) == 0:
            try:
                self.load_flashcards()
            except Exception as e:
                return jsonify({"success": False, "message": f"An error occurred while loading flashcards: {e}"})

        flashcard1 = self.questions[random.randint(0, 2)]
        flashcard2 = random.choice(self.questions)

        flashcard = random.choice([flashcard1, flashcard2])

        response = {
            'question': flashcard[0],
            'answer': flashcard[1]
        }
        return jsonify(response)

if __name__ == "__main__":
    server = Server()
    server.run()
