# Blackjack.py
# Author: Dong Hyun Kim
# Date: 09/26/2018
# A simple console-based single-player blackjack game.
# Simply type "h" (for hit) or "s" (for stand) in the console to interact with the dealer. If you stand,
#   you can see the dealer getting cards from the deck until the value of his hand is 17 or higher.
# Enjoy!


# import libraries
from random import shuffle  # to shuffle the deck
import time                  # to have intervals between dealer drawing (for suspense)

# initialize global variables regarding cards
values = {'A':11, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
suits = ['Clubs', 'Spade', 'Diamond', 'Hearts']

# used to determine if game is over
PLAYER_IN = 0       # game is not over
PLAYER_BUSTED = 1   # player busted, game over
BLACKJACK = 2       # player blackjack, dealer needs to draw cards

# constants
BLACKJACK_VAL = 21      # value of hand for a blackjack
ZERO_SCORE = 0          # hand with no value
ACE_HARD_TO_SOFT = 10   # translation value from soft value to hard value ace (11 - 1)
WIN = 1
TIE = 0
LOSE = -1

class Card:
    '''The Card class is used to represent individual cards.
        It contains the rank, value, and suit of a card.'''
    def __init__(self, rank, suit):
        self.rank = rank
        self.value = values[rank]
        self.suit = suit

    # returns rank of a given card
    def get_rank(self):
        return self.rank

    # returns suit of a given card
    def get_suit(self):
        return self.suit

    # returns the value of a given card. The Ace was chosen to have
    #   a value of 11.
    def get_value(self):
        return self.value

class Hand:
    '''The Hand class is used to represent the hand of dealer or
        player. It contains the list of cards held in a hand,
        the number of aces within the hand, and the hard value.'''
    def __init__(self):
        self.hand = []
        self.numAce = 0
        self.value = 0

    # adds a Card object to the list. Each time an ace is added,
    #   the counter value increments.
    def add_card(self, card):
        self.hand.append(card)
        self.value += card.get_value()
        if card.get_rank() == 'A':
            self.numAce += 1

    # returns the point value of a hand. Notice that the code
    #   handles the case of one or multiple Aces in the hand.
    # If there exists no ace, the first tuple element will simply
    #   return 0 and the second tuple element will return the
    #   overall point value.
    # If there exists an ace, the first tuple element will return
    #   the soft value and the second tuple element will return the
    #   hard value. If the hard value has exceeded BLACKJACK_VAL, however,
    #   the first tuple element will return 0 and the second tuple element
    #   will return the soft value.
    def get_value(self):
        # if there is an ace, return a soft value and hard value unless
        #   the hard value has exceeded BLACKJACK_VAL. In this case, we just
        #   return the soft value.
        if self.numAce:
            self.value -= (self.numAce - 1) * ACE_HARD_TO_SOFT
            if self.value > BLACKJACK_VAL:
                return ZERO_SCORE, self.value - ACE_HARD_TO_SOFT
            else:
                return self.value - ACE_HARD_TO_SOFT, self.value

        # if there is no ace, simply return the value
        return ZERO_SCORE, self.value

    # returns the hand in a form that can be printed to the console
    def get_hand(self):
        return [[card.get_rank(), card.get_suit()] for card in self.hand]

class Deck:
    '''The Deck class is used to represent the pack of 52 cards.
        It contains the deck itself.'''
    def __init__(self):
        self.deck = [Card(rank, suit) for rank in ranks for suit in suits]

    # shuffle the deck using the shuffle library from random library
    def shuffle_deck(self):
        shuffle(self.deck)

    # returns a card from the deck and removes it
    def deal_card(self):
        return self.deck.pop()

class PlayBlackjack:
    '''The PlayBlackjack class is used to handle the flow of blackjack.
        It contains the deck used in the game, the hand for the player,
        and the hand for the dealer.'''
    def __init__(self):
        self.gameDeck = Deck()
        self.playerHand = Hand()
        self.dealerHand = Hand()

    # start the game by dealing appropriately and checking if
    #   there is an immediate blackjack. If so, we return a
    #   non-zero value.
    def start(self):
        # shuffle deck
        self.gameDeck.shuffle_deck()
        # deal 2 cards to player and 1 card to dealer
        self.playerHand.add_card(self.gameDeck.deal_card())
        self.playerHand.add_card(self.gameDeck.deal_card())
        self.dealerHand.add_card(self.gameDeck.deal_card())

        # print the game status
        self.print_status()

        # check the value (or hard value if there's an ace)
        #   for a blackjack. If so, we return a non-zero
        #   value and proceed appropriately.
        PVal = self.playerHand.get_value()[1]
        if PVal == BLACKJACK_VAL:
            print("Blackjack! Wait for dealer...")
            return BLACKJACK
        # otherwise, we return PLAYER_IN.
        return PLAYER_IN

    # deals a card to the player and checks if there is
    #   a bust or a blackjack. If so, we return a non-zero
    #   value corresponding to the action.
    def hit(self):
        # deal card, add to player hand, and print
        self.playerHand.add_card(self.gameDeck.deal_card())
        self.print_status()

        # check the value (or hard value if there's an ace)
        #   for a blackjack or a bust. If either, we return
        #   a non-zero value.
        PVal = self.playerHand.get_value()[1]
        if PVal > BLACKJACK_VAL:
            return PLAYER_BUSTED
        elif PVal == BLACKJACK_VAL:
            print("Blackjack! Wait for dealer...")
            print()
            return BLACKJACK
        # otherwise, we return PLAYER_IN
        return PLAYER_IN

    # keeps adding cards to the dealer's hand until it reaches
    #   17 or above. Uses the hard value, unless drawing an ace
    #   with the hard value will cause the dealer to bust.
    def stand(self):
        print("Dealer getting cards...")
        while self.dealerHand.get_value()[1] < 17:
            self.dealerHand.add_card(self.gameDeck.deal_card())
            time.sleep(2)
            self.print_status()
            print()

    # print the status of the game. Only outputs the soft value
    #   if appropriate.
    def print_status(self):
        softDVal, DVal = self.dealerHand.get_value()
        softPVal, PVal = self.playerHand.get_value()
        if softDVal:
            print("Dealer Val: ", softDVal, "/", DVal)
        else:
            print("Dealer Val: ", DVal)
        print("Dealer Cards: ", self.dealerHand.get_hand())
        if softPVal:
            print("Player Val: ", softPVal, "/", PVal)
        else:
            print("Player Val: ", PVal)
        print("Player Cards: ", self.playerHand.get_hand())

    # checks the status of the game. return WIN and LOSE as necessary.
    def check_status(self):
        softDval, DVal = self.dealerHand.get_value()
        softPVal, PVal = self.playerHand.get_value()
        # player is busted, dealer score doesn't matter
        if PVal > BLACKJACK_VAL:
            print("Player Busted! You lose!")
            return LOSE
        # player is good but dealer busts
        elif DVal > BLACKJACK_VAL:
            print("Dealer Busted! You win!")
            return WIN
        # player and dealer are good, but tied
        #   includes case of PVal = DVal = BLACKJACK_VAL
        elif PVal == DVal:
            print("Tie!")
            return TIE
        # player and dealer are good, and player has
        #   a blackjack while dealer doesn't
        elif PVal == BLACKJACK_VAL:
            print("Blackjack! You win!")
            return WIN
        # player has higher score than dealer
        elif PVal > DVal:
            print("Player value higher! You win!")
            return WIN
        # player has lower score than dealer
        elif PVal < DVal:
            print("Dealer value higher! You lose!")
            return LOSE

if __name__ == '__main__':
    # determine if player wants to play game
    play_game = True
    win, tie, lose = 0, 0, 0

    while  play_game:
        # initialize game of blackjack
        game = PlayBlackjack()
        status = game.start()
        # if there is an immediate blackjack, we skip to the part where
        #   dealer draws until the value is 17 or over
        if status == BLACKJACK:
            response = 's'
            game.stand()
        # otherwise, proceed as normal
        else:
            response = 'h'

        while (response == 'h'):
            response = input('Hit or stay? (Hit = \'h\', Stand = \'s\')')
            print()
            # if player hits, check for a bust or blackjack.
            if response == 'h':
                status = game.hit()
                # if bust, game is over.
                if status == PLAYER_BUSTED:
                    break
                # if blackjack, dealer draws until value is 17 or over
                elif status == BLACKJACK:
                    game.stand()
                    break
            # if player stands, act accordingly
            elif response == 's':
                game.stand()
            else:
                print("Invalid answer. Please select again.")
                response = 'h'

        # output the game status
        gamestatus = game.check_status()
        if gamestatus == WIN:
            win += 1
        elif gamestatus == TIE:
            tie += 1
        elif gamestatus == LOSE:
            lose += 1

        print("Won: ", win, ", Tied: ", tie, ", Lost: ", lose)

        response = 'y'

        # check if user wants to play again
        while response == 'y':
            response = input('Play again? (Yes = \'y\', No = \'n\')')
            print()
            if response == 'y':
                print("Welcome back!")
                break
            elif response == 'n':
                print("Thank you. Come back soon!")
                play_game = False
            else:
                print("Invalid answer. Please select again.")
                response = 'y'