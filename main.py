import math
import sys
import random
import mysql.connector
import pycountry

# Establish database connection
conn = mysql.connector.connect(
    host='127.0.0.1',
    port='3306',
    database='flight_game',
    user='root',
    password='12345',
    autocommit=True
)

# Functions related to database operations
def lento_kenta():
    sql = ("SELECT iso_country, ident, NAME, latitude_deg, longitude_deg FROM airport WHERE iso_country IN ('FI','SE', 'IT,DE,FR,AT')")
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def airport_info(icao):
    sql = f"SELECT iso_country, ident, NAME, latitude_deg, longitude_deg FROM airport WHERE ident = '{icao}' LIMIT 1"
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        country_name = conn.get_country(result[0])  # Assuming you have a function to get country name
        return (result[1], result[2], result[3], result[4], country_name)
    else:
        return None

def country_answer(name):
    sql = f"SELECT option_1, option_2, option_3, option_4 FROM answer WHERE name = '{name}'"
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        return result
    else:
        return None

def correct_option(answer):
    sql = f"SELECT correct_option FROM answer WHERE name = '{answer}'"
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        country_name = result[0]
        return country_name
    else:
        return None

# Function to ask the player if they want to play
def ask_to_play():
    while True:
        answer = input("Do you want to play? (yes/no): ").lower()
        if answer == "yes":
            return True
        elif answer == "no":
            return False
        else:
            print("Please enter either 'yes' or 'no'.")

# Function to check if the length of a name is valid
def name_length(name):
    if len(name) < 5 or len(name) > 10:
        return False
    else:
        return True

# Function to choose a random airport
def choose_random_airport():
    airports = lento_kenta()
    if airports:
        return random.choice(airports)
    else:
        return None

# Function to ask the player if they want to play with a randomly chosen airport
def ask_to_play_with_random_airport():
    random_airport = choose_random_airport()
    if random_airport:
        print("Your random airport:")
        print("Country:", random_airport[0])
        print("Ident:", random_airport[1])
        print("Name:", random_airport[2])
        print("Latitude:", random_airport[3])
        print("Longitude:", random_airport[4])

        while True:
            answer = input("Do you want to play with this airport? (yes/no): ").lower()
            if answer == "yes":
                return True, random_airport
            elif answer == "no":
                return False, None
            else:
                print("Please enter either 'yes' or 'no'.")
    else:
        print("No airports available.")
        return False, None

# Start of the game
if ask_to_play():
    print("Great! Let's start play!")

    # Player's name input
    name = input("Give your name: ")
    if name_length(name):
        print("Welcome to the game, " + name + "!")
    else:
        print("Okay, see you next time!")
        sys.exit()

    # Asking to play with a random airport
    play, random_airport = ask_to_play_with_random_airport()

    if play:
        print("Great! Let's start play!")

        # Define a dictionary of questions for each country
        country_questions = {
            'FI': ["What is the capital of Finland?"],
            'SE': ["Where is Sweden located?"],
            'IT': ["What is the capital of Italy?"],
            'AT':["What is the language of Austria?"]
            # Add more countries and their respective questions as needed
        }

        # Function to get a question for a given country
        def get_question_for_country(country_name):
            if country_name in country_questions:
                questions = country_questions[country_name]
                return random.choice(questions)
            else:
                return None

        # Function to get a question for a random country
        def get_question_for_random_country():
            random_country = random.choice(list(country_questions.keys()))
            return get_question_for_country(random_country)

        # Example usage
        if random_airport[0] in country_questions:
            question = get_question_for_country(random_airport[0])
            if question:
                print("Question for the selected country:")
            else:
                print("No question found for the selected country.")
        else:
            print("No questions available for the selected country.")

        option = country_answer(random_airport[0])  # Assuming random_airport[0] is the country ISO code

        # Function to ask a question and check the answer
        def ask_question_and_check_answer(question, options):
            print(question)
            for idx, opt in enumerate(options, start=1):
                print(f"Option {idx}: {opt}")

            # Get player's answer
            player_answer = input("Your answer (enter the option answer): ")

            # Assuming the correct answer is stored as 'correct_option' in the database
            correct_opt = correct_option(random_airport[0])

            # Check if the player's answer matches the correct option
            if player_answer == correct_opt:
                print("Correct! You get 5 points!")
            else:
                print("Incorrect.")

            return ask_to_continue()

        # Function to ask if the player wants to continue playing
        def ask_to_continue():
            while True:
                answer = input("Do you want to continue playing? (yes/no): ").lower()
                if answer == "yes":
                    return True
                elif answer == "no":
                    return False
                else:
                    print("Please enter either 'yes' or 'no'.")

        while True:
            if question:
                continue_playing = ask_question_and_check_answer(question, option)
                if continue_playing:
                    random_airport = choose_random_airport()
                    if random_airport:
                        print("Your new random airport:")
                        print("Country:", random_airport[0])
                        print("Ident:", random_airport[1])
                        print("Name:", random_airport[2])
                        print("Latitude:", random_airport[3])
                        print("Longitude:", random_airport[4])

                        question = get_question_for_country(random_airport[0])
                        option = country_answer(random_airport[0])  # Assuming this retrieves options for the question
                    else:
                        print("No more airports available.")
                        break
                else:
                    print("Okay, see you next time!")
                    break
            else:
                print("No question found for the selected country.")
                break
else:
    print("Okay, see you next time!")
