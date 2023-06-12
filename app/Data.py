import os
import json
import csv



class DataHandler:
    def __init__(self, path: str):
        self.max_threshold = 4
        self.current_threshold = 0
        self.path = os.path.join(os.path.dirname(__file__), path)

    def load_setting(self):
        json_path = os.path.join(os.path.dirname(__file__), "settings.json")
        with open(json_path) as file:
            setting = json.load(file)
        return setting

    def sort_prioritize(self):
        self.current_threshold += 1
        if self.current_threshold >= self.max_threshold:
            self.current_threshold = 0
            self.sort_flashcards(self.path)

    def update_flashcard(self, data: list) -> None:
        question = data[0]
        time_taken = data[1]
        correctness = data[2]

        updated = False
        rows = []

        try:
            with open(self.path, 'r', encoding='utf-8') as file:
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
                with open(self.path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)

                self.sort_prioritize()

        except Exception as e:
            print(f"An error occurred while updating the flashcard: {e}")

    def read_csv(self) -> list:
        questions = []
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                questions = list(reader)
        except Exception as e:
            print(f"An error occurred while loading flashcards: {e}")

        return questions

    def append_data(self, data: list) -> None:
        try:
            question = data[0]
            answer = data[1]
            time_taken = data[2]
            correctness = data[3]
            number_of_times_failed = data[4]

            with open(self.path, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([question, answer, time_taken, correctness, number_of_times_failed])

        except Exception as e:
            print(f"An error occurred while saving the flashcard: {e}")
        else:
            self.sort_prioritize()

    def sort_flashcards(self) -> None:
        try:
            questions = self.read_csv()

            if questions is None:
                print("Unable to load flashcards for sorting.")

            # Remove empty lines from the questions list
            questions = [question for question in questions if question]

            questions.sort(key=lambda x: (x[3] is False, -float(x[2]), int(x[4])), reverse=True)

            with open(self.path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(questions)

        except IndexError:
            print("Some rows in the CSV file do not have the expected number of columns.")
        
        except Exception as e:
            print(f"An error occurred while sorting flashcards: {e}")
