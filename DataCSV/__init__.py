import csv
import asyncio
from threading import Lock
from flask import jsonify

class DataHandler:
    def __init__(self):
        self.lock = Lock()

    async def update_flashcard(self, data: list, path: str) -> bool:
        question = data[0]
        time_taken = data[1]
        correctness = data[2]

        updated = False
        rows = []
        try:
            async with self.lock:
                with open(path, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[0] == question:
                            # Update the flashcard fields for the matching question
                            row[2] = time_taken
                            row[3] = correctness

                            if str(correctness).lower() == 'false':
                                row[4] = str(int(row[4]) + 1)
                            else:
                                row[4] = '0'

                            updated = True
                        rows.append(row)

                if updated:
                    with open(path, 'w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerows(rows)

            await asyncio.sleep(0)  # Allow other coroutines to run

            await self.sort_flashcards(path)

            return updated

        except Exception as e:
            # Handle the exception, e.g., print an error message or log the exception
            print(f"An error occurred while updating the flashcard: {e}")

            return updated

    async def read_csv(self, path: str) -> list:
        questions = []
        try:
            async with self.lock:
                with open(path, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    questions = list(reader)
        except Exception as e:
            # Handle the exception, e.g., print an error message or log the exception
            print(f"An error occurred while loading flashcards: {e}")

        return questions

    async def append_data(self, data: list, path: str) -> None:
        try:
            question = data[0]
            answer = data[1]
            time_taken = data[2]
            correctness = data[3]
            number_of_times_failed = data[4]

            # Save the data to the CSV file
            async with self.lock:
                with open(path, 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([question, answer, time_taken, correctness, number_of_times_failed])

        except Exception as e:
            # Handle the exception, e.g., print an error message or log the exception
            print(f"An error occurred while saving the flashcard: {e}")
            return jsonify({"success": False})

    async def sort_flashcards(self, path: str) -> None:
        try:
            questions = await self.read_csv(path)

            if questions is None:
                print("Unable to load flashcards for sorting.")
                return

            questions.sort(key=lambda x: (x[3] is False, -float(x[2]), int(x[4])), reverse=True)

            async with self.lock:
                with open(path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(questions)
        except IndexError:
            print("Some rows in the CSV file do not have the expected number of columns.")
        except Exception as e:
            print(f"An error occurred while sorting flashcards: {e}")
