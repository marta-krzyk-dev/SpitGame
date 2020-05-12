# Spit Game
Spit card console game in Python. This project is made for [Pirple's Python course](https://www.pirple.com/courses/python-is-easy)

[How to play Spit?](https://www.youtube.com/watch?v=yv7k6XYzgSo&t=32s)

![](https://github.com/marta-krzyk-dev/SpitGame/blob/master/Gameplay_GIF.gif?raw=true)

# Features:
- [x] Player's name is shortened to 15 characters
- [x] command --help print the game's instructions (at any point of the game)
- [x] command -- resume resumes the game
- [x] the game asks 2 players for their names (name can consist of any characters, at least 1 character)
- [x] Save score between rounds
- [x] print graphical cards onto screen
- [x] User can choose to move a stack a duplicated card with 'y' , 'n'
- [ ] Option to redraw game when resuming game
- [x] Ask player to stack duplicates only once (per new duplicate)

# Gameplay:
- [x] Player can choose the card to be added to spit pile
- [x] If card is repeated in their piles, the duplicate will be placed on the leftmost pile
- [x] If the chosen cad can be put into 2 spit piles, the leftmost spit is chosen
- [x] If the player cannot move a card, they lose their turn
- [x] If both players cannot move a card, they both put any card to their spit piles
- [x] If player has an empty pile, a card from right-most pile is moved to reveal another card. This is repeated till there are empty spots
- [x] Player can choose a card to be moved onto an empty spot
