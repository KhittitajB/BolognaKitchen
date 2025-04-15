import pygame
import meals

class Chef:
    name = ""
    rarity = ""
    description = ""
    image_path = ""
    image = None

    def __init__(self):
        if self.image_path:
            self.image = pygame.image.load(self.image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (80, 120))

    def on_hand_evaluated(self, hand, score):
        pass

    def on_round_start(self, game_state):
        pass

    def on_card_played(self, card):
        pass

class ChefJohn(Chef):
    name = "Chef John"
    rarity = "Common"
    description = "+4 Mult"
    image_path = "BolognaKitchen/assets_chef/ChefJohn.png"

    def on_hand_evaluated(self, hand, score):
        score["mult"] += 4

# Suite jokers
class BuffedChef(Chef):
    name = "Buffed Chef"
    rarity = "Common"
    description = "Played Meat give +3 Mult when scored"
    image_path = "BolognaKitchen/assets_chef/ChefJohn.png"

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
    image_path = "BolognaKitchen/assets_chef/ChefJohn.png"

    def on_hand_evaluated(self, hand, score):
        if meals.evaluate_hand(hand) in [meals.feast, meals.feastcourse, meals.feastplatter]:
            score["score"] += 80
