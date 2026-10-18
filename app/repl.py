from colorama import Fore, Style, init
from app.calculator import Calculator
from app.help_menu import get_help_menu



def main():
    """Run the interactive calculator."""
    init(autoreset=True, strip=False)

    calculator = Calculator()
    calculator.load_history()

    print(Fore.CYAN + "Advanced Python Calculator" + Style.RESET_ALL)
    print("Type 'help' for available commands.")

    while True:
        try:
            user_input = input("calculator> ").strip()

            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0].lower()

            if command in ("exit", "quit"):
                print(Fore.CYAN + "Goodbye!" + Style.RESET_ALL)
                break

            elif command == "help":
                print(Fore.CYAN + get_help_menu() + Style.RESET_ALL)

            elif command == "history":
                if not calculator.history:
                    print(Fore.YELLOW + "No calculation history." + Style.RESET_ALL)
                else:
                    for index, calculation in enumerate(
                        calculator.history, start=1
                    ):
                        print(
                            Fore.YELLOW
                            + f"{index}. {calculation}"
                            + Style.RESET_ALL
                        )

            elif command == "undo":
                calculator.undo()
                print(Fore.CYAN + "Last history change undone." + Style.RESET_ALL)

            elif command == "redo":
                calculator.redo()
                print(Fore.CYAN + "Last history change redone." + Style.RESET_ALL)

            elif command == "clear":
                calculator.clear()
                print(Fore.CYAN + "Calculation history cleared." + Style.RESET_ALL)

            else:
                if len(parts) != 3:
                    print(
                        Fore.RED
                        + "Invalid command. Use: "
                        + "<operation> <number1> <number2>"
                        + Style.RESET_ALL
                    )
                    continue

                operation, a, b = parts
                result = calculator.calculate(operation, a, b)

                print(Fore.GREEN + f"Result: {result}" + Style.RESET_ALL)

        except Exception as error:
            print(Fore.RED + f"Error: {error}" + Style.RESET_ALL)


if __name__ == "__main__":
    main()
