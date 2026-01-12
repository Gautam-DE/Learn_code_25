import random

def roll_dice(number_of_sides: int) -> int:
    dice_roll = random.randint(1, number_of_sides)
    return dice_roll

def main():
    number_of_sides = 6
    is_playing = True
    
    while is_playing:
        user_input = input("Ready to roll? Enter Q to Quit: ")
        
        if user_input.lower() != "q":
            roll_result = roll_dice(number_of_sides)
            print("You have rolled a", roll_result)
        else:
            is_playing = False


if __name__ == "__main__":
    main()

