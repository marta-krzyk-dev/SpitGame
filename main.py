<<<<<<< HEAD
from Project4_Split.SpitGame import SpitGame

game = SpitGame()
game.PrintTitle()
game.CreatePlayers()

while True:
    game.PlayRound()
    game.PrintScores()
=======
from Project4_Split.SpitGame import SpitGame


game = SpitGame()
game.PrintTitle()
game.CreatePlayers()

result = game.Play()
#game.PrintResult()
# play again with same players
# save score
#while True:
#   input = input()
#  Command(input())
>>>>>>> a8b2937820a192227135ebe91399e7f31b4c7084
