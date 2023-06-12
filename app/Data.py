import threading
import csv
import json

class DataHandler:
    lock = threading.Lock()
    max_threshold = 4
    current_threshold = 0

    @classmethod
    def settings(cls):
        with open("settings.json") as file:
            data = json.load(file)
        return data

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

