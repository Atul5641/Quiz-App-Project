# Importing necessary libraries
import sys
import random
import re  # For regular expressions

# Database for users
users_db = {}

# Quiz data for three subjects (including additional questions)
quizzes = {
    "DSA": [
        {"question": "What is the time complexity of binary search?", 
         "options": ["1. O(n)", "2. O(log n)", "3. O(n^2)", "4. O(1)"], 
         "answer": 2},
        {"question": "What is the time complexity of quicksort in the best case?", 
         "options": ["1. O(n)", "2. O(n log n)", "3. O(n^2)", "4. O(log n)"], 
         "answer": 2},
        {"question": "Which algorithm is used for finding the shortest path in a graph?", 
         "options": ["1. Dijkstra's Algorithm", "2. QuickSort", "3. MergeSort", "4. Binary Search"], 
         "answer": 1},
        {"question": "What does 'Big O' notation describe?", 
         "options": ["1. The space complexity of an algorithm", "2. The time complexity of an algorithm", "3. The input size of an algorithm", "4. None of the above"], 
         "answer": 2},
        {"question": "Which data structure is used in implementing a recursive function?", 
         "options": ["1. Stack", "2. Queue", "3. Array", "4. Linked List"], 
         "answer": 1},
        {"question": "Which of these is a greedy algorithm?", 
         "options": ["1. Prim's Algorithm", "2. MergeSort", "3. QuickSort", "4. Binary Search"], 
         "answer": 1},
        {"question": "What is the time complexity of inserting an element in a balanced binary search tree?", 
         "options": ["1. O(1)", "2. O(log n)", "3. O(n)", "4. O(n log n)"], 
         "answer": 2},
        {"question": "Which of the following is an example of divide and conquer?", 
         "options": ["1. MergeSort", "2. Bubble Sort", "3. Insertion Sort", "4. Linear Search"], 
         "answer": 1},
        {"question": "What is the worst-case time complexity of merge sort?", 
         "options": ["1. O(n log n)", "2. O(n^2)", "3. O(log n)", "4. O(n)"], 
         "answer": 1},
        {"question": "Which of the following is the most efficient way to search a sorted array?", 
         "options": ["1. Linear Search", "2. Binary Search", "3. Hashing", "4. Merge Sort"], 
         "answer": 2}
    ],
    "DBMS": [
        {"question": "What does SQL stand for?", 
         "options": ["1. Structured Query Language", "2. Strong Query Language", "3. Simple Query Language", "4. Secure Query Language"], 
         "answer": 1},
        {"question": "What is a foreign key in a database?", 
         "options": ["1. A key used to identify records", "2. A key that links two tables", "3. A key used for encryption", "4. A primary key"], 
         "answer": 2},
        {"question": "Which of the following is not a type of SQL join?", 
         "options": ["1. INNER JOIN", "2. LEFT JOIN", "3. RIGHT JOIN", "4. CROSS JOIN", "5. FULL JOIN", "6. DUPLICATE JOIN"], 
         "answer": 6},
        {"question": "What is normalization in databases?", 
         "options": ["1. Reducing data redundancy", "2. Increasing data redundancy", "3. Enforcing security", "4. Encrypting data"], 
         "answer": 1},
        {"question": "Which of the following is used for querying data in SQL?", 
         "options": ["1. INSERT", "2. SELECT", "3. DELETE", "4. UPDATE"], 
         "answer": 2},
        {"question": "What is the default sorting order in SQL?", 
         "options": ["1. Descending", "2. Ascending", "3. Random", "4. None"], 
         "answer": 2},
        {"question": "Which of the following is a type of SQL constraint?", 
         "options": ["1. NOT NULL", "2. UNIQUE", "3. PRIMARY KEY", "4. All of the above"], 
         "answer": 4},
        {"question": "What is a database schema?", 
         "options": ["1. A diagram representing data tables", "2. The structure of a database", "3. A set of stored procedures", "4. A backup of data"], 
         "answer": 2},
        {"question": "Which of the following is a non-relational database?", 
         "options": ["1. MySQL", "2. PostgreSQL", "3. MongoDB", "4. Oracle"], 
         "answer": 3},
        {"question": "What is ACID in DBMS?", 
         "options": ["1. A database management system", "2. A property of SQL", "3. A set of properties ensuring reliability of database transactions", "4. None of the above"], 
         "answer": 3}
    ],
    "Python": [
        {"question": "Which of the following is a mutable data type in Python?", 
         "options": ["1. Tuple", "2. List", "3. String", "4. Int"], 
         "answer": 2},
        {"question": "Which function is used to get the length of a list in Python?", 
         "options": ["1. len()", "2. length()", "3. size()", "4. count()"], 
         "answer": 1},
        {"question": "Which of these is not a valid Python data type?", 
         "options": ["1. List", "2. Dictionary", "3. Set", "4. Tuple", "5. String", "6. Array"], 
         "answer": 6},
        {"question": "What is the correct way to define a function in Python?", 
         "options": ["1. def function():", "2. function def():", "3. def function;", "4. function(): def"], 
         "answer": 1},
        {"question": "Which of the following is a Python tuple?", 
         "options": ["1. [1, 2, 3]", "2. {1, 2, 3}", "3. (1, 2, 3)", "4. 1, 2, 3"], 
         "answer": 3},
        {"question": "Which operator is used for exponentiation in Python?", 
         "options": ["1. ^", "2. **", "3. *", "4. %"], 
         "answer": 2},
        {"question": "How do you create a comment in Python?", 
         "options": ["1. //", "2. #", "3. /*", "4. --"], 
         "answer": 2},
        {"question": "Which of the following is the correct syntax to create a class in Python?", 
         "options": ["1. class MyClass:", "2. class MyClass{}:", "3. MyClass class:", "4. class MyClass[]:"], 
         "answer": 1},
        {"question": "Which function is used to convert a string to a number in Python?", 
         "options": ["1. to_int()", "2. int()", "3. number()", "4. convert()"], 
         "answer": 2},
        {"question": "What is the correct syntax to import a module in Python?", 
         "options": ["1. import module", "2. import module()", "3. include module", "4. require module"], 
         "answer": 1}
    ]
}

# Function to validate user input
def validate_input(field, value):
    if field == "username":
        if len(value) < 3 or len(value) > 20:
            return "Username must be between 3 and 20 characters long."
        if not re.match("^[A-Za-z0-9_]+$", value):
            return "Username can only contain letters, numbers, and underscores."
    elif field == "password":
        if len(value) < 6:
            return "Password must be at least 6 characters long."
        if not any(char.isdigit() for char in value):
            return "Password must contain at least one number."
        if not any(char.isalpha() for char in value):
            return "Password must contain at least one letter."
    elif field == "email":
        if not re.match(r"^[\w.-]+@[\w.-]+\.\w+$", value):
            return "Invalid email format."
    elif field == "age":
        if not value.isdigit() or int(value) <= 0:
            return "Age must be a positive number."
    elif field == "contact":
        if not value.isdigit() or len(value) != 10:
            return "Contact number must be exactly 10 digits."
    return None

# Function to register a user
def register():
    print("======================================== User Registration =========================================")

    while True:
        username = input("Enter username: ")
        error = validate_input("username", username)
        if error:
            print(error)
        elif username in users_db:
            print("Username already exists. Please try again.")
        else:
            break

    while True:
        password = input("Enter password: ")
        error = validate_input("password", password)
        if error:
            print(error)
        else:
            break

    while True:
        email = input("Enter email: ")
        error = validate_input("email", email)
        if error:
            print(error)
        else:
            break

    while True:
        age = input("Enter your age: ")
        error = validate_input("age", age)
        if error:
            print(error)
        else:
            break

    while True:
        contact_number = input("Enter your contact number: ")
        error = validate_input("contact", contact_number)
        if error:
            print(error)
        else:
            break

    # Saving user data
    users_db[username] = {
        "password": password,
        "email": email,
        "age": age,
        "contact": contact_number,
        "score": 0
    }
    print("Registration successful!\n")

# Function to login a user
def login():
    print("============================================ User Login ============================================")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in users_db and users_db[username]["password"] == password:
        print(f"Welcome back, {username}!\n")
        return username
    else:
        print("Invalid username or password. Please try again.\n")
        return None

# Function to display the quiz
def attempt_quiz(username):
    print("Select a quiz subject:")
    print("1. DSA")
    print("2. DBMS")
    print("3. Python")
    choice = input("Enter the subject number: ")

    subject = ""
    if choice == "1":
        subject = "DSA"
    elif choice == "2":
        subject = "DBMS"
    elif choice == "3":
        subject = "Python"
    else:
        print("Invalid selection. Exiting quiz.")
        return

    # Select 5 random questions from the selected subject
    selected_questions = random.sample(quizzes[subject], 5)
    score = 0
    total_questions = len(selected_questions)

    print(f"\nStarting {subject} Quiz:\n")

    # Loop through the selected questions
    for idx, question in enumerate(selected_questions):
        print(f"Question {idx + 1}: {question['question']}")
        for option in question['options']:
            print(option)
        answer = input("Enter the option number (1-4): ")

        if answer.isdigit() and int(answer) == question["answer"]:
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong. Correct answer was option {question['answer']}.\n")

    # Calculate the percentage
    percentage = (score / total_questions) * 100

    # Update the user's score
    users_db[username]["score"] += score
    print(f"Quiz finished! You scored {score}/{total_questions} in this quiz.\n")
    print(f"Your score percentage: {percentage:.2f}%\n")
    print(f"Total score: {users_db[username]['score']}\n")

# Function to show result
def show_result(username):
    score = users_db[username]['score']
    total_score_possible = len(quizzes["DSA"]) + len(quizzes["DBMS"]) + len(quizzes["Python"])  # Total questions from all subjects
    percentage = (score / total_score_possible) * 100
    print(f"\n====================================== Result for {username} =====================================")
    print(f"Your total score: {score}/{total_score_possible}")
    print(f"Your total percentage: {percentage:.2f}%\n")
    print(f"******************************** !!! THANK YOU !!! {username} *************************************\n")

# Function to display menu options
def display_menu():
    print("###################################### !!! WELCOME TO QUIZ COMPETITION !!! #################################")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")
    print("\n")
    return choice

# Main function to control the flow
def main():
    while True:
        choice = display_menu()

        if choice == "1":
            register()
        elif choice == "2":
            username = login()
            if username:
                while True:
                    print("1. Attempt Quiz")
                    print("2. Show Result")
                    print("3. Logout")
                    quiz_choice = input("Enter your choice: ")
                    print("\n")

                    if quiz_choice == "1":
                        attempt_quiz(username)
                    elif quiz_choice == "2":
                        show_result(username)
                    elif quiz_choice == "3":
                        print(f"Logging out {username}...\n")
                        break
                    else:
                        print("Invalid choice. Try again.")
        elif choice == "3":
            print("Exiting the program...")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

# Entry point of the script
if __name__ == "__main__":
    main()
