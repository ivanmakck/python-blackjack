import random
from os import system
from time import sleep

cards_value = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 10,
    'Q': 10,
    'K': 10,
    'A': [1, 11]
}

class Deck:

    def __init__(self):
        self.cards = ['2','3','4','5','6','7','8','9','10','J','Q','K','A'] * 4

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_one(self):
        return self.cards.pop()


class Hand:

    def __init__(self):
        self.cards = []
        self.score = 0

    def hit(self, card):
        self.cards.append(card)
        self.add_score()

    def show_all(self):
        return self.cards

    def add_score(self):
        card = self.cards[-1]
        if card == 'A' and self.score > 10:
            self.score += cards_value[card][0]
        elif card == 'A' and self.score <= 10:
            self.score += cards_value[card][1]
        else:
            self.score += cards_value[card]

    def reset(self):
        self.cards = []
        self.score = 0


class Dealer(Hand):

    def show_one(self):
        return list(self.cards[0])


class Player(Hand):

    def __init__(self):
        super().__init__()
        self.balance = 0

    def add_balance(self, balance):
        self.balance += balance

    def place_bet(self, bet):
        self.balance -= bet


def clear_output():
    system('cls||clear')


def add_balance_inquery(player):
    ask = True
    while ask:
        print('Insufficient funds!')
        add_balance = input('Would you like to add money to your account? (Y/N) ').upper()
        clear_output()
        if add_balance == 'Y':
            ask = add_balance_amount(player)
        elif add_balance == 'N':
            ask = False


def add_balance_amount(player):
    while True:
        clear_output()
        try:
            balance = int(input(f'How much would you like to add to your account? '))
            clear_output()
        except:
            continue
        else:
            if balance < 0:
                continue
            else:
                player.add_balance(balance)
                return False


def bet_input(player):
    while True:
        clear_output()
        try:
            bet = int(input(f'How much do you want to bet? You have ${player.balance} in your account. (Enter 0 to exit game) '))
            clear_output()
        except:
            continue
        else:
            if bet > player.balance:
                add_balance_inquery(player)
            elif bet < 0:
                continue
            else:
                return bet


def win(player, bet, multiplier):
    player.add_balance(bet * multiplier)
    return f'You win ${bet * multiplier}!'


def show_cards(player, dealer, dealer_show_all=False):
    if dealer_show_all:
        print(f"Dealer's hand: {dealer.show_all()}, the dealer's score is {dealer.score}.")
        print(f"Player's hand: {player.show_all()}, your score is {player.score}.")
    else:
        print(f"Dealer's hand: {dealer.show_one()}.")
        print(f"Player's hand: {player.show_all()}, your score is {player.score}.")


def hit(player, deck):
    player.hit(deck.deal_one())


def hit_inquery():
    while True:
        hit_q = input('Hit? (Y/N) ').upper()
        clear_output()
        if hit_q in ('Y', 'N'):
            return hit_q


def confirm_play():
    while True:
        play = input('Continue playing? (Y/N) ').upper()
        clear_output()
        if play == 'Y':
            return True
        elif play == 'N':
            return False


def welcome():
    print('''

 /$$$$$$$  /$$                     /$$                               /$$      
| $$__  $$| $$                    | $$                              | $$      
| $$  \ $$| $$  /$$$$$$   /$$$$$$$| $$   /$$ /$$  /$$$$$$   /$$$$$$$| $$   /$$
| $$$$$$$ | $$ |____  $$ /$$_____/| $$  /$$/|__/ |____  $$ /$$_____/| $$  /$$/
| $$__  $$| $$  /$$$$$$$| $$      | $$$$$$/  /$$  /$$$$$$$| $$      | $$$$$$/ 
| $$  \ $$| $$ /$$__  $$| $$      | $$_  $$ | $$ /$$__  $$| $$      | $$_  $$ 
| $$$$$$$/| $$|  $$$$$$$|  $$$$$$$| $$ \  $$| $$|  $$$$$$$|  $$$$$$$| $$ \  $$
|_______/ |__/ \_______/ \_______/|__/  \__/| $$ \_______/ \_______/|__/  \__/
                                       /$$  | $$                              
                                      |  $$$$$$/                              
                                       \______/                               
            
Welcome to Blackjack played in the terminal. The rules are simple: try to get as
close to 21 as possible without going over!  You can add and bet virtual funds.
If you win, you get double the amount!
'J', 'Q', and 'K' represent a value of 10.
'A' represents either a value of 1 or 11.
    ''')

    input('<< Hit any key to start playing! >>')


def play_game():
    deck = Deck()
    deck.shuffle()

    dealer = Dealer()
    player = Player()
    player.add_balance(100)

    session_on = True
    while session_on:

        print(f'Game starting')
        sleep(3)

        dealer.reset()
        player.reset()

        for i in range(2):
            hit(dealer, deck)
            hit(player, deck)

        if player.balance == 0:
            add_balance_inquery(player)

        bet = bet_input(player)

        if bet == 0:
            break

        player.place_bet(bet)

        print(f'You bet ${bet}.')
        sleep(1)
        print(f'Round starting')
        sleep(1)

        show_cards(player, dealer)

        game_on = True
        while game_on:
            if dealer.score == 21:
                clear_output()
                print(f"Dealer has {dealer.score}! You lose ${bet}.")
                show_cards(player, dealer, dealer_show_all=True)
                game_on = False
            else:
                if player.score == 21:
                    clear_output()
                    print(f"You have {player.score}! {win(player, bet, 2)}")
                    show_cards(player, dealer, dealer_show_all=True)
                    game_on = False
                else:
                    if hit_inquery() == 'Y':
                        hit(player, deck)
                        if player.score == 21:
                            print(f"You have {player.score}! {win(player, bet, 2)}")
                            show_cards(player, dealer, dealer_show_all=True)
                            game_on = False
                        elif player.score > 21:
                            print(f"Bust! You lost your bet of ${bet}!")
                            show_cards(player, dealer, dealer_show_all=True)
                            game_on = False
                        else:
                            show_cards(player, dealer)
                    else:
                        print("Dealer is drawing...")
                        sleep(1)
                        while True:
                            if dealer.score < 21 and dealer.score <= player.score:
                                hit(dealer, deck)
                            elif dealer.score < 21 and dealer.score > player.score:
                                show_cards(player, dealer, dealer_show_all=True)
                                print(f'Dealer has {dealer.score} and you stopped at {player.score}. You lose ${bet}.')
                                game_on = False
                                break
                            elif dealer.score > 21:
                                show_cards(player, dealer, dealer_show_all=True)
                                print(f'Dealer bust! {win(player, bet, 2)}')
                                game_on = False
                                break
                            else:
                                print(f"Dealer has {dealer.score}! You lose ${bet}.")
                                show_cards(player, dealer, dealer_show_all=True)
                                game_on = False
                                break
        
        session_on = confirm_play()

if __name__=='__main__':
    
    welcome()
    play_game()
