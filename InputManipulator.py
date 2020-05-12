from termcolor import colored, COLORS
from os import system, get_terminal_size
from Project4_Split.instructions import getInstructions


class InputManipulator:
    def __init__(self, font_color="white"):
        self.font_color = font_color if font_color in COLORS.keys() else "white"
        try:
            self.console_width = get_terminal_size().columns
        except OSError:
            self.console_width = 40

    def ClearConsole(self):
        system('cls')

    # region Helper print methods
    def PrintInstructions(self):
        self.PrintParagraphs(getInstructions())

    def PrintCommands(self):
        print("Available commands:")
        print("--help       Print instructions")
        print("--resume     Resume the game")
    # endregion

    # region Input methods
        #TODO REmove
    def IsCommand(self, input):
        input = input.replace(" ", "").lower()
        return input == "--help" or input == "--resume"

    def GetInput(self, message="", allowed_answers=[], not_allowed_answer_message=""):

        allowed_answers = [str(x).lower() for x in allowed_answers]

        while True:
            answer = input(colored(message, self.font_color, attrs=["bold", "reverse"]))  # Remove whitespaces
            formatted_answer = answer.replace(" ", "").lower()

            if formatted_answer in allowed_answers:
                return answer
            elif formatted_answer == "--help":
                self.PrintInstructions()
                while True:
                    answer_ = input(colored("Type --resume to get back to the game", self.font_color, attrs=["bold", "reverse"])).replace(" ", "").lower()
                    if answer_ == '--resume':
                        break
                    elif answer_ == '--help':
                        self.PrintInstructions()
                    else:
                        self.PrintCommands()
            elif formatted_answer == "--resume":
                continue
            elif formatted_answer.startswith("--"):
                self.PrintCommands()
            elif allowed_answers and not_allowed_answer_message:
                print(not_allowed_answer_message)
            elif not allowed_answers:
                return answer

    def Command(self, input):
        if False == (input is str):
            raise TypeError

        answer = input.replace(" ", "").lower()  # Remove whitespaces

        if answer == "--help":
            self.PrintInstructions()
        elif answer == "--resume":
            return
        else:
            self.PrintCommands()

        return answer
    # endregion