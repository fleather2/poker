from colorama import Fore, Style
import random

VALUE_STRINGS = {2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10", 11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}
SUITS = ["Spade", "Club", "Heart", "Diamond"]
VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] # 11=Jack 12=Queen 13=King 14=Ace
BIG_BLIND = 100
SMALL_BLIND = 50

class card:
    
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def printcard(self):
        s = ["", ""]
        if self.suit in ("Heart",  "Diamond"):
            s[0] = Fore.RED
        else:
            s[0] = Fore.WHITE
            

        s[0] += VALUE_STRINGS[self.value] 
        s[1] = "of " + self.suit + "s" + Style.RESET_ALL
        print('{:>12} {:>12}'.format(s[0], s[1]))



class deck:
    def __init__(self, shuffle=True):
        d = []
        for i in range(0, 13):
            for j in range(0, 4):
                suit = SUITS[j]
                value = VALUES[i]
                c = card(suit, value)
                d.append(c)
        self.cards = d
        
        if shuffle:
            random.shuffle(self.cards)

    def printdeck(self):
        for c in self.cards:
            c.printcard()


    def deal(self): #deals a card, removing it from the decks
        return self.cards.pop()

#basic hand, TODO add player with attributes hand, total money, player-controlled
class player_hand:

    def __init__(self):
        self.cards = []
        self.bet = 0
        self.isfold = False

    def givecard(self, card):
        self.cards.append(card)

    def showcards(self):
        for c in self.cards:
            c.printcard()

    def fold(self):
        self.isfold = True

    
    
#5 cards at the front of the table
class dealer_hand:

    def __init__(self):
        self.cards = []
        self.bet = 0

    def givecard(self, card):
        self.cards.append(card)



gamedeck = deck()

# Deal Cards to Player, Dealer
user = player_hand()
opp = player_hand()
dealer = dealer_hand()

for i in range(2):
    user.givecard(gamedeck.deal())
    opp.givecard(gamedeck.deal())

for i in range(5):
    dealer.givecard(gamedeck.deal())


players = [user, opp]
#assign small and big blinds
players[0].bet = SMALL_BLIND
players[1].bet = BIG_BLIND

leadingbet = BIG_BLIND



# to deal with order change when raising, if a player raises, make a new list of players called nextorder.
#  add the raising player to it. add all of the subsequent player to it as the turn continues.
# when the turn is over. add the rest of the players in players[] IN ORDER  WHO ARE NOT ON THE LIST to it
# if the order has not changed and the leading bet is 0, flip a dealer card
neworder = []
for player in players:
    if len(neworder) > 0:
        neworder.append(player)
    if not player.isfold:

        if player == user:

            print("Your Turn")
            player.showcards()
            if players[0] == user:
                print("Betting it at you.")
                choice = int(input("1 - Check, 2 - Bet, 3- Fold\n\t"))
                print(choice)
                if choice == 1:
                    pass
                elif choice == 2:
                    choice = int(input("How much would you like to bet?\n\t"))
                    player.bet += choice
                    leadingbet = choice
                elif choice == 3:
                    print("You Fold")
                    player.fold()
            else:
                print("Leading bet is", leadingbet)
                choice = int(input("1 - Call, 2 - Raise, 3 - Fold\n\t"))
                if choice == 1:
                    player.bet += leadingbet
                elif choice == 2:
                    choice = input("How much would you like to raise by?\n\t")
                    player.bet += leadingbet
                    player.bet += choice
                    leadingbet = choice
                    neworder = [player]
                elif choice == 3:
                    print("You Fold")
                    player.fold()
            
        else: #Player not contolled by user
            if players[0] == player:
                # can check, bet, or fold
                choice = random.randint(1,3)
                if choice == 1:
                    pass
                    print("Opponent Checks")
                elif choice == 2:
                    player.bet += 50
                    leadingbet = 50
                    print("Opponent Bets 50")
                else:
                    print("Opponent Folds")
                    player.fold()
            else:
                # can call, raise, or fold
                choice = random.randint(1,3)
                if choice == 1:
                    player.bet += leadingbet
                    print("Opponent Calls")
                elif choice == 2:
                    player.bet += leadingbet
                    player.bet += 50
                    neworder = [player]
                    print("Opponent Raises 50")
                else:
                    player.fold()
                    print("Opponent Folds")
if len(neworder) > 0:
    i = 0
    while len(players) > len(neworder):
        neworder.append(players[i])
        i += 1



            
        




 

