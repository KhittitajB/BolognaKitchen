import pygame
import random
import configs
import meals
import chefs

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
    base_y = configs.HEIGHT - configs.CARD_HEIGHT - 120
    spacing = 100

    for i, card in enumerate(h.hand):
        x = start_x + i * spacing
        y = base_y - 20 if card in hand.selected else base_y
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

def refill_hand():
    while len(hand.hand) < 8 and dp.pile:
        hand.add_to_hand(dp.pile.pop(random.randint(0, len(dp.pile) - 1)))

def draw_score_panel():
    score_text = font.render(f"Score: {current_score} / {goal_score}", True, (0, 0, 0))
    screen.blit(score_text, (configs.WIDTH // 2 - 50, 20))

    if hand.selected:
        recieved_hand = meals.evaluate_hand(hand.selected) # Recieves hand name for further calcs
        hand_text = font.render(f"Hand: {recieved_hand.name}", True, (0, 0, 0))
        screen.blit(hand_text, (configs.WIDTH // 2 - 50, 50))

# Played cards animation
def animate_cards_to_center(cards):
    frames = 15
    center_x = configs.WIDTH // 2 - configs.CARD_WIDTH // 2
    center_y = configs.HEIGHT // 2 - configs.CARD_HEIGHT // 2

    card_positions = []

    start_x = (configs.WIDTH - (len(hand.hand) * 100)) // 2
    y = configs.HEIGHT - configs.CARD_HEIGHT - 120
    spacing = 100

    for card in cards:
        i = hand.hand.index(card)
        x = start_x + i * spacing
        card_positions.append((x, y))

    for frame in range(frames):
        screen.blit(background_img, (0, 0))
        draw_hand(hand)
        draw_score_panel()
        draw_play_button()
        draw_draw_pile(dp)

        for i, card in enumerate(cards):
            start_x, start_y = card_positions[i]
            x = start_x + (center_x - start_x) * frame / frames
            y = start_y + (center_y - start_y) * frame / frames
            draw_card(x, y, card, selected=True)

        pygame.display.flip()
        pygame.time.delay(25)

def play_selected_cards():
    global current_score, game_won

    if not hand.selected:
        return

    animate_cards_to_center(hand.selected)

    hand_obj = meals.evaluate_hand(hand.selected)

    score_dict = {
        "score": hand_obj.score + sum(card.size for card in hand.selected),
        "mult": hand_obj.mult
    }

    for chef in active_chefs:
        chef.on_hand_evaluated(hand.selected, score_dict)

    added_score = score_dict["score"] * score_dict["mult"]
    current_score += added_score

    for card in hand.selected:
        hand.hand.remove(card)
    hand.selected.clear()

    if current_score >= goal_score:
        game_won = True

    refill_hand()

def draw_win_screen():
    screen.fill((0, 0, 0))
    win_text = font.render("You Win!", True, (255, 255, 0))
    win_rect = win_text.get_rect(center=(configs.WIDTH // 2, configs.HEIGHT // 2))
    screen.blit(win_text, win_rect)


dp = DrawPile()
hand = Hand()

for suite in ["meat", "veggie", "grains", "dairy"]:
    for i in range(1, 12):
        dp.add_to_pile(PlayingCard(i, suite))

for _ in range(8):
    hand.add_to_hand(dp.pile.pop(random.randint(0, len(dp.pile) - 1)))

chef_positions = []

def draw_chefs():
    chef_positions.clear()
    x = 20
    y = 40
    for chef in active_chefs:
        if chef.image:
            screen.blit(chef.image, (x, y))
        else:
            pygame.draw.rect(screen, (60, 60, 60), (x, y, 80, 80), border_radius=10)

        chef_positions.append((pygame.Rect(x, y, 120, 80), chef))

        x += 110

def draw_chef_tooltip():
    mouse_pos = pygame.mouse.get_pos()
    for rect, chef in chef_positions:
        if rect.collidepoint(mouse_pos):
            tooltip_width = 400
            tooltip_height = 60
            tooltip_x = rect.x
            tooltip_y = rect.y + rect.height + 10
            pygame.draw.rect(screen, (0, 0, 0), (tooltip_x, tooltip_y, tooltip_width, tooltip_height), border_radius=10)
            pygame.draw.rect(screen, (255, 255, 0), (tooltip_x, tooltip_y, tooltip_width, tooltip_height), 2, border_radius=10)

            name_text = font.render(chef.name, True, (255, 255, 0))
            desc_text = font.render(chef.description, True, (255, 255, 255))
            screen.blit(name_text, (tooltip_x + 10, tooltip_y + 5))
            screen.blit(desc_text, (tooltip_x + 10, tooltip_y + 30))

# Score System
goal_score = 100
current_score = 0
game_won = False

active_chefs = [chefs.ChefJohn(), chefs.BuffedChef(), chefs.PickyChef()]

running = True
while running:
    screen.blit(background_img, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_won and event.type == pygame.MOUSEBUTTONDOWN:
            clicked_card = get_clicked_card(hand, pygame.mouse.get_pos())

            if clicked_card:
                toggle_card_selection(clicked_card)

            play_rect = pygame.Rect(configs.WIDTH // 2 - 50, configs.HEIGHT - 50, 100, 40)
            if play_rect.collidepoint(pygame.mouse.get_pos()):
                play_selected_cards()

    if game_won:
        draw_win_screen()
    else:
        draw_hand(hand)
        draw_score_panel()
        draw_chefs()
        draw_chef_tooltip()
        draw_play_button()

    pygame.display.flip()

pygame.quit()
