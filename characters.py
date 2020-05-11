import poker

class character:
    def __init__(self, name="", money=0):
        self.name = name
        self.money = money

    def readmoney(self):
        return self.money

    def changemoney(self, money):
        self.money += money
