import pygame

WIDTH, HEIGHT = 1200,800
WHITE = (255, 255, 255)
CARD_WIDTH, CARD_HEIGHT = 80, 120
CARD_COLOR = (200, 50, 50)

BUTTON_COLOR = (50, 200, 50)
BUTTON_HOVER = (30, 180, 30)
BUTTON_RECT = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 60, 100, 40)

meat_img = pygame.image.load("BolognaKitchen/assets/minecraft_pork.png")
veggie_img = pygame.image.load("BolognaKitchen/assets/minecraft_carrot.png")
grains_img = pygame.image.load("BolognaKitchen/assets/minecraft_wheat.png")
dairy_img = pygame.image.load("BolognaKitchen/assets/minecraft_milk.png")

background = pygame.image.load("BolognaKitchen/assets/kitchen.png")

meat_img = pygame.transform.scale(meat_img, (CARD_WIDTH, CARD_HEIGHT))
veggie_img = pygame.transform.scale(veggie_img, (CARD_WIDTH, CARD_HEIGHT))
grains_img = pygame.transform.scale(grains_img, (CARD_WIDTH, CARD_HEIGHT))
dairy_img = pygame.transform.scale(dairy_img, (CARD_WIDTH, CARD_HEIGHT))

draw_pile_img = pygame.image.load("BolognaKitchen/assets/card_back.png")
draw_pile_img = pygame.transform.scale(draw_pile_img, (CARD_WIDTH, CARD_HEIGHT))

SUITE_IMAGES = {
    "meat": meat_img,
    "veggie": veggie_img,
    "grains": grains_img,
    "dairy": dairy_img
}
