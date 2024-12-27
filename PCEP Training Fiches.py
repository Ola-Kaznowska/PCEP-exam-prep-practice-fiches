import os
import time
import json
import random
from datetime import datetime, timedelta

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.flashcards = []
        self.sessions = []
        self.progress = {}

class PythonExamAssistant:
    def __init__(self):
        self.users = {}
        self.current_user = None
        self.data_file = "users_data.json"
        self.load_data()
        self.default_flashcards = [
            {"topic": "Variables", "question": "What is the correct way to declare a variable in Python?", "answer": "variable_name = value"},
            {"topic": "Data Types", "question": "What is the data type of '3.14' in Python?", "answer": "float"},
            {"topic": "Control Flow", "question": "Which keyword is used for conditional branching in Python?", "answer": "if"},
            {"topic": "Loops", "question": "Which loop is used to iterate over a sequence in Python?", "answer": "for"},
            {"topic": "Functions", "question": "How do you define a function in Python?", "answer": "def"},
            {"topic": "Modules", "question": "Which keyword is used to import a module in Python?", "answer": "import"},
            {"topic": "Exceptions", "question": "What keyword is used to handle exceptions in Python?", "answer": "try"},
            {"topic": "Lists", "question": "How do you access the first element of a list named 'my_list'?", "answer": "my_list[0]"},
            {"topic": "Dictionaries", "question": "What method is used to get all keys from a dictionary?", "answer": "keys()"},
            {"topic": "Strings", "question": "What method is used to convert a string to lowercase?", "answer": "lower()"},
            {"topic": "Sets", "question": "Which Python data type does not allow duplicate values?", "answer": "set"},
            {"topic": "Tuples", "question": "Can you modify a tuple after its creation?", "answer": "no"},
            {"topic": "File Handling", "question": "Which mode is used to open a file for writing in Python?", "answer": "w"},
            {"topic": "Boolean Logic", "question": "What is the result of True and False?", "answer": "False"},
            {"topic": "Operators", "question": "Which operator is used for exponentiation in Python?", "answer": "**"},
            {"topic": "Classes", "question": "What is the keyword used to define a class in Python?", "answer": "class"},
            {"topic": "Inheritance", "question": "Which method is used to call the parent class constructor?", "answer": "super()"},
            {"topic": "Methods", "question": "What is the first argument of instance methods in Python?", "answer": "self"},
            {"topic": "Attributes", "question": "How do you access an attribute 'x' of an object 'obj'?", "answer": "obj.x"},
            {"topic": "Global Variables", "question": "Which keyword is used to declare a global variable?", "answer": "global"},
            {"topic": "Lambda Functions", "question": "How do you define an anonymous function in Python?", "answer": "lambda"},
            {"topic": "Comprehensions", "question": "What is the syntax to create a list comprehension?", "answer": "[expression for item in iterable]"},
            {"topic": "Generators", "question": "Which keyword is used to create a generator?", "answer": "yield"},
            {"topic": "Decorators", "question": "What symbol is used to apply a decorator to a function?", "answer": "@"},
            {"topic": "Arguments", "question": "What are *args and **kwargs used for in Python functions?", "answer": "variable length arguments"},
            {"topic": "Assertions", "question": "What is the keyword used to assert a condition in Python?", "answer": "assert"},
            {"topic": "Libraries", "question": "Which library is commonly used for numerical computations in Python?", "answer": "numpy"},
            {"topic": "Environment", "question": "What command is used to install packages in Python?", "answer": "pip"},
            {"topic": "Versioning", "question": "How do you check the Python version installed?", "answer": "python --version"}
        ]

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                for username, user_data in data.items():
                    user = User(username, user_data['password'])
                    user.flashcards = user_data['flashcards']
                    user.sessions = user_data['sessions']
                    user.progress = user_data['progress']
                    self.users[username] = user

    def save_data(self):
        data = {
            user.username: {
                'password': user.password,
                'flashcards': user.flashcards,
                'sessions': user.sessions,
                'progress': user.progress
            } for user in self.users.values()
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)

    def register(self):
        username = input("Enter a username: ")
        if username in self.users:
            print("Username already exists.")
            return
        password = input("Enter a password: ")
        self.users[username] = User(username, password)
        self.save_data()
        print("Registration successful!")

    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        user = self.users.get(username)
        if user and user.password == password:
            self.current_user = user
            print(f"Welcome back, {username}!")
        else:
            print("Invalid credentials.")

    def study_flashcards(self):
        print("\nStarting Python PCEP flashcard study session!")

        flashcards = random.sample(self.default_flashcards, min(len(self.default_flashcards), 30))
        correct_answers = 0

        for flashcard in flashcards:
            print(f"\nTopic: {flashcard['topic']}")
            print(f"Question: {flashcard['question']}")
            user_answer = input("Your answer: ")

            if user_answer.strip().lower() == flashcard['answer'].strip().lower():
                print("Correct! 🎉")
                correct_answers += 1
            else:
                print(f"Incorrect. The correct answer is: {flashcard['answer']}")

        print(f"\nSession complete! You answered {correct_answers}/{len(flashcards)} correctly.")
        self.current_user.progress[datetime.now().isoformat()] = correct_answers
        self.save_data()

    def schedule_study_session(self):
        date_str = input("Enter the date for the session (YYYY-MM-DD HH:MM): ")
        try:
            session_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            self.current_user.sessions.append(session_time.isoformat())
            self.save_data()
            print(f"Study session scheduled for {session_time.strftime('%Y-%m-%d %H:%M')}!")
        except ValueError:
            print("Invalid date format.")

    def check_scheduled_sessions(self):
        now = datetime.now()
        for session_str in self.current_user.sessions:
            session_time = datetime.fromisoformat(session_str)
            if now >= session_time and now - session_time <= timedelta(minutes=30):
                print(f"Reminder: You have a study session scheduled for {session_time.strftime('%Y-%m-%d %H:%M')}!")

    def display_menu(self):
        while True:
            if not self.current_user:
                print("\n1. Register\n2. Login\n3. Exit")
                choice = input("Choose an option: ")
                if choice == '1':
                    self.register()
                elif choice == '2':
                    self.login()
                elif choice == '3':
                    break
                else:
                    print("Invalid option.")
            else:
                self.check_scheduled_sessions()
                print("\n1. Study Python PCEP Flashcards\n2. Schedule Study Session\n3. Logout\n4. Exit")
                choice = input("Choose an option: ")
                if choice == '1':
                    self.study_flashcards()
                elif choice == '2':
                    self.schedule_study_session()
                elif choice == '3':
                    self.current_user = None
                elif choice == '4':
                    self.save_data()
                    break
                else:
                    print("Invalid option.")

if __name__ == "__main__":
    assistant = PythonExamAssistant()
    assistant.display_menu()
