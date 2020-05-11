from colorama import Fore, Style
import random
import characters

VALUE_STRINGS = {2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10", 11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}
SUITS = ["Spade", "Club", "Heart", "Diamond"]
VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] # 11=Jack 12=Queen 13=King 14=Ace
BIG_BLIND = 100
SMALL_BLIND = 50
VICTORY = ""

COMBINATIONS = {0: "High Card", 1: "One Pair", 2: "Two Pairs", 3: "Three of a Kind", 4: "Straight", 5:"Flush", 6: "Full House", 7:"Four of a Kind", 8:"Straight Flush", 9: "Royal Flush", 10: "Five of a Kind"}

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
        self.score = 0

    def givecard(self, card):
        self.cards.append(card)

    def showcards(self):
        for c in self.cards:
            c.printcard()

    def fold(self):
        self.isfold = True

    def givecards(self, cards):
        for c in cards:
            self.cards.append(c)

    def givecard(self, card):
        self.cards.append(card)

    
    
#5 cards at the front of the table
class dealer_hand:

    def __init__(self):
        self.cards = []
        self.bet = 0
        self.revealed = 0

    def givecard(self, card):
        self.cards.append(card)

    def showcards(self):
        for i in range(self.revealed):
            self.cards[i].printcard()


def setscore(oldscore, newscore): #function for comparing two score arrays. first compares type of hand, then compares different values to help sort out potential ties
    if newscore[0] > oldscore[0]:
        return newscore
    if newscore[0] < oldscore[0]:
        return oldscore
    if newscore[1] > oldscore[1]:
        return newscore 
    return oldscore

def calculateHand(dealer, player): #TODO after every condition is checked, modularize
    #Take Value, print hand, return score
    score = [0, 0]
    allcards = dealer.cards + player.cards

    # Check for flushes/straights
    if all(c.suit == allcards[0].suit for c in allcards): # if the suits are the same (flush)
        if all(x.value in [10,11,12,13,14] for x in allcards): # if ace, king, queen, jack, 10 are all in allcards
             #Royal Flush
            return setscore(score, [9, 0])
        else:
            for card in allcards:
                cardexclude = [] + allcards #created this way to ensure that cardexclude is a separate list
                cardexclude.remove(card)
                if all(x.value in [card.value+1, card.value+2, card.value+3, card.value+4] for x in cardexclude): #checks for straights (and flush)
                    return setscore(score, [8, card.value])# Straight Flush with the value of the lowest card
            
            score = setscore(score, [5, max(x.value for x in allcards)])# Flush with no straight, high card wins TODO check facts here
    
    for card in allcards:
        cardexclude = [] + allcards
        cardexclude.remove(card)
        if all(x.value in [card.value+1, card.value+2, card.value+3, card.value+4] for x in cardexclude): #checks for straights
            score = setscore(score, [4, card.value])# Straight with the value of the lowest card
            
    
    #check for card combos, such as full house, _ of a kind, etc
    combos = []
    values = []
    
    for card in allcards:
        
        if len(combos) == 0:
            combos.append([card])

        else:
            for x in combos:
                if card.value == x[0].value:
                    x.append(card)
            if all(card not in x for x in combos):
                combos.append([card])
            
    for x in combos:
        if len(x) == 5:
            score = setscore(score, [10, x[0].value]) # 5 of a kind (only possible w joker)
        if len(x) == 4:
            score = setscore(score, [7, x[0].value]) # 4 of a kind
        if len(x) == 3:
            score = setscore(score, [3, x[0].value]) # 3 of a kind
            for y in combos:
                if len(y) == 2:
                    score = setscore(score, [6, x[0].value]) # Full House
        if len(x) == 2:
            score = setscore(score, [1, x[0].value]) # Pair
            for y in combos:
                if len(y) == 2 and y != x:
                    score = setscore(score, [2, x[0].value]) # Two Pair
    

    #check for high card
    highcard = max(card.value for card in allcards)
    score = setscore(score, [0, highcard])

    return score

class gamestate:
    def __init__(self, players, dealer, leadingbet, userfold=False):
        self.players = players
        self.dealer = dealer
        self.leadingbet = leadingbet
        self.userfold = userfold

def userturn(user, state): 
    # takes info from game, returns players[] in a different order if the betting is increased, returns new leading bet
    players = state.players
    dealer = state.dealer
    leadingbet = state.leadingbet
    
    pot = 0
    for p in players:
        pot += p.bet
    print("--- Your Turn ---")
    print("Your Current Bet:", user.bet)
    print("The Pot:", pot)
    print("Your Hand:")
    user.showcards()
    print("Dealer Hand:")
    dealer.showcards()
    if players[0] == user:
        print ("Betting is at you")
        
        choice = 0
        while choice not in [1, 2, 3]:
            choice = input("You can: 1 - Check, 2 - Bet, 3 - Fold\n\t")
            try:
                choice = int(choice)
                if choice not in [1,2,3]:
                    raise ValueError("Invalid Choice Input")
                
                if choice == 1:
                    print("You Check")
                    return state 

                elif choice == 2:
                    bet = int(input("How much would you like to bet?\n\t"))
                    leadingbet = bet # TODO check if player has enough money for bet
                    user.bet += leadingbet
                    state.leadingbet = bet
                    return state

                elif choice == 3:
                    print("You Fold")
                    state.userfold = True
                    user.isfold = True
                    return state

                else:
                    choice = 0
            except: 
                print("INVALID INPUT. Try again")
                choice = 0
        

    else:
        print("Leading bet is", leadingbet)
        choice = 0
        while choice not in [1,2,3]:
            choice = input(str("You can: 1 - Call (bet " + str(leadingbet) + ") 2 - Raise, 3 - Fold\n\t"))

            try:
                choice = int(choice)
                if choice not in [1,2,3]:
                    raise ValueError("Invalid Choice Input")
                
                if choice == 1:
                    print("You Call")
                    user.bet += leadingbet
                    return state 

                elif choice == 2:
                    bet = int(input("How much would you like to raise by?\n\t"))
                    leadingbet += bet # TODO check if player has enough money for bet
                    user.bet += leadingbet
                    state.leadingbet = bet

                    #Change the position of the players
                    neworder = []
                    appendrest = False
                    for p in players:
                        if p == user:
                            neworder.append(p)
                            appendrest = True
                        elif appendrest == True:
                            neworder.append(p)
                    for p in players:
                        if p not in neworder:
                            neworder.append(p)
                    state.players = neworder
                    return state

                elif choice == 3:
                    print("You Fold")
                    state.userfold = True
                    user.isfold = True
                    return state

                else:
                    choice = 0
            except: 
                print("INVALID INPUT. Try again")
                choice = 0
    
    return state

def opponentturn(player, state):
    
    maxchoice = 2 #2 for never fold, 3 for fold
    print("--- Opponent Turn ---")
    if state.players[0] == player:
        print("Betting at Opponent")
        choice = random.randint(1, maxchoice)
        if choice == 1:
            print("Opponent Checks")
            return state
        elif choice == 2:
            print("Opponent Bets 50")
            state.leadingbet = 50
            player.bet += 50
            return state
        elif choice == 3:
            print("Opponent Folds")
            player.isfold = True
            return state
    else:
        print("Leading bet is", state.leadingbet)
        choice = random.randint(1,maxchoice)
        if choice == 1:
            print("Opponent Calls")
            player.bet += state.leadingbet
            return state
        elif choice == 2:
            print("Opponent Raises")
            state.leadingbet += 50
            player.bet += state.leadingbet

            # Change order of betting for raise
            neworder = []
            appendrest = False
            for p in state.players:
                if p == player:
                    neworder.append(p)
                    appendrest = True
                elif appendrest == True:
                    neworder.append(p)
            for p in state.players:
                if p not in neworder:
                    neworder.append(p)
            state.players = neworder
            return state

        elif choice == 3:
            print("Opponent Folds")
            player.isfold = True
            return state
        


def main():
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
    
    turn = True # Condition for continuing to another turn. Stops if every player has checked at all 5 decks revealed, or if everyone except one person has folded
    state = gamestate(players, dealer, leadingbet, userfold=False)
    while turn:

        for p in players:
            
            if p == user:
                state = userturn(user, state)
            else:
                state = opponentturn(p, state)
            
        
        
        if leadingbet == 0:
            #Flip a Dealer Card
            if dealer.revealed == 5:
                # End if all dealer cards are showing and everyone has checked
                victory = "All Check"
                turn = False
            else:
                dealer.revealed += 1
        else:
            leadingbet=0
        
        # End if there is only one person left
        folds = 0
        for p in players:
            if p.isfold == True:
                folds += 1
                
        if folds == (len(players) - 1):
            turn = False
            victory = "Folds"


    # Victory condition - everyone but one person folds
    if victory == "Folds":
        winner = player_hand()
        for p in players:
            if p.isfold == False:
                
                winner = p

        if winner == user:
            print("You Win!")


    if victory == "All Check":
        print("Showdown")
        #determine winner
        competing = []
        for p in players:
            if p.isfold == False:
                competing.append(p)
        
        for p in competing:
            p.score = calculateHand(dealer, p)
            print(p.score)

        # TODO simplify
        besthand = 0
        for p in competing:
            if p.score[0] > besthand:
                besthand = p.score[0]
        print("Best first score: ", besthand)
        finalists = []
        for p in competing:
            if p.score[0] == besthand:
                finalists.append(p)
        winner = player_hand()
        besthand = 0
        for p in finalists:
            if p.score[1] > besthand:
                winner = p
                besthand = p.score[1]

    # For Both Win Conditions

    for p in players:
        
        if p != winner and p != user:
            print("Opponent Hand")
            p.showcards()
        if p == user:
            print("Your Hand")
            p.showcards()

    print("---WINNING HAND---")
    winner.showcards()
    print("Dealer's Hand")
    dealer.showcards()
    pot = 0
    for p in players:
        pot += p.bet
    if winner==user:

        print("Coagulations. You win the pot of", pot)
    else:
        
        print("You lose")

            
            



    
if __name__ == "__main__":
    main()


    
    

    


            
        




 

