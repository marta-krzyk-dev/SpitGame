def PrintGameInstructions():
    pass


while True:
    answer = input("")

    if answer.startswith("--"):
        answer = answer[2:].strip() # Remove -- from the beginning of the string

        if answer is "help":
            PrintGameInstructions()

        elif answer is "resume":
            game.Play() # Reprint game
