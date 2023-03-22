import models

class Engine():
    draw_deck = None
    discard_pile = None
    royal_deck = None
    player = None
    hand_limit = 8
    royal = None
    won_game = False
    played_cards = []
    card_selection = set()
    game_state = None       #Possible values 'Charge', 'Discard', 'Over'

    def __init__(self) -> None:
        self.draw_deck = models.Deck('draw')
        self.discard_pile = models.Deck('discard')
        self.royal_deck = models.Deck('royal')
        self.player = models.Player()
        self.draw_deck.shuffle()
        while len(self.player.hand)<self.hand_limit:
            self.player.draw(self.draw_deck)
        self.royal = models.Royal(self.royal_deck.deal())
        self.game_state = 'Charge'

    def select_card(self, card):
        if card in self.card_selection:
            self.card_selection.remove(card)
        else:
            self.card_selection.add(card)
    
       
    def charge(self) ->bool:
        """
        Checks if we can call attack
        """
        cards = self.card_selection.copy()
        values = set()
        for card in cards:
            values.add(card.get_value())
        if len(values)>2:       #Cannot play multiple values
            return False
        if len(values) == 2:    #Two different values is only allowed with exactly one ace and one other
            if len(cards)>2:
                return False
            aces = len([card for card in cards if card.get_value() == 1])
            if aces == 1:
                return True
            else:
                return False
        match len(self.card_selection):
            case 0:                     #Cannot attack with 0 cards
                return False
            case 1:                     #Single card will always work
                return True
            case 2:
                if cards.pop().get_value() >5:  # Double 1s, 2s, 3s, 4s, and 5s permissable
                    return False
                else: return True
            case 3:
                if cards.pop().get_value() > 3:
                    return False
                else: return True
            case 4:
                if cards.pop().get_value() > 2:
                    return False
                else: return True
            case _:
                return False

    def attack(self):
        """
        Attack using current card selection
        """
        total_attack = 0
        played_heart = False
        played_diamonds = False
        played_spades = False
        played_clubs = False
        for card in self.card_selection:
            self.player.hand.remove(card)
            self.played_cards.append(card)

            total_attack += card.get_value()
            if card.get_suit()!=self.royal.get_suit():
                match card.get_suit():
                    case models.Suits.CLUB:
                        played_clubs = True
                    case models.Suits.SPADE:
                        played_spades = True
                    case models.Suits.HEART:
                        played_heart = True
                    case models.Suits.DIAMOND:
                        played_diamonds = True
        self.card_selection = set()
        
        #Heart effect
        if played_heart:
            self.discard_pile.shuffle()
            self.draw_deck.refresh(total_attack, self.discard_pile)

        #Diamond effect
        if played_diamonds:
            draw_cards = min(total_attack, self.hand_limit-len(self.player.hand))
            for n in range(draw_cards):
                try:
                    self.player.draw(self.draw_deck)
                except:
                    pass

        #Spade effect
        if played_spades:
            self.royal.block(total_attack)

        #Clubs effect        
        if played_clubs:
            total_attack = total_attack*2
    
        #Player attacks
        self.royal.attack(total_attack)

        #Cleanup when royal defeated
        health_check = self.royal.get_health()
        if health_check < 1:
            defeated = models.Card(self.royal.get_suit(), self.royal.get_value())
            if health_check == 0:
                self.draw_deck.add_to_top(defeated)
            else:
                self.discard_pile.add_to_top(defeated)
            self.royal = None
            for card in self.played_cards:
                self.discard_pile.add_to_top(card)
            self.played_cards = []
            try:
                self.royal = models.Royal(self.royal_deck.deal())
            except Exception:
                self.won_game = True
                self.game_state = 'Over'
        else:
            if self.royal.get_attack()>0:
                if len(self.player.hand)>0:
                    self.game_state = 'Discard'
                else:
                    self.game_state = 'Over'
    
    def discard(self):
        """
        Check if selected cards are enough to discard
        """
        #Player defends against royal attack value by discarding cards
        discard_amount = self.royal.defend()
        value = 0
        for card in self.card_selection:
            value += card.get_value()
        if value >= discard_amount:
            return True
        else: return False
    
    def defend(self):
        """
        Discard card selection
        """
        for card in self.card_selection:
            self.player.hand.remove(card)
            self.discard_pile.add_to_top(card)
        self.card_selection = set()
        if len(self.player.hand)>0:
            self.game_state = 'Charge'
        else:
            self.game_state = 'Over'
            
    def get_selected(self):
        return self.card_selection
    
    def get_hand(self):
        return self.player.hand
    
    def get_played(self):
        return self.played_cards
    
    def get_state(self):
        return self.game_state
    
    def get_royal_immunity(self):

        #power_text = f"Hearts: refresh draw pile\nDiamonds: draw cards\nSpades: block attack.\nClubs: double your attack.\n"

        if self.royal.get_suit() == models.Suits.CLUB:
            return f"The {self.royal.get_rank()} of Clubs immune to the attack doubling power of clubs"
        elif self.royal.get_suit() == models.Suits.SPADE:
            return f"The {self.royal.get_rank()} of Spades immune to the blocking power of spades"
        elif self.royal.get_suit() == models.Suits.HEART:
            return f"The {self.royal.get_rank()} of Hearts stops the refresh power of hearts"
        elif self.royal.get_suit() == models.Suits.DIAMOND:
            return f"The {self.royal.get_rank()} of Diamonds stops the redraw power of diamonds"
