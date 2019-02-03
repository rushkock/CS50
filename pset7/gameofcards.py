# Implements a cards shuffler and dealer.
import random
class Card(object):
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    def __str__(self):
        return self.value + " of " + self.suit
class Deck(object):
    def __init__(self):
        self.suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        self.values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.cards = []
        for x in self.suits:
            for y in self.values:
                new_card = Card(x, y)
                self.cards.append(new_card)
    def __str__(self):
        return f"{len(self.cards)} cards in the deck"
    def shuffle(self):
        return random.shuffle(self.cards)
    def deal(self):
        return self.cards.pop()

if __name__ == "__main__":
    deck = Deck()
    print(deck)
    card = deck.deal()
    print(card)
    deck.shuffle()
    card = deck.deal()
    print(card)