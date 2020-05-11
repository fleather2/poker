from poker import *
import random

class character:
    def __init__(self, name="", money=0):
        self.name = name
        self.money = money

    def readmoney(self):
        return self.money

    def changemoney(self, money):
        self.money += money

def generateplayers(opponents=1):
    
    with open(f"opponents.txt") as f:
        names = f.readlines()
    names = [x.strip() for x in names]
    random.shuffle(names) 
    players = []
    for i in range(opponents):
        char = character(name=names[i], money=1000)
        player = player_hand(char=char)
        players.append(player)
    return players
    