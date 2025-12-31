import random


def is_valid_guess(guess_input_string: str) -> bool:
    return guess_input_string.isdigit() and 1 <= int(guess_input_string) <= 100


def prompt_and_validate_guess() -> int:
    guess = input("Guess a number between 1 and 100:")
    while not is_valid_guess(guess):
        guess = input("I wont count this one Please enter a number between 1 to 100:")
    return int(guess)


def play() -> None:
    secret_number = random.randint(1, 100)
    attempt_count = 0
    while True:
        guess = prompt_and_validate_guess()
        attempt_count += 1
        if guess < secret_number:
            print("Too low. Guess again")
        elif guess > secret_number:
            print("Too High. Guess again")
        else:
            print("You guessed it in", attempt_count, "guesses!")
            break


if __name__ == "__main__":
    play()

