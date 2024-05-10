import tkinter as tk
import random
from tkinter import messagebox

game_window = None  # Define game_window as a global variable
incorrect_guesses = 0 # Track the number of incorrect guesses
MAX_INCORRECT_GUESSES = 3  # Define the maximum number of incorrect guesses allowed

# Function to read statements from a file and store them in a dictionary
def total_statements():
    statements = {}
    with open('C:/Users/mgarc/Desktop/bcog200/cryptogram_game/data/statements.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            print("Parts:", parts)  # Debug print
            if len(parts) == 2:
                statement_key = parts[0].strip()
                statement_parts = parts[1].strip().split(',')
                print("Statement parts:", statement_parts)  # Debug print
                statement_text = statement_parts[0].strip()
                provided_letters = {}
                for pair in statement_parts[1:]:
                    letter, number = pair.strip().split()
                    print("Letter:", letter, "Number:", number)  # Debug print
                    provided_letters[letter.strip()] = number.strip()
                statements[statement_key] = {'statement': statement_text, 'provided_letters': provided_letters}
    return statements

# Function to choose a statement and determine provided letters
def choose_statement():
    statements = total_statements()
    statement_key = random.choice(list(statements.keys()))
    statement_data = statements[statement_key]
    print("Chosen statement:", statement_key)  # Debugging line
    print("Statement data:", statement_data)   # Debugging line
    return statement_data['statement'], statement_data['provided_letters']

# Function to handle letter guess
def guess_letter(guess, statement, provided_letters):
    guess = guess.lower()  # Convert guess to lowercase for case-insensitive comparison
    print("Guess:", guess)
    print("Provided letters:", provided_letters)
    
    found = False  # Flag to indicate if the guess is found in the statement
    for index, char in enumerate(statement):
        if char.isalpha() and char.lower() == guess:  # Check if the character is a letter and matches the guess
            found = True
            provided_letters[char.lower()] = char.upper()  # Update the provided letters dictionary
            break  # Exit loop once the guess is found
    
    if found:
        return f"Correct guess! {guess.upper()}", provided_letters
    else:
        return "Incorrect guess.", provided_letters

# Function to display the cryptogram puzzle
def display_cryptogram(statement, provided_letters):
    displayed_statement = ""
    legend = "Legend/Key:\n"
    guessed_letters = {}
    
    for char in statement:
        if char.isalpha():
            char_lower = char.lower()
            if char_lower in provided_letters:
                displayed_statement += provided_letters[char_lower] + ' '
                guessed_letters[char_lower] = provided_letters[char_lower]
            else:
                if char_lower not in guessed_letters:
                    number = str(random.randint(1, 50))
                    guessed_letters[char_lower] = number
                displayed_statement += guessed_letters[char_lower] + ' '
        else:
            displayed_statement += char + ' '
    
    # Construct the legend from the guessed letters dictionary
    for letter, number in guessed_letters.items():
        legend += f"{letter.upper()} -> {number}\n"

    return displayed_statement.strip(), legend


# Function to start the game
def start_game(root):
    global game_window, incorrect_guesses, provided_letters, statement  # Declare statement as a global variable
    incorrect_guesses = 0 # Reset incorrect_guesses counter
    statement, provided_letters = choose_statement()
    print("Original statement:", statement)
    print("Provided letters:", provided_letters)
    print("Cryptogram puzzle:", display_cryptogram(statement, provided_letters))

    # Function to handle the user's guess
    def handle_guess():
        global provided_letters, statement, incorrect_guesses  # Access the global statement variable
        guess = guess_entry.get().lower()
        result = guess_letter(guess, statement, provided_letters)
        print(result)
        if "Incorrect guess" in result:
            incorrect_guesses += 1
            if incorrect_guesses >= MAX_INCORRECT_GUESSES:
                print("Maximum mistakes reached. Starting new game.")
                game_window.destroy()
                start_game(root)
            else:
                guess_entry.delete(0, tk.END)
        else:
            provided_letters.update(result[1])
            puzzle_text, _ = display_cryptogram(statement, provided_letters)
            puzzle_label.config(text=puzzle_text)
            # Clear the guess entry
            guess_entry.delete(0, tk.END)

    # Create a Tkinter window
    game_window = tk.Toplevel(root)
    game_window.title("Cryptogram Game")

    # Display the cryptogram puzzle
    puzzle_text, legend_text = display_cryptogram(statement, provided_letters)
    puzzle_label = tk.Label(game_window, text=puzzle_text)
    puzzle_label.pack()

    legend_label = tk.Label(game_window, text=legend_text)
    legend_label.pack()

    # Entry widget for the user's guess
    guess_entry = tk.Entry(game_window)
    guess_entry.pack()

    # Button to submit the guess
    guess_button = tk.Button(game_window, text="Guess", command=handle_guess)
    guess_button.pack()


def main():
    root = tk.Tk()
    root.title("Cryptogram Game")
    root.geometry("600x400")

    with open('C:/Users/mgarc/Desktop/bcog200/cryptogram_game/data/cryptogram_instructions.txt', 'r') as instructions_file:
        instructions = instructions_file.read()
    
    instructions_label = tk.Label(root, text=instructions)
    instructions_label.pack()

    start_button = tk.Button(root, text="Start", command=lambda: start_game(root))
    start_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()