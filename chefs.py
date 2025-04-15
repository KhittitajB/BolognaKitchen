class Chef:
    name = ""
    rarity = ""
    description = ""

    def __init__(self):
        pass

    def on_hand_evaluated(self, hand, score):
        pass

    def on_round_start(self, game_state):
        pass

    def on_card_played(self, card):
        pass

class ChefJohn(Chef):
    name = "Gold Joker"
    rarity = "Common"
    description = "+4 Mult"

    def on_hand_evaluated(self, hand, score):
        score["mult"] += 4

# Suite jokers
class BuffedChef(Chef):
    name = "Buffed Chef"
    rarity = "Common"
    description = "Played Meat give +3 Mult when scored"

    def on_hand_evaluated(self, hand, score):
        x = 0

        for i in hand:
            if i.suite == "meat":
                x += 1

        score["mult"] += (3*x)

# Hand jokers
class PickyChef(Chef):
    name = "Picky Chef"
    rarity = "Common"
    description = "+80 Score if played hand contains a Feast"

    def on_hand_evaluated(self, hand, score):
        if 
