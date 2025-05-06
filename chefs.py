import pygame
import meals
import configs

pygame.init()

screen = pygame.display.set_mode((configs.WIDTH, configs.HEIGHT))

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
        if self.image:
            screen.blit(self.image, (x, y))
        else:
            pygame.draw.rect(screen, (60, 60, 60), (x, y, 80, 80), border_radius=10)

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
    image_path = "BolognaKitchen/assets_chef/buffed_chef.png"
    price = 5

    def on_hand_evaluated(self, hand, score):
        x = 0

        for i in hand:
            if i.suite == "meat":
                x += 1

        score["mult"] += (3*x)

class KeenChef(Chef):
    name = "Keen Chef"
    rarity = "Common"
    description = "Played Veggies give +3 Mult when scored"
    image_path = "BolognaKitchen/assets_chef/keen_chef.png"
    price = 5

    def on_hand_evaluated(self, hand, score):
        x = 0

        for i in hand:
            if i.suite == "veggie":
                x += 1

        score["mult"] += (3*x)

class GrainyChef(Chef):
    name = "Grainy Chef"
    rarity = "Common"
    description = "Played Grains give +3 Mult when scored"
    image_path = "BolognaKitchen/assets_chef/grainy_chef.png"
    price = 5

    def on_hand_evaluated(self, hand, score):
        x = 0

        for i in hand:
            if i.suite == "grains":
                x += 1

        score["mult"] += (3*x)

class TallChef(Chef):
    name = "Tall Chef"
    rarity = "Common"
    description = "Played Dairy give +3 Mult when scored"
    image_path = "BolognaKitchen/assets_chef/tall_chef.png"
    price = 5

    def on_hand_evaluated(self, hand, score):
        x = 0

        for i in hand:
            if i.suite == "dairy":
                x += 1

        score["mult"] += (3*x)

# Hand jokers
class SmallChef(Chef):
    name = "Small Chef"
    rarity = "Common"
    description = "+50 Score if played hand contains a Small Platter"
    image_path = "BolognaKitchen/assets_chef/small_chef.png"
    price = 3

    def on_hand_evaluated(self, hand, score):
        if meals.evaluate_hand(hand) in [meals.smallplatter, meals.doublecourse, meals.mediumplatter, meals.fullcourse, meals.bigplatter, meals.enormousplatter, meals.feastcourse, meals.feastplatter]:
            score["score"] += 50

class BuddyChef(Chef):
    name = "Buddy Chef"
    rarity = "Common"
    description = "+80 Score if played hand contains a Double Course"
    image_path = "BolognaKitchen/assets_chef/buddy_chef.png"
    price = 3

    def on_hand_evaluated(self, hand, score):
        if meals.evaluate_hand(hand) in [meals.doublecourse, meals.fullcourse, meals.feastcourse]:
            score["score"] += 80

class MediocreChef(Chef):
    name = "Mediocre Chef"
    rarity = "Common"
    description = "+100 Score if played hand contains a Medium Platter"
    image_path = "BolognaKitchen/assets_chef/mediocre_chef.png"
    price = 3

    def on_hand_evaluated(self, hand, score):
        if meals.evaluate_hand(hand) in [meals.mediumplatter, meals.fullcourse, meals.bigplatter, meals.enormousplatter, meals.feastcourse, meals.feastplatter]:
            score["score"] += 100

class OldChef(Chef):
    name = "Old Chef"
    rarity = "Common"
    description = "+100 Score if played hand contains a Signature"
    image_path = "BolognaKitchen/assets_chef/old_chef.png"
    price = 3

    def on_hand_evaluated(self, hand, score):
        if meals.evaluate_hand(hand) in [meals.signature, meals.chefspecial]:
            score["score"] += 100

class PickyChef(Chef):
    name = "Picky Chef"
    rarity = "Common"
    description = "+80 Score if played hand contains a Feast"
    image_path = "BolognaKitchen/assets_chef/picky_chef.png"
    price = 3

    def on_hand_evaluated(self, hand, score):
        if meals.evaluate_hand(hand) in [meals.feast, meals.feastcourse, meals.feastplatter]:
            score["score"] += 80

class BigChef(Chef):
    name = "Big Chef"
    rarity = "Common"
    description = "+200 Score if played hand contains a Big Platter"
    image_path = "BolognaKitchen/assets_chef/big_chef.png"
    price = 3

    def on_hand_evaluated(self, hand, score):
        if meals.evaluate_hand(hand) in [meals.bigplatter, meals.enormousplatter, meals.feastplatter]:
            score["score"] += 200


chef_list = [ChefJohn(), BuffedChef(), KeenChef(), GrainyChef(), TallChef(), SmallChef(), BuddyChef(), MediocreChef(), OldChef(), PickyChef(), BigChef()]
