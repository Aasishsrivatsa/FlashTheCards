import atexit
import csv
import random
import threading
import json

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS


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

        atexit.register(self.shutdown)  # Register shutdown hook

    def homepage(self):
        return render_template("homepage.html")

    def add_card(self):
        return render_template("add-card.html")

    def start(self):
        return render_template("start-app.html")

    def load_flashcards(self):
        try:
            self.questions = DataHandler.read_csv(self.csv_file_path)
        except Exception as e:
            return jsonify({"success": False, "message": f"An error occurred while loading flashcards: {e}"})

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

    def shutdown(self):
        try:
            threading.Thread(target=DataHandler.sort_flashcards, args=(self.csv_file_path,)).start()
        except Exception as e:
            print(f"An error occurred while sorting flashcards: {e}")

    def run(self):
        self.app.run(host='0.0.0.0', threaded=True)


class DataHandler:
    lock = threading.Lock()
    path = 'flashcards.csv'
    max_threshold = 4
    current_threshold = 0

    @classmethod
    def sort_prioritize(cls):
        cls.current_threshold += 1
        if cls.current_threshold >= cls.max_threshold:
            cls.current_threshold = 0
            threading.Thread(target=cls.sort_flashcards, args=(cls.path,)).start()

    @classmethod
    def update_flashcard(cls, data: list, path: str) -> None:
        question = data[0]
        time_taken = data[1]
        correctness = data[2]

        updated = False
        rows = []

        try:
            with cls.lock:
                with open(path, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[0] == question:
                            row[2] = time_taken
                            row[3] = correctness

                            if str(correctness).lower() == 'false':
                                row[4] = str(int(row[4]) + 1)
                            else:
                                row[4] = '0'

                            updated = True

                        rows.append(row)

            if updated:
                with cls.lock:
                    with open(path, 'w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerows(rows)

                cls.sort_prioritize()

        except Exception as e:
            raise Exception(f"An error occurred while updating the flashcard: {e}")

    @classmethod
    def read_csv(cls, path: str) -> list:
        questions = []
        try:
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                questions = list(reader)
        except Exception as e:
            raise Exception(f"An error occurred while loading flashcards: {e}")

        return questions

    @classmethod
    def append_data(cls, data: list, path: str) -> None:
        try:
            question = data[0]
            answer = data[1]
            time_taken = data[2]
            correctness = data[3]
            number_of_times_failed = data[4]

            with cls.lock:
                with open(path, 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([question, answer, time_taken, correctness, number_of_times_failed])

        except Exception as e:
            raise Exception(f"An error occurred while saving the flashcard: {e}")

        else:
            cls.sort_prioritize()

    @classmethod
    def sort_flashcards(cls, path: str) -> None:
        try:
            questions = DataHandler.read_csv(path)

            if questions is None:
                raise Exception("Unable to load flashcards for sorting.")

            # Remove empty lines from the questions list
            questions = [question for question in questions if question]

            questions.sort(key=lambda x: (x[3] is False, -float(x[2]), int(x[4])), reverse=True)

            with cls.lock:
                with open(path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(questions)
        except IndexError:
            raise Exception("Some rows in the CSV file do not have the expected number of columns.")
        except Exception as e:
            raise Exception(f"An error occurred while sorting flashcards: {e}")


if __name__ == "__main__":
    server = Backend()
    server.run()
