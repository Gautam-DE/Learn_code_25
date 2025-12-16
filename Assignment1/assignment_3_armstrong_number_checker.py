def calculate_armstrong_sum(number: int) -> int:
    # Initialize sum and digit count
    sum_of_powers = 0
    digit_count = 0
    
    # Calculate number of digits
    temp_number = number
    while temp_number > 0:
        digit_count += 1
        temp_number = temp_number // 10
    
    # Calculate sum of digits raised to the power of digit count
    temp_number = number
    while temp_number > 0:
        current_digit = temp_number % 10
        sum_of_powers += (current_digit ** digit_count)
        temp_number = temp_number // 10
    
    return sum_of_powers


def main():
    input_number = int(input("\nPlease Enter the Number to Check for Armstrong: "))
    
    armstrong_sum = calculate_armstrong_sum(input_number)
    
    if input_number == armstrong_sum:
        print("\n %d is Armstrong Number.\n" % input_number)
    else:
        print("\n %d is Not an Armstrong Number.\n" % input_number)


if __name__ == "__main__":
    main()

