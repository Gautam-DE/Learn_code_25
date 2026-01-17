import random


def is_valid_guess(guess_input: str) -> bool:
    return guess_input.isdigit() and 1 <= int(guess_input) <= 100


def prompt_and_validate_guess() -> int:
    guess = input("Guess a number between 1 and 100:")
    while not is_valid_guess(guess):
        guess = input("I won't count this one Please enter a number between 1 to 100:")
    return int(guess)


def play() -> None:
    secret_number = random.randint(1, 100)
    guess_count = 0
    while True:
        guess = prompt_and_validate_guess()
        guess_count += 1
        if guess < secret_number:
            print("Too low. Guess again")
        elif guess > secret_number:
            print("Too High. Guess again")
        else:
            print("You guessed it in", guess_count, "guesses!")
            break


if __name__ == "__main__":
    play()

