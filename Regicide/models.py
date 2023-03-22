from enum import Enum
import pygame
import random

class Suits(Enum):
    CLUB = 0
    SPADE = 1
    HEART = 2
    DIAMOND = 3

class Card:
    suit = None
    value = None
    image = None

    def __init__(self, suit, value, size='small'):
        self.suit = suit
        self.value = value
        self.image = pygame.image.load('Regicide/images/' + self.suit.name + '-' + str(self.value) + '.svg')
        if size == 'small':
            self.image = pygame.transform.scale(self.image, (int(238*0.4), int(332*0.4)))
        else:
            self.image = pygame.transform.scale(self.image, (int(238*0.8), int(332*0.8)))
    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit
    
class Deck:
    cards = None
    def __init__(self, name) -> None:
        self.cards = []
        if name == "draw":
            for suit in Suits:
                for value in range(1,11):
                    self.cards.append(Card(suit, value))
        elif name == "royal":
            jacks = []
            queens = []
            kings = []
            for suit in Suits:
                kings.append(Card(suit, 13, 'large'))
            random.shuffle(kings)
            self.cards.extend(kings)
            for suit in Suits:
                queens.append(Card(suit, 12, 'large'))
            random.shuffle(queens)
            self.cards.extend(queens)
            for suit in Suits:
                jacks.append(Card(suit, 11, 'large'))
            random.shuffle(jacks)
            self.cards.extend(jacks)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def length(self):
        return len(self.cards)
  
    def refresh(self, cards:int, pile):
        self.cards.reverse()
        for n in range(cards):
            try: 
                self.cards.append(pile.deal())
            except:
               pass
        self.cards.reverse()
    
    def add_to_top(self, card:Card):
       self.cards.append(card)

class Player:
    hand = None

    def __init__(self):
        self.hand = []

    def draw(self, deck):
        self.hand.append(deck.deal())

    def play(self) -> Card:
        return self.hand.pop(0)

class Royal:
    health = None
    attack_value = None
    suit = None
    card = None
    rank = None

    def __init__(self, card:Card) -> None:
        self.card = card
        self.suit = card.get_suit()
        if card.get_value() == 11:
            self.health = 20
            self.attack_value = 10
            self.rank = 'Jack'
        elif card.get_value() == 12:
            self.health = 30
            self.attack_value = 15
            self.rank = 'Queen'
        else:
            self.health = 40
            self.attack_value = 20
            self.rank = 'King'

    def attack(self, damage:int):
        "Player attacking royal"
        self.health -= damage
    
    def block(self, block:int):
       "Royal being blocked"
       self.attack_value -= block

    def defend(self):
        "Royal attacking player"
        return self.attack_value
    
    def get_health(self):
       return self.health
    
    def get_suit(self):
       return self.suit
    
    def get_rank(self):
        return self.rank
    
    def get_card(self):
       return self.card
    
    def get_attack(self):
        return self.attack_value
    
    def get_value(self):
        return self.card.get_value()