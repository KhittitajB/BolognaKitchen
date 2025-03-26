import pygame
import random
import configs

class PlayingCard:
    def __init__(self, size, suite):
        if size in [1,2,3,4,5,6,7,8,9,10,11]:
            self.size = size             # Acts like rank in Balatro
        else:
            raise ValueError(f"Invalid card size: {size}")
        if suite.lower() in ["meat","veggie","grains","dairy"]:
            self.suite = suite.lower()   # Acts like suite in Balatro
            self.image = configs.SUITE_IMAGES[self.suite]
        else:
            raise ValueError(f"Invalid card size: {suite}")

    def __repr__(self):
        return f"{self.size} of {self.suite}"

class DrawPile:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DrawPile, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "pile"):
            self.pile = []

    def add_to_pile(self, item):
        self.pile.append(item)

    def show_pile(self):
        for c in self.pile:
            print(c)

class Hand:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Hand, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "hand"):
            self.hand = []
            self.selected = []

    def add_to_hand(self, item):
        self.hand.append(item)

    # to debug
    def __repr__(self):
        return f"{self.hand}"


dp = DrawPile()
hand = Hand()

for i in range(11):
    m = PlayingCard(i+1, "meat")
    dp.pile.append(m)

for i in range(11):
    v = PlayingCard(i+1, "veggie")
    dp.pile.append(v)

for i in range(11):
    g = PlayingCard(i+1, "grains")
    dp.pile.append(g)

for i in range(11):
    d = PlayingCard(i+1, "dairy")
    dp.pile.append(d)


# MAIN
pygame.init()

screen = pygame.display.set_mode((configs.WIDTH, configs.HEIGHT))
pygame.display.set_caption("Bologna Kitchen")

background_img = configs.background
background_img = pygame.transform.scale(background_img, (configs.WIDTH, configs.HEIGHT))

font = pygame.font.Font(None, 30)

def draw_card(x, y, card, selected=False):
    border_color = (0, 255, 0) if selected else (200, 50, 50)
    pygame.draw.rect(screen, border_color, (x, y, configs.CARD_WIDTH, configs.CARD_HEIGHT), border_radius=10)
    screen.blit(card.image, (x, y))

    text_surface = font.render(str(card.size), True, (255, 255, 255))
    screen.blit(text_surface, (x + 10, y + 10))

def draw_hand(h):
    start_x = (configs.WIDTH - (len(h.hand) * 100)) // 2
    y = configs.HEIGHT - configs.CARD_HEIGHT - 120
    spacing = 100

    for i, card in enumerate(h.hand):
        x = start_x + i * spacing
        draw_card(x, y, card, selected=(card in hand.selected))

def draw_button():
    mouse_pos = pygame.mouse.get_pos()
    color = configs.BUTTON_HOVER if configs.BUTTON_RECT.collidepoint(mouse_pos) else configs.BUTTON_COLOR
    pygame.draw.rect(screen, color, configs.BUTTON_RECT, border_radius=10)
    text_surface = font.render("Play", True, configs.WHITE)
    screen.blit(text_surface, (configs.BUTTON_RECT.x + 25, configs.BUTTON_RECT.y + 10))

def toggle_card_selection(card):
    if card in hand.selected:
        hand.selected.remove(card)
    elif len(hand.selected) < 5:
        hand.selected.append(card)

def draw_draw_pile(draw_pile):
    x = configs.WIDTH - 150
    y = configs.HEIGHT - configs.CARD_HEIGHT - 20
    screen.blit(configs.draw_pile_img, (x, y))

    font = pygame.font.Font(None, 40)
    text_surface = font.render(str(len(draw_pile.pile)), True, configs.WHITE)
    screen.blit(text_surface, (x + 30, y + 40))

def draw_play_button():
    play_rect = pygame.Rect(configs.WIDTH // 2 - 50, configs.HEIGHT - 50, 100, 40)
    pygame.draw.rect(screen, (0, 0, 255), play_rect)
    text_surface = font.render("Play", True, configs.WHITE)
    screen.blit(text_surface, (configs.WIDTH // 2 - 20, configs.HEIGHT - 40))
    return play_rect

def get_clicked_card(hand, mouse_pos):
    start_x = (configs.WIDTH - (len(hand.hand) * 100)) // 2
    y = configs.HEIGHT - configs.CARD_HEIGHT - 120
    spacing = 100

    for i, card in enumerate(hand.hand):
        x = start_x + i * spacing
        card_rect = pygame.Rect(x, y, configs.CARD_WIDTH, configs.CARD_HEIGHT)

        if card_rect.collidepoint(mouse_pos):
            return card
    return None

def play_selected_cards():
    global current_score

    if not hand.selected:
        return

    multiplier, hand_name = evaluate_hand(hand.selected)

    hand_score = sum(card.size for card in hand.selected) * multiplier
    current_score += int(hand_score)

    print(f"Played: {hand_name}! Score: +{int(hand_score)}")

    for card in hand.selected:
        hand.hand.remove(card)
    hand.selected.clear()

    refill_hand()

def evaluate_hand(cards):
    size_counts = {}
    suite_counts = {}

    for card in cards:
        size_counts[card.size] = size_counts.get(card.size, 0) + 1
        suite_counts[card.suite] = suite_counts.get(card.suite, 0) + 1

    values = sorted(size_counts.values(), reverse=True)

    # Hand Ranking (Balatro-style) - Returns number + hand name
    if 5 in values:
        return 10, "Five of a Kind"
    if 4 in values:
        return 6, "Four of a Kind"
    if 3 in values and 2 in values:
        return 5, "Full House"
    if 3 in values:
        return 3, "Three of a Kind"
    if values.count(2) == 2:
        return 2, "Two Pair"
    if 2 in values:
        return 1.5, "Pair"
    if len(set(card.suite for card in cards)) == 1:
        return 4, "Flush"

    return 1, "High Card"

def refill_hand():
    while len(hand.hand) < 8 and dp.pile:
        hand.add_to_hand(dp.pile.pop(random.randint(0, len(dp.pile) - 1)))

def draw_score_panel():
    score_text = font.render(f"Score: {current_score} / {goal_score}", True, (0, 0, 0))
    screen.blit(score_text, (configs.WIDTH // 2 - 50, 20))

    if hand.selected:
        _, hand_name = evaluate_hand(hand.selected) # Recieves number + hand name
        hand_text = font.render(f"Hand: {hand_name}", True, (0, 0, 0))
        screen.blit(hand_text, (configs.WIDTH // 2 - 50, 50))


dp = DrawPile()
hand = Hand()

for suite in ["meat", "veggie", "grains", "dairy"]:
    for i in range(1, 12):
        dp.add_to_pile(PlayingCard(i, suite))

for _ in range(8):
    hand.add_to_hand(dp.pile.pop(random.randint(0, len(dp.pile) - 1)))

# Score System
goal_score = 50
current_score = 0

running = True
while running:
    screen.blit(background_img, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_card = get_clicked_card(hand, pygame.mouse.get_pos())

            if clicked_card:
                toggle_card_selection(clicked_card)

            play_rect = pygame.Rect(configs.WIDTH // 2 - 50, configs.HEIGHT - 50, 100, 40)
            if play_rect.collidepoint(pygame.mouse.get_pos()):
                play_selected_cards()

    draw_hand(hand)
    draw_score_panel()
    draw_play_button()

    pygame.display.flip()

pygame.quit()
