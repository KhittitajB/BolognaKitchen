import pygame
import random
import copy
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


# MAIN
pygame.init()

screen = pygame.display.set_mode((configs.WIDTH, configs.HEIGHT))
pygame.display.set_caption("Bologna Kitchen")

background_img = configs.background
background_img = pygame.transform.scale(background_img, (configs.WIDTH, configs.HEIGHT))

small_font = pygame.font.Font(None, 20)
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

# NOT USED RIGHT NOW
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
    screen.blit(text_surface, (configs.WIDTH // 2 - 22, configs.HEIGHT - 40))
    return play_rect

def draw_discard_button():
    discard_rect = pygame.Rect(configs.WIDTH // 2 - 50, configs.HEIGHT - 100, 100, 40)
    pygame.draw.rect(screen, (255, 0, 0), discard_rect)
    text_surface = font.render("Discard", True, configs.WHITE)
    screen.blit(text_surface, (configs.WIDTH // 2 - 38, configs.HEIGHT - 90))
    return discard_rect

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
    if not dp.pile and len(hand.hand) < 8:
        print("Draw pile empty and hand incomplete. Transitioning to shop or ending round.")
        global game_lost
        game_lost = True
        return

    while len(hand.hand) < 8 and dp.pile:
        hand.add_to_hand(dp.pile.pop(random.randint(0, len(dp.pile) - 1)))

def draw_score_panel():
    score_text = font.render(f"Score: {current_score} / {goal_score}", True, (0, 0, 0))
    screen.blit(score_text, (configs.WIDTH // 2 - 50, 20))

    if hand.selected:
        recieved_hand = meals.evaluate_hand(hand.selected) # Recieves hand name for further calcs
        hand_text = font.render(f"{recieved_hand.name}", True, (0, 0, 0))
        screen.blit(hand_text, (configs.WIDTH // 2 - 50, 50))
    discard_text = font.render(f"Discards {discards_left}", True, (0, 0, 0))
    plays_text = font.render(f"Hands {plays_left}", True, (0, 0, 0))
    screen.blit(plays_text, (configs.WIDTH // 2 - 50, 90))
    screen.blit(discard_text, (configs.WIDTH // 2 - 50, 110))

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

        for i, card in enumerate(cards):
            start_x, start_y = card_positions[i]
            x = start_x + (center_x - start_x) * frame / frames
            y = start_y + (center_y - start_y) * frame / frames
            draw_card(x, y, card, selected=True)

        pygame.display.flip()
        pygame.time.delay(25)

def play_selected_cards():
    global current_score, game_won, plays_left

    if plays_left <= 0:
        return

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

    plays_left -= 1

    if current_score >= goal_score:
        game_won = True

    print("# Cards in Pile:", len(dp.pile))
    print("Remaining Cards in Pile:", dp.pile)
    # DEBUG LINE
    refill_hand()

def discard():
    global discards_left

    if plays_left <= 0:
        return

    if not hand.selected:
        return

    for card in hand.selected:
        hand.hand.remove(card)
    hand.selected.clear()

    discards_left -= 1

    refill_hand()

def draw_money():
    money_text = font.render(f"${current_money}", True, (255, 255, 0))
    text_rect = money_text.get_rect(bottomright=(40, configs.HEIGHT - 20))
    screen.blit(money_text, text_rect)

# REWORK THIS
def draw_win_screen():
    screen.fill((0, 0, 0))
    win_text = font.render("You Win!", True, (255, 255, 0))
    win_rect = win_text.get_rect(center=(configs.WIDTH // 2, configs.HEIGHT // 2))
    screen.blit(win_text, win_rect)

# REWORK THIS
def draw_lose_screen():
    screen.fill((0, 0, 0))
    win_text = font.render("You Lose!", True, (255, 0, 0))
    win_rect = win_text.get_rect(center=(configs.WIDTH // 2, configs.HEIGHT // 2))
    screen.blit(win_text, win_rect)

    restart_button = pygame.Rect(configs.WIDTH // 2 - 60, configs.HEIGHT // 2 + 20, 120, 40)
    pygame.draw.rect(screen, (0, 100, 200), restart_button, border_radius=10)
    restart_text = font.render("Restart", True, (255, 255, 255))
    screen.blit(restart_text, (restart_button.x + 15, restart_button.y + 8))

    return restart_button

def open_shop():
    global shop_chefs, spices, shop_prices, shop

    shop = True
    shop_chefs = random.sample(chefs.chef_list, 3)
    shop_prices = [x.price for x in shop_chefs]

if 'shop_spices' not in globals():
    shop_spices = random.sample(list(meals.all_meals.items()), 2)
    spice_purchased = [False, False]


def draw_shop():
    global spice_rects

    screen.fill((240, 230, 200))

    shop_text = font.render("Chef Shop", True, (0, 0, 0))
    screen.blit(shop_text, (configs.WIDTH // 2 - shop_text.get_width() // 2, 50))

    for i, chef_instance in enumerate(shop_chefs):
        x = 100 + i * 200
        y = 150
        price = shop_prices[i]
        try:
            chef_instance.draw(screen, x, y)
            price_text = small_font.render(f"${price}", True, (0, 0, 0))
            screen.blit(price_text, (x + 50, y + 170))
        except:
            return

        if getattr(chef_instance, 'purchased', False):
            overlay = pygame.Surface((100, 150), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            screen.blit(overlay, (x, y))

    spice_rects = []
    for i, spice_name in enumerate(shop_spices):
        x = 750
        y = 150 + i * 200
        rect = pygame.Rect(x, y, 120, 160)
        spice_rects.append(rect)
        print(spice_rects)

        pygame.draw.rect(screen, (200, 100, 50), rect, border_radius=10)
        name_text = small_font.render(spice_name[0], True, (255, 255, 255))
        screen.blit(name_text, (x + 10, y + 20))

        price_text = small_font.render("$10", True, (255, 255, 255))
        screen.blit(price_text, (x + 35, y + 130))

        if spice_purchased[i]:
            overlay = pygame.Surface((120, 160), pygame.SRCALPHA)
            overlay.fill((50, 50, 50, 180))
            screen.blit(overlay, (x, y))

    cont_button = pygame.Rect(configs.WIDTH // 2 - 50, configs.HEIGHT - 60, 100, 40)
    pygame.draw.rect(screen, (0, 100, 200), cont_button)
    cont_text = font.render("Continue", True, (255, 255, 255))
    screen.blit(cont_text, (cont_button.x + 10, cont_button.y + 10))

    draw_money()

    return spice_rects, cont_button

def reset_game():
    global current_score, plays_left, discards_left, game_lost, game_won, current_money, goal_score
    goal_score = 100
    current_score = 0
    plays_left = max_plays_per_round
    discards_left = max_discards_per_round
    game_lost = False
    game_won = False
    current_money = 0
    active_chefs.clear()
    hand.hand.clear()
    hand.selected.clear()
    reset_dp()
    refill_hand()


dp = DrawPile()
hand = Hand()

for suite in ["meat", "veggie", "grains", "dairy"]:
    for i in range(1, 12):
        dp.add_to_pile(PlayingCard(i, suite))

# RESET DECK AFTER SHOP
def reset_dp():
    dp.pile = []
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

def draw_title_screen():
    screen.fill((30, 30, 30))

    title_text = font.render("Bologna Kitchen", True, (255, 255, 0))
    start_text = font.render("Click to Start", True, (255, 255, 255))

    title_rect = title_text.get_rect(center=(configs.WIDTH // 2, configs.HEIGHT // 2 - 40))
    start_rect = start_text.get_rect(center=(configs.WIDTH // 2, configs.HEIGHT // 2 + 40))

    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)

# Score System
title_screen = True

goal_score = 100
current_score = 0
game_won = False
shop = False

game_lost = False

max_plays_per_round = 4
plays_left = max_plays_per_round
max_discards_per_round = 3
discards_left = max_discards_per_round

last_meal_score = 0
last_meal_name = ""

current_money = 0
phase = 1

active_chefs = []

running = True
while running:
    if title_screen:
        draw_title_screen()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                title_screen = False

        continue

    screen.blit(background_img, (0,0))

    if shop:
        draw_shop()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Chefs
                for i in range(len(shop_chefs)):
                    x = 100 + i * 200
                    y = 150
                    box_rect = pygame.Rect(x, y, 150, 200)
                    if box_rect.collidepoint(mouse_x, mouse_y):
                        price = shop_prices[i]
                        if price != None and current_money >= price:
                            current_money -= price
                            new_chef = shop_chefs[i]
                            active_chefs.append(new_chef)
                            print(f"Bought {new_chef.name}!")
                            shop_prices[i] = None
                            shop_chefs[i] = None

                # Spices
                for i, rect in enumerate(spice_rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        if not spice_purchased[i] and current_money >= 10:
                            current_money -= 10
                            spice_purchased[i] = True
                            spice_name, spice_func = shop_spices[i]
                            spice_func.level_up()
                            print(f"Used {spice_name} spice!")

                cont_button = pygame.Rect(configs.WIDTH // 2 - 50, configs.HEIGHT - 60, 100, 40)
                if cont_button.collidepoint(mouse_x, mouse_y):
                    shop = False
                    refill_hand()
            continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_won and event.type == pygame.MOUSEBUTTONDOWN:
            clicked_card = get_clicked_card(hand, pygame.mouse.get_pos())

            if clicked_card:
                toggle_card_selection(clicked_card)

            play_rect = pygame.Rect(configs.WIDTH // 2 - 50, configs.HEIGHT - 50, 100, 40)
            if play_rect.collidepoint(pygame.mouse.get_pos()) and plays_left > 0:
                play_selected_cards()

            discard_rect = pygame.Rect(configs.WIDTH // 2 - 50, configs.HEIGHT - 100, 100, 40)
            if discard_rect.collidepoint(pygame.mouse.get_pos()) and discards_left > 0:
                discard()

    if game_won and not shop:
        reset_dp()

        if phase == 4:
            phase = 1

        if phase == 1:
            current_money += 3
        elif phase == 2:
            current_money += 4
        elif phase == 3:
            current_money += 5

        current_money += plays_left
        plays_left = max_plays_per_round
        discards_left = max_discards_per_round

        phase += 1
        current_score = 0
        goal_score += int(200 * 1.5 * phase)

        open_shop()
        shop = True

        game_won = False

    else:
        draw_hand(hand)
        draw_score_panel()
        draw_chefs()
        draw_chef_tooltip()
        draw_play_button()
        draw_discard_button()
        draw_money()

    if plays_left == 0 and not game_won:
        game_lost = True

    if game_lost:
        restart_button = draw_lose_screen()
        if event.type == pygame.MOUSEBUTTONDOWN and restart_button.collidepoint(pygame.mouse.get_pos()):
            reset_game()
        pygame.display.flip()

    pygame.display.flip()

pygame.quit()
