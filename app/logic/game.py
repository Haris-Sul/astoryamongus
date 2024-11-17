import random
from logic.player import Player
from logic.story import Story
from logic.ai_responses import generate_intro, generate_sentence


class Game:
    def __init__(self, num_players):
        # make list of players with names Player 1... 
        # self.players = [Player(f"Player {i+1}") for i in range(num_players)]
        self.players = [Player("") for _ in range(num_players)]  # Human players
        self.ai = Player("", is_ai=True)  # AI starts without an alias
        self.players.append(self.ai)

        self.story = Story()
        self.keywords = {}
        self.rounds = 0
        self.game_over = False
        # print joined list of player names
        # print(", ".join([player.name for player in self.players]))