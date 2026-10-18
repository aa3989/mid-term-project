from colorama import Fore, Style, init
from app.calculator import Calculator
from app.help_menu import get_help_menu
from app.commands import CalculationCommand, CommandQueue


def main():
    """Run the interactive calculator."""
    init(autoreset=True, strip=False)

    calculator = Calculator()
    calculator.load_history()
    command_queue = CommandQueue()

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
                
            elif command == "queue":
                if len(parts) != 4:
                    print(
                        Fore.RED
                        + "Invalid queue command. Use: "
                        + "queue <operation> <number1> <number2>"
                        + Style.RESET_ALL
                    )
                    continue

                _, operation, a, b = parts

                calculation_command = CalculationCommand(
                    calculator, operation, a, b
                )

                command_queue.add_command(calculation_command)

                print(
                    Fore.CYAN
                    + f"Queued: {operation} {a} {b}"
                    + Style.RESET_ALL
                )

            elif command == "run":
                if len(command_queue) == 0:
                    print(
                        Fore.YELLOW
                        + "No queued calculations."
                        + Style.RESET_ALL
                    )
                    continue

                results = command_queue.execute_all()

                for result in results:
                    print(
                        Fore.GREEN
                        + f"Result: {result}"
                        + Style.RESET_ALL
                    )
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
