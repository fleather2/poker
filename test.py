from poker import *
card0 = card("Hearts", 10)
card1 = card("Hearts", 11)
card2 = card("Hearts", 12)
card3 = card("Hearts", 13)
card4 = card("Hearts", 9)

player = player_hand()
cards = [card0, card1, card2, card3, card4]
player.givecards(cards)
dealer = dealer_hand()

calculateHand(dealer, player)