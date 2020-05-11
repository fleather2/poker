from poker import *
card0 = card("Heart", 10)
card1 = card("Diamond", 11)
card2 = card("Heart", 2)
card3 = card("Spade", 1)
card4 = card("Club", 3)

player = player_hand()
cards = [card0, card1, card2, card3, card4]
player.givecards(cards)
dealer = dealer_hand()

score = []
score = calculateHand(dealer, player)

print(COMBINATIONS[score[0]])