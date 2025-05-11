import pygame
import random
import configs
import meals
import chefs
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import threading
import datetime
import os

from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

# Click Sound
click_sound = pygame.mixer.Sound("assets/select_card.mp3")

def get_clicked_card(hand, mouse_pos):
    start_x = (configs.WIDTH - (len(hand.hand) * 100)) // 2
    y = configs.HEIGHT - configs.CARD_HEIGHT - 120
    spacing = 100

    for i, card in enumerate(hand.hand):
        x = start_x + i * spacing
        card_rect = pygame.Rect(x, y, configs.CARD_WIDTH, configs.CARD_HEIGHT)

        if card_rect.collidepoint(mouse_pos):
            pygame.mixer.music.set_volume(volume)
            click_sound.set_volume(volume)
            click_sound.play()
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
    score_text = font.render(f"Score: {current_score} / {goal_score}", True, (0,0,0))
    screen.blit(score_text, (configs.WIDTH // 2 - 50, 20))

    if hand.selected:
        recieved_hand = meals.evaluate_hand(hand.selected) # Recieves hand name for further calcs
        hand_text = font.render(f"{recieved_hand.name}", True, (0,0,0))
        screen.blit(hand_text, (configs.WIDTH // 2 - 50, 50))
    discard_text = font.render(f"Discards {discards_left}", True, (0,0,0))
    plays_text = font.render(f"Hands {plays_left}", True, (0,0,0))
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

def log_hand_to_csv(hand_name, score):
    new_row = {"Timestamp": datetime.datetime.now().isoformat(), "Hand": hand_name, "Score": score}
    file_path = "data/hands_played.csv"

    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        df = pd.DataFrame([new_row])
        df.to_csv(file_path, index=False)
    else:
        df = pd.read_csv(file_path)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(file_path, index=False)

def log_played_to_csv(cards):
    file_path = "data/cards_played.csv"
    rows = []

    for card in cards:
        rows.append({
            "Timestamp": datetime.datetime.now().isoformat(),
            "Card Suite": card.suite,
            "Value": card.size
        })

    df = pd.DataFrame(rows)

    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        df.to_csv(file_path, index=False)
    else:
        existing_df = pd.read_csv(file_path)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.to_csv(file_path, index=False)

def log_discarded_to_csv(cards):
    file_path = "data/cards_discarded.csv"
    rows = []

    for card in cards:
        rows.append({
            "Timestamp": datetime.datetime.now().isoformat(),
            "Card Suite": card.suite,
            "Value": card.size
        })

    df = pd.DataFrame(rows)

    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        df.to_csv(file_path, index=False)
    else:
        existing_df = pd.read_csv(file_path)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.to_csv(file_path, index=False)

def play_selected_cards():
    global current_score, game_won, plays_left, highest_hand

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
    log_hand_to_csv(hand_obj.name ,added_score)
    log_played_to_csv(hand.selected)

    for card in hand.selected:
        hand.hand.remove(card)
    hand.selected.clear()

    plays_left -= 1

    if current_score >= goal_score:
        game_won = True

    if current_score > highest_hand:
        highest_hand = current_score

    # print("# Cards in Pile:", len(dp.pile))
    # print("Remaining Cards in Pile:", dp.pile)
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
    log_discarded_to_csv(hand.selected)
    hand.selected.clear()

    discards_left -= 1

    refill_hand()

def draw_money():
    money_text = font.render(f"${current_money}", True, (255, 255, 0))
    text_rect = money_text.get_rect(bottomright=(40, configs.HEIGHT - 20))
    screen.blit(money_text, text_rect)

def draw_lose_screen():
    lose_screen_bg = pygame.image.load("assets/lose_screen.png").convert()
    lose_screen_bg = pygame.transform.scale(lose_screen_bg, (configs.WIDTH, configs.HEIGHT))

    screen.blit(lose_screen_bg, (0, 0))

    win_text = font.render("You Lose!", True, (255, 0, 0))
    win_rect = win_text.get_rect(center=(configs.WIDTH // 2, configs.HEIGHT // 2))
    screen.blit(win_text, win_rect)

    restart_button = pygame.Rect(configs.WIDTH // 2 - 60, configs.HEIGHT // 2 + 20, 120, 40)
    pygame.draw.rect(screen, (0, 100, 200), restart_button, border_radius=10)
    restart_text = font.render("Restart", True, (255, 255, 255))
    screen.blit(restart_text, (restart_button.x + 15, restart_button.y + 8))

    high_score_text = small_font.render(f"Highest Hand: {highest_hand}", True, (255, 255, 255))
    screen.blit(high_score_text, ((configs.WIDTH // 2) - 55, (configs.HEIGHT // 2) + 100))

    high_score_text = small_font.render(f"Highest Round: {highest_round}", True, (255, 255, 255))
    screen.blit(high_score_text, ((configs.WIDTH // 2) - 55, (configs.HEIGHT // 2) + 120))

    return restart_button

if 'shop_spices' not in globals():
    shop_spices = random.sample(list(meals.all_meals.items()), 2)
    spice_purchased = [False, False]

def open_shop():
    global shop_chefs, shop_prices, shop, shop_spices, spice_purchased

    shop = True
    shop_chefs = random.sample(chefs.chef_list, 3)
    shop_prices = [x.price for x in shop_chefs]

    shop_spices = random.sample(list(meals.all_meals.items()), 2)
    spice_purchased = [False, False]


shop_background_img = pygame.image.load("assets/freezer.png").convert()
shop_background_img = pygame.transform.scale(shop_background_img, (configs.WIDTH, configs.HEIGHT))

def draw_shop():
    global spice_rects, reroll_button

    screen.blit(shop_background_img, (0, 0))

    shop_text = font.render("Chef Shop", True, (0, 0, 0))
    screen.blit(shop_text, (configs.WIDTH // 2 - shop_text.get_width() // 2, 50))

    for i, chef_instance in enumerate(shop_chefs):
        if chef_instance is None:
            continue

        x = 100 + i * 200
        y = 150
        price = shop_prices[i]

        chef_instance.draw(screen, x, y)
        price_text = small_font.render(f"${price}", True, (0, 0, 0))
        screen.blit(price_text, (x + 50, y + 170))

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

        pygame.draw.rect(screen, (200, 100, 50), rect, border_radius=10)
        name_text = small_font.render(spice_name[0], True, (255, 255, 255))
        screen.blit(name_text, (x + 10, y + 20))

        price_text = small_font.render("$5", True, (255, 255, 255))
        screen.blit(price_text, (x + 35, y + 130))

        if spice_purchased[i]:
            overlay = pygame.Surface((120, 160), pygame.SRCALPHA)
            overlay.fill((50, 50, 50, 180))
            screen.blit(overlay, (x, y))

    cont_button = pygame.Rect(configs.WIDTH // 2 - 50, configs.HEIGHT - 60, 100, 40)
    pygame.draw.rect(screen, (0, 100, 200), cont_button)
    cont_text = font.render("Continue", True, (255, 255, 255))
    screen.blit(cont_text, (cont_button.x + 10, cont_button.y + 10))

    reroll_button = pygame.Rect(configs.WIDTH // 2 - 60, configs.HEIGHT - 110, 120, 40)
    pygame.draw.rect(screen, (200, 50, 50), reroll_button, border_radius=10)
    reroll_text = font.render("Reroll ($3)", True, (255, 255, 255))
    screen.blit(reroll_text, (reroll_button.x + 5, reroll_button.y + 8))

    draw_money()

    mouse_x, mouse_y = pygame.mouse.get_pos()
    for i, chef in enumerate(shop_chefs):
        x = 100 + i * 200
        y = 150
        box_rect = pygame.Rect(x, y, 150, 200)

        if chef and box_rect.collidepoint(mouse_x, mouse_y):
            draw_chef_tooltip(chef, mouse_x, mouse_y)

    return spice_rects, cont_button, reroll_button

def draw_chef_tooltip(chef, x, y):
    tooltip_width = 380
    tooltip_height = 80
    tooltip_rect = pygame.Rect(x + 10, y + 10, tooltip_width, tooltip_height)

    pygame.draw.rect(screen, (255, 255, 240), tooltip_rect)
    pygame.draw.rect(screen, (0, 0, 0), tooltip_rect, 2)

    name_text = small_font.render(chef.name, True, (0, 0, 0))
    screen.blit(name_text, (tooltip_rect.x + 10, tooltip_rect.y + 10))

    if hasattr(chef, "description"):
        desc_text = small_font.render(chef.description, True, (0, 0, 0))
        screen.blit(desc_text, (tooltip_rect.x + 10, tooltip_rect.y + 40))

def generate_shop_chefs():
    new_chefs = [random.choice(chefs.chef_list) for _ in range(3)]
    new_prices = [chef.price for chef in new_chefs]
    return new_chefs, new_prices

def reset_game():
    global current_score, plays_left, discards_left, game_lost, game_won, current_money, goal_score, highest_hand
    goal_score = 100
    highest_hand = 0
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

numeric_files = ["data/cards_played.csv",
             "data/cards_discarded.csv",
             "data/chef_bought.csv"]

string_files = ["data/hands_played.csv",
             "data/shop_activities.csv"]

def open_tk_window_with_tabs():
    root = tk.Tk()
    root.title("Data Visualization")
    root.geometry("800x600")

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    for file_path in numeric_files:
        try:
            df = pd.read_csv(file_path)
            numeric_columns = df.select_dtypes(include='number').columns

            if numeric_columns.empty:
                continue

            column = numeric_columns[0]

            tab = ttk.Frame(notebook)
            notebook.add(tab, text=file_path.split("/")[-1])

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.hist(df[column], bins=10, color="skyblue", edgecolor="black")
            ax.set_title(f"Histogram of {column}")

            canvas = FigureCanvasTkAgg(fig, master=tab)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            print(f"Failed to process {file_path}: {e}")

    for file_path in string_files:
        try:
            df = pd.read_csv(file_path)
            string_col = df.select_dtypes(include='object').columns

            if string_col.empty:
                continue

            column = string_col[1]

            tab = ttk.Frame(notebook)
            notebook.add(tab, text=file_path.split("/")[-1])

            counts = df[column].value_counts()

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
            ax.set_title(f"Pie Chart of {column}")
            ax.axis("equal")

            canvas = FigureCanvasTkAgg(fig, master=tab)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            print(f"Failed to process {file_path}: {e}")

    quit_button = tk.Button(root, text="Quit", command=root.destroy)
    quit_button.pack(pady=10)

    root.mainloop()


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
    chef_rects = []
    for i, chef in enumerate(active_chefs):
        x = 70 + i * 90
        y = 20
        chef.draw(screen, x, y)
        rect = pygame.Rect(x, y, 150, 200)
        chef_rects.append((rect, chef))
    return chef_rects

def draw_title_screen():
    title_img = pygame.image.load("assets/title.png").convert()
    title_img = pygame.transform.scale(title_img, (configs.WIDTH, configs.HEIGHT))
    screen.blit(title_img, (0, 0))

# Music
pygame.mixer.init()
pygame.mixer.music.load("assets/orchestra.mp3")
volume = 0.5
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)

# Score System
title_screen = True

highest_hand = 0
highest_round = 0

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

current_money = 3
phase = 1

active_chefs = []

# SCREEN MANAGERS

# Title
def handle_title_screen(events):
    global title_screen
    draw_title_screen()

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            title_screen = False

buy_sound = pygame.mixer.Sound("assets/buy_chef.mp3")

def log_chef_to_csv(chef):
    file_path = "data/chef_bought.csv"
    row = {
        "Timestamp": datetime.datetime.now().isoformat(),
        "Chef Name": chef.name,
        "Rarity": chef.rarity,
        "Price": chef.price
    }

    df = pd.DataFrame([row])

    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        df.to_csv(file_path, index=False)
    else:
        existing_df = pd.read_csv(file_path)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.to_csv(file_path, index=False)

def log_shop_activity(action_type):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        'timestamp': timestamp,
        'action': action_type,
    }

    try:
        df = pd.read_csv("data/shop_activities.csv")
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([entry])
    except pd.errors.EmptyDataError:
        df = pd.DataFrame([entry])

    df.to_csv("data/shop_activities.csv", index=False)

# Shop
def handle_shop(events):
    global shop, current_money, shop_chefs, shop_prices

    screen.blit(background_img, (0, 0))
    draw_shop()

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            pygame.mixer.music.set_volume(volume)
            buy_sound.set_volume(volume)

            # Chefs
            for i in range(len(shop_chefs)):
                x = 100 + i * 200
                y = 150
                box_rect = pygame.Rect(x, y, 150, 200)
                if box_rect.collidepoint(mouse_x, mouse_y):
                    price = shop_prices[i]
                    if price is not None and current_money >= price:
                        if len(active_chefs) < 5:
                            buy_sound.play()
                            current_money -= price
                            new_chef = shop_chefs[i]
                            active_chefs.append(new_chef)
                            log_chef_to_csv(new_chef)
                            log_shop_activity("Buy Chef")
                            print(f"Bought {new_chef.name}!")
                            shop_prices[i] = None
                            shop_chefs[i] = None
                        else:
                            print("You already have the maximum number of chefs!")

            # Spices
            for i, rect in enumerate(spice_rects):
                if rect.collidepoint(mouse_x, mouse_y):
                    if not spice_purchased[i] and current_money >= 5:
                        buy_sound.play()
                        current_money -= 5
                        spice_purchased[i] = True
                        spice_name, spice_func = shop_spices[i]
                        log_shop_activity("Buy Spice")
                        spice_func.level_up()
                        print(f"Used {spice_name} spice!")

            cont_button = pygame.Rect(configs.WIDTH // 2 - 50, configs.HEIGHT - 60, 100, 40)
            if cont_button.collidepoint(mouse_x, mouse_y):
                shop = False
                refill_hand()

            if reroll_button.collidepoint(mouse_x, mouse_y) and current_money >= 3:
                buy_sound.play()
                current_money -= 3
                shop_chefs, shop_prices = generate_shop_chefs()
                log_shop_activity("Reroll Shop")

# Main Game
def handle_gameplay(events):
    global plays_left, discards_left, game_won, game_lost, chef_click_rects, current_money

    screen.blit(background_img, (0, 0))

    mouse_pos = pygame.mouse.get_pos()
    hovered_chef = None

    info1 = font.render("Press 'P' to view data window", True, (255, 255, 255))
    info2 = font.render("Press H to check hand levels", True, (255, 255, 255))
    info3 = font.render("Press 1 and 2 to sort cards", True, (255, 255, 255))
    screen.blit(info1, (configs.WIDTH - info1.get_width() - 10, 10))
    screen.blit(info2, (configs.WIDTH - info2.get_width() - 10, 40))
    screen.blit(info3, (configs.WIDTH - info3.get_width() - 10, 70))


    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_card = get_clicked_card(hand, pygame.mouse.get_pos())

            if not shop and not title_screen:
                for rect, chef in chef_click_rects:
                    if rect.collidepoint(mouse_pos):
                        if chef in active_chefs:
                            refund = chef.price // 2
                            current_money += refund
                            print(f"Sold {chef.name} for ${refund}")
                            active_chefs.remove(chef)

            if clicked_card:
                toggle_card_selection(clicked_card)

            play_rect = pygame.Rect(configs.WIDTH // 2 - 50, configs.HEIGHT - 50, 100, 40)
            if play_rect.collidepoint(mouse_pos) and plays_left > 0:
                play_selected_cards()

            discard_rect = pygame.Rect(configs.WIDTH // 2 - 50, configs.HEIGHT - 100, 100, 40)
            if discard_rect.collidepoint(mouse_pos) and discards_left > 0:
                discard()

    draw_hand(hand)
    draw_score_panel()
    chef_click_rects = draw_chefs()

    for rect, chef in chef_click_rects:
        if rect.collidepoint(mouse_pos):
            hovered_chef = chef
            break

    if hovered_chef:
        draw_chef_tooltip(hovered_chef, mouse_pos[0] + 10, mouse_pos[1] + 10)

    draw_play_button()
    draw_discard_button()
    draw_money()

    if plays_left == 0:
        game_lost = True


# Win Screen
def handle_game_win():
    global phase, current_money, plays_left, discards_left
    global current_score, goal_score, game_won, shop, highest_round

    reset_dp()

    phase += 1
    highest_round += 1
    # print(phase, phase%3)
    # DEBUG LINE

    current_money += [3, 4, 5][phase%3] + plays_left
    plays_left = max_plays_per_round
    discards_left = max_discards_per_round
    current_score = 0
    goal_score += int(200 * 1.5 * phase)

    open_shop()
    shop = True
    game_won = False

# Lose Screen
def handle_game_loss(events):
    global game_lost
    restart_button = draw_lose_screen()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.collidepoint(pygame.mouse.get_pos()):
                reset_game()
                game_lost = False

def main_game_loop():
    global running, title_screen, shop, game_won, game_lost

    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    threading.Thread(target=open_tk_window_with_tabs).start()

                if event.key == pygame.K_h:
                    print("========================================")
                    print("[!] Hands")
                    meals.represent()
                    print("========================================")

                if event.key == pygame.K_1:
                    hand.hand.sort(key=lambda card: card.size)
                    print("Hand sorted by number.")

                if event.key == pygame.K_2:
                    suit_order = {"meat": 0, "veggie": 1, "grains": 2, "dairy": 3}
                    hand.hand.sort(key=lambda card: suit_order.get(card.suite, 99))
                    print("Hand sorted by suit.")

                global volume
                if event.key == pygame.K_UP:
                    volume = min(1.0, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)
                    # print(f"Volume: {int(volume * 100)}%")
                    # DEBUG

                elif event.key == pygame.K_DOWN:
                    volume = max(0.0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)
                    # print(f"Volume: {int(volume * 100)}%")
                    # DEBUG

        if title_screen:
            handle_title_screen(events)
        elif shop:
            handle_shop(events)
        elif game_won:
            handle_game_win()
        elif game_lost:
            handle_game_loss(events)
        else:
            handle_gameplay(events)

        pygame.display.flip()

    pygame.quit()


main_game_loop()
