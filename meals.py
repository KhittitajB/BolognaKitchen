# Classes here are only for referencing mults and scores in the game, it doesn't mean each hands
from collections import Counter

class Appetizer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Appetizer, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "name", "score", "mult"):
            self.name = "Appetizer"
            self.score = 5
            self.mult = 1

    def level_up(self):
        self.score += 10
        self.mult += 1

class SmallPlatter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SmallPlatter, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "name", "score", "mult"):
            self.name = "Small Platter"
            self.score = 10
            self.mult = 2

    def level_up(self):
        self.score += 15
        self.mult += 1

class DoubleCourse:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DoubleCourse, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "name", "score", "mult"):
            self.name = "Double Course"
            self.score = 20
            self.mult = 2

    def level_up(self):
        self.score += 20
        self.mult += 1

class MediumPlatter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MediumPlatter, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "name", "score", "mult"):
            self.name = "Medium Platter"
            self.score = 30
            self.mult = 3

    def level_up(self):
        self.score += 20
        self.mult += 2

class Signature:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Signature, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "name", "score", "mult"):
            self.name = "Signature Dish"
            self.score = 30
            self.mult = 4

    def level_up(self):
        self.score += 30
        self.mult += 3

class Feast:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Feast, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "name", "score", "mult"):
            self.name = "Feast"
            self.score = 35
            self.mult = 4

    def level_up(self):
        self.score += 15
        self.mult += 2

class FullCourse:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FullCourse, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "name", "score", "mult"):
            self.name = "Full Course Meal"
            self.score = 40
            self.mult = 4

    def level_up(self):
        self.score += 25
        self.mult += 2

class BigPlatter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BigPlatter, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "name", "score", "mult"):
            self.name = "Big Platter"
            self.score = 60
            self.mult = 7

    def level_up(self):
        self.score += 30
        self.mult += 3

class ChefSpecial:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChefSpecial, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "name", "score", "mult"):
            self.name = "Chef's Special"
            self.score = 100
            self.mult = 8

    def level_up(self):
        self.score += 40
        self.mult += 4

class EnormousPlatter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EnormousPlatter, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "name", "score", "mult"):
            self.name = "Enormous Platter"
            self.score = 120
            self.mult = 12

    def level_up(self):
        self.score += 35
        self.mult += 3

class FeastCourse:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FeastCourse, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "name", "score", "mult"):
            self.name = "Feast Course"
            self.score = 140
            self.mult = 14

    def level_up(self):
        self.score += 40
        self.mult += 4

class FeastPlatter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FeastPlatter, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "name", "score", "mult"):
            self.name = "Feast Platter"
            self.score = 160
            self.mult = 16

    def level_up(self):
        self.score += 50
        self.mult += 3


# VERY IMPORTANT
def all_same(items):
    return all(x == items[0] for x in items)

def count_same(items):
    count = Counter(items)
    max_freq = max(count.values())

    if list(count.values()).count(max_freq) > 1:
        return 0
    return max_freq

def evaluate_hand(cards):
    size_counts = []
    suite_counts = []

    for card in cards:
        size_counts.append(card.size)
        suite_counts.append(card.suite)

    # FLUSHES
    if len(suite_counts) == 5 and all_same(suite_counts):
        if count_same(size_counts) == 5:
            return "Feast Platter"      # Flush Five
        else:
            return "Feast"              # Flush
    # NOT FLUSHES
    else:
        if count_same(size_counts) == 5:
            return "Enormous Platter"   # Five of a Kind
        elif count_same(size_counts) == 4:
            return "Big Platter"        # Four of a Kind
        elif count_same(size_counts) == 3:
            return "Medium Platter"     # Three of a Kind
        elif count_same(size_counts) == 0:
            return "Double Course"      # Two Pair
        elif count_same(size_counts) == 2:
            return "Small Platter"      # Pair
        else:
            return "Appetizer"          # High Card
