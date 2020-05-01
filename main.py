from Project4_Split.SpitGame import SpitGame

game = SpitGame()
game.PrintTitle()

game.CreatePlayers(use_defaults=True)

while True:
    game.PlayRound()
    game.PrintScores()
