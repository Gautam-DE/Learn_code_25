import random

def roll_dice(max_sides: int) -> int:
    dice_roll = random.randint(1, max_sides)
    return dice_roll

def main():
    max_sides = 6
    is_playing = True
    
    while is_playing:
        user_input = input("Ready to roll? Enter Q to Quit: ")
        
        if user_input.lower() != "q":
            roll_result = roll_dice(max_sides)
            print("You have rolled a", roll_result)
        else:
            is_playing = False


if __name__ == "__main__":
    main()

