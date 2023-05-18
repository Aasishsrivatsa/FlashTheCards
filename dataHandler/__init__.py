import csv
from flask import jsonify

class DataHandler:
    def __init__(self) -> None:
        self.csv_file_path = 'flashcards.csv'

    @staticmethod
    def read_csv(path):
        try:
            with open(path, 'r') as file:
                reader = csv.reader(file)
                questions = list(reader)
        except Exception as e:
            # Handle the exception, e.g., print an error message or log the exception
            print(f"An error occurred while loading flashcards: {e}")
        finally:
            return questions
    
    def append_data(self, data):
        try:
            self.question = data[0]
            self.answer = data[1]
            self.time_taken = data[2]
            self.correctness = data[3]
            self.number_of_times_failed = data[4]

            # Save the data to the CSV file

            with open(self.csv_file_path, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([self.question, self.answer, self.time_taken, self.correctness, self.number_of_times_failed])

        except Exception as e:

            # Handle the exception, e.g., print an error message or log the exception
            print(f"An error occurred while saving the flashcard: {e}")
            return jsonify({"success": False})
