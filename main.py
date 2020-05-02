from Project4_Split.SpitGame import SpitGame

game = SpitGame()
game.PrintTitle()

game.CreatePlayers(ask_for_names=False)

while True:
    game.PlayGame()
    game.PrintTitle()
