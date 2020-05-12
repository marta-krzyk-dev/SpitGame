# Spit Game
Spit card console game in Python. This project is made for [Pirple's Python course](https://www.pirple.com/courses/python-is-easy)

[How to play Spit?](https://www.youtube.com/watch?v=yv7k6XYzgSo&t=32s)

![](https://github.com/marta-krzyk-dev/SpitGame/blob/master/Gameplay_GIF.gif?raw=true)

# Features:
- Command **--help** print the game's instructions (at any point of the game)
- Command **--resume** resumes the game
- The game asks 2 players for their names (name can consist of any characters, at least 1 character)
- Player's name is shortened to 15 characters
- Save score between rounds
- User can choose to move a stack a duplicated card with 'y' , 'n'
- Option to redraw game when resuming game
- Ask player to stack duplicates only once (per new duplicate)

# Gameplay:
- Player can choose the card to be added to spit pile
- If card is repeated in their piles, the duplicate will be placed on the leftmost pile
- If the chosen cad can be put into 2 spit piles, the leftmost spit is chosen
- If the player cannot move a card, they lose their turn
- If both players cannot move a card, they both put any card to their spit piles
- If player has an empty pile, a card from right-most pile is moved to reveal another card. This is repeated till there are empty spots
- Player can choose a card to be moved onto an empty spot
