from termcolor import colored, COLORS

class ConsoleInputOutputManipulator:
    def __init__(self, font_color="white"):
        self.font_color = font_color if font_color in COLORS.keys() else "white"

    def Print(self, text):
        if not isinstance(text,str):
            return

        print(colored(text, self.font_color, attrs=["bold"]))

    def PrintOnBackground(self, text):
        if not isinstance(text, str):
            return

        print(colored(text, self.font_color, attrs=["bold", "reverse"]))

    def PrintInstructions(self):
        # self.ClearScreen()

        with open("spit_instructions.txt", "r") as file:
            print(file.read())

    def GetInput(self, text):
        answer = input(text).strip()
        trimmed_answer = answer.replace(" ", "").lower()  # Remove whitespaces

        if trimmed_answer == "--help":
            self.PrintInstructions()
            self.GetInput(input(">> "))
        elif trimmed_answer == "--resume":
            pass
            # self.Play()  # Reprint game
        elif trimmed_answer.startswith("--"):
            print("Available commands:")
            print("--help       Print instructions")
            print("--resume     Resumes the game")

        return answer

    def PrintParagraphs(self, paragraphDict):
        if False == isinstance(paragraphDict, dict):
            return

        for p in paragraphDict:
            print(colored(f"\n\n*** {p} ***\n\n", "blue", attrs=['bold']))

            print(colored(paragraphDict[p], "white", attrs=['bold']))

    def IsCommand(self, input):
        input = input.replace(" ", "").lower()
        return input == "--help" or input == "--resume"

    def Command(self, input):
        if False == input is str:
            raise TypeError

        answer = input.replace(" ", "").lower()  # Remove whitespaces

        if answer == "--help":
            self.PrintInstructions()
        elif answer == "--resume":
            return
        else:
            print("Available commands:")
            print("--help       Print instructions")
            print("--resume     Resumes the game")

        return answer
