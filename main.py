from Project4_Split.SpitGame import SpitGame

game = SpitGame()
game.PrintTitle()
game.CreatePlayers(ask_for_names=True)

while True:
    game.PlayGame()
    game.GetInput("Click enter to have another game...")
    game.PrintTitle()
