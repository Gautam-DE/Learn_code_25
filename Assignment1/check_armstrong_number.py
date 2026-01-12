def calculate_armstrong_sum(number: int) -> int:
    # Initialize sum and digit count
    armstrong_sum = 0
    digit_count = 0
    
    # Calculate number of digits
    remaining_number = number
    while remaining_number > 0:
        digit_count += 1
        remaining_number = remaining_number // 10
    
    # Calculate sum of digits raised to the power of digit count
    remaining_number = number
    while remaining_number > 0:
        current_digit = remaining_number % 10
        armstrong_sum += (current_digit ** digit_count)
        remaining_number = remaining_number // 10
    
    return armstrong_sum


def main():
    input_number = int(input("\nPlease Enter the Number to Check for Armstrong: "))
    
    armstrong_sum = calculate_armstrong_sum(input_number)
    
    if input_number == armstrong_sum:
        print("\n %d is Armstrong Number.\n" % input_number)
    else:
        print("\n %d is Not an Armstrong Number.\n" % input_number)


if __name__ == "__main__":
    main()

