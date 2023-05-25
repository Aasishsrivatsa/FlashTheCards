import csv
from flask import jsonify

class DataHandler:

    @staticmethod
    def update_flashcard(data:list, path:str) -> bool:
        question = data[0]
        time_taken = data[1]
        correctness = data[2]

        updated = False
        rows = []
        try:
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

                # Sort the flashcards using a separate thread
                threading.Thread(target=DataHandler.sort_flashcards, args=(path,)).start()

            return updated

        except Exception as e:
            # Handle the exception, e.g., print an error message or log the exception
            print(f"An error occurred while updating the flashcard: {e}")

            return updated
        
        DataHandler.sort_flashcards(path)

    @staticmethod
    def read_csv(path:str) -> list:
        questions = []
        try:
            with open(path, 'r', encoding = 'utf-8') as file:
                reader = csv.reader(file)
                questions = list(reader)
        except Exception as e:
            # Handle the exception, e.g., print an error message or log the exception
            print(f"An error occurred while loading flashcards: {e}")

        return questions

        DataHandler.sort_flashcards(path)
    
    @staticmethod
    def append_data(data:list ,path:str) -> None:
        try:
            question = data[0]
            answer = data[1]
            time_taken = data[2]
            correctness = data[3]
            number_of_times_failed = data[4]

            # Save the data to the CSV file

            with open(path, 'a', newline='', encoding = 'utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([question, answer, time_taken, correctness, number_of_times_failed])

        except Exception as e:

            # Handle the exception, e.g., print an error message or log the exception
            print(f"An error occurred while saving the flashcard: {e}")
            return jsonify({"success": False})
        
        DataHandler.sort_flashcards(path)

    @staticmethod
    def sort_flashcards(path:str) -> None:
        try:
            questions = DataHandler.read_csv(path)

            if questions is None:
                print("Unable to load flashcards for sorting.")
                return

            questions.sort(key=lambda x: (x[3] is False, -float(x[2]), int(x[4])), reverse=True)

            with open(path, 'w', newline='',encoding = 'utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(questions)
        except IndexError:
            print("Some rows in the CSV file do not have the expected number of columns.")
        except Exception as e:
            print(f"An error occurred while sorting flashcards: {e}")
