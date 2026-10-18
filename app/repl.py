
from app.calculator import Calculator


def main():
    """Run the interactive calculator."""
    calculator = Calculator()
    calculator.load_history()

    print("Advanced Python Calculator")
    print("Type 'help' for available commands.")

    while True:
        try:
            user_input = input("calculator> ").strip()

            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0].lower()

            if command in ("exit", "quit"):
                print("Goodbye!")
                break

            elif command == "help":
                print(
                    "Operations: add, subtract, multiply, divide, "
                    "power, root, modulus, int_divide, percent, abs_diff"
                )
                print(
                    "Usage: <operation> <number1> <number2>"
                )
                print(
                    "Commands: help, history, undo, redo, clear, exit"
                )

            elif command == "history":
                if not calculator.history:
                    print("No calculation history.")
                else:
                    for index, calculation in enumerate(
                        calculator.history, start=1
                    ):
                        print(f"{index}. {calculation}")

            elif command == "undo":
                calculator.undo()
                print("Last history change undone.")

            elif command == "redo":
                calculator.redo()
                print("Last history change redone.")

            elif command == "clear":
                calculator.clear()
                print("Calculation history cleared.")

            else:
                if len(parts) != 3:
                    print(
                        "Invalid command. Use: "
                        "<operation> <number1> <number2>"
                    )
                    continue

                operation, a, b = parts
                result = calculator.calculate(operation, a, b)
                print(f"Result: {result}")

        except Exception as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
