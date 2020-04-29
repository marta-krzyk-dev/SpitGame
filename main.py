from Project4_Split.SpitGame import SpitGame

game = SpitGame()
game.PrintTitle()
game.CreatePlayers()

while True:
    game.PlayRound()
    game.PrintScores()
