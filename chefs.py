import pygame
import meals

pygame.init()

font = pygame.font.Font(None, 30)
small_font = pygame.font.Font(None, 20)

class Chef:
    name = ""
    rarity = ""
    description = ""
    image_path = ""
    price = 0
    image = None

    def __init__(self):
        if self.image_path:
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, (80, 120))

    def draw(self, surface, x, y, width=150, height=200, highlight=False):
        color = (220, 180, 120) if not highlight else (255, 215, 100)
        pygame.draw.rect(surface, color, (x, y, width, height))
        pygame.draw.rect(surface, (0, 0, 0), (x, y, width, height), 3)

        name_text = font.render(self.name, True, (0, 0, 0))
        effect_text = small_font.render(self.description, True, (50, 50, 50))

        surface.blit(name_text, (x + 10, y + 10))
        surface.blit(effect_text, (x + 10, y + 40))

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
    price = 2

    def on_hand_evaluated(self, hand, score):
        score["mult"] += 4

# Suite jokers
class BuffedChef(Chef):
    name = "Buffed Chef"
    rarity = "Common"
    description = "Played Meat give +3 Mult when scored"
    image_path = "BolognaKitchen/assets_chef/ChefJohn.png"
    price = 5

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
    price = 3

    def on_hand_evaluated(self, hand, score):
        if meals.evaluate_hand(hand) in [meals.feast, meals.feastcourse, meals.feastplatter]:
            score["score"] += 80


chef_list = [ChefJohn(), BuffedChef(), PickyChef()]
