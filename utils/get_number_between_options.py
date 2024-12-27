def get_number(prompt: str, options_number: int) -> int:
    while True:
        user_input = input(prompt).strip()
        if user_input.isdigit() and int(user_input) <= options_number:
            return int(user_input)
        else:
            print("Invalid input. Please enter a valid number")
