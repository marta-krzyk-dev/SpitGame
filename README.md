# SplitGame
Split card console game in Python

TO DOs:
- [x] command --help print the game's instructions (at any point of the game)
- [x] command -- resume resumes the game
- [x] the game asks 2 players for their names (name can consist of any characters, at least 1 character)
- [ ] 2 players can connect via internal network, python-request library, Flask
- [ ] spits are part of SpitGame class, not players?
- [x] implement Spit's logic
- [ ] show winner at the end (scores)
- [x] Save score between rounds
- [x] print graphical cards onto screen
- [ ] Defect infinite loop when there are around 5 cards, some can be stacked onto 1 pile, then player is prompted to move card to an empty place
- [x] User can choose to move a stack a duplicated card with 'y' , 'n'
- [ ] Redraw game when resuming game
- [ ] Fix recognizing when both users cannot make a move
- [x] Ask player to stack duplicates only once (per duplicate)
- [ ] Recognize draw
- [x] Don't ask to stack up the same duplicates more than once
- [ ] Move AddCardToSpitPile , MoveCardsInPlayersPile to Player class

TESTS use commands when:
- [x] Game prompts for player's names
- [ ] Both users cannot move and they add cards to their spit piles
- [x] User chooses a card
- [x] User chooses a card to move to an empty spot
- [x] User agrees to stack cards onto another 

TODOs
- [ ] Move AskForName to pLayer class?
- [ ] Merge method GetInputWithAllowedAnswers into GetInput
- [ ] Use ConvertCardToNumericValue in Player
- [ ] Uniform print cards methods (remove some if possible)
- [ ] Show number of cards in piles

TESTS:
- [x] Create player with 15+ character name, check score table
- [ ] Play 2 full rounds
- [ ] Have both players outta moves

Special scenarios:
- [x] Consider cards: 2 9 9 Q K. The game cannot infinitely prompt user to stack 9s and then move top 9 to empty spot

Features:
- [x] Player's name is shortened to 15 characters

Gameplay:
- [ ] Player can choose the card to be added to spit pile
- [ ] If card is repeated in their piles, the duplicate will be placed on the leftmost pile
- [ ] If the chosen cad can be put into 2 spit piles, the leftmost spit is chosen
- [ ] If the player cannot move a card, they lose their turn
- [ ] If both players cannot move a card, they both put any card to their spit piles
- [ ] Game automatically moves a duplicate card to the left pile to reveal another card. This is repeated until no more duplicate moving is possible
- [ ] If player has an empty pile, a card from right-most pile is moved to reveal another card. This is reperated till possible
- [ ] Player can choose a card to be moved onto an empty spot
