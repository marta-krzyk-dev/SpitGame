from random import shuffle


class Deck:
    faceValues = faceValues = dict(A=14, K=13, Q=12, J=11)  # Static field

    def __init__(self):
        self.deck = []

        for i in range(4):
            for card in range(2, 11):
                self.deck.append(str(card))
            for card in Deck.faceValues:
                self.deck.append(card)

        shuffle(self.deck)

    def getHalves(self):
        return self.deck[:26], self.deck[26:]
