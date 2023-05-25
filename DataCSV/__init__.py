import csv
import asyncio
from asyncio import Lock
from flask import jsonify

class DataHandler:
    def __init__(self):
        self.lock = Lock()
        self.counter = 0
        self.threshold = 3

    async def update_flashcard(self, data: list, path: str) -> bool:
        question = data[0]
        time_taken = data[1]
        correctness = data[2]

        updated = False
        rows = []
        try:
            async with self.lock:
                rows = await self.read_csv(path)
                for i, row in enumerate(rows):
                    if row[0] == question:
                        # Update the flashcard fields for the matching question
                        rows[i][2] = time_taken
                        rows[i][3] = correctness

                        if str(correctness).lower() == 'false':
                            rows[i][4] = str(int(rows[i][4]) + 1)
                        else:
                            rows[i][4] = '0'

                        updated = True

                if updated:
                    await self.write_csv(path, rows)

            await asyncio.sleep(0)  # Allow other coroutines to run

            self.counter += 1

            if self.counter >= self.threshold:
                await self.sort_flashcards(path)
                self.counter = 0

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
                    questions = [row for row in reader]

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

            self.counter += 1

            if self.counter >= self.threshold:
                await self.sort_flashcards(path)
                self.counter = 0

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
                await self.write_csv(path, questions)
        except IndexError:
            print("Some rows in the CSV file do not have the expected number of columns.")
        except Exception as e:
            print(f"An error occurred while sorting flashcards: {e}")

    @staticmethod
    async def write_csv(path: str, questions: list) -> None:
        with open(path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(questions)
