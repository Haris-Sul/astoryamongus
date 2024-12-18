import random
from logic.player import Player
from logic.story import Story
from logic.ai_responses import generate_intro, generate_sentence


class Game:
    def __init__(self, num_players):
        # make list of players with  names Player 1... 
        # self.players = [Player(f"Player {i+1}") for i in range(num_players)]
        self.players = [Player("") for _ in range(num_players)]  # Human players
        self.ai = Player("", is_ai=True)  # AI starts without an alias
        self.players.append(self.ai)

        self.story = Story()
        self.keywords = []
        self.rounds = 0
        self.current_player = 0
        self.game_over = False


    def assign_aliases(self):
        """Assign random aliases to players, hiding AI identity."""
        random.shuffle(self.players)  # Shuffle players for anonymity
        for i, player in enumerate(self.players, start=1):
            player.name = f"Player {i}"  # Assign generic aliases
        # print joined list of player names
        print(", ".join([player.name for player in self.players]))

    def generate_initial_story(self, keywords):
        """Generate the opening paragraph of the story using AI."""
        intro_text = generate_intro(keywords)  # Call AI function to generate intro
        self.story.add_sentence("AI", intro_text)
        
    def ai_turn(self):
        """Handle a single turn for the AI."""
        context = self.story.get_full_story()
        ai_sentence = generate_sentence(context)  # AI generates a sentence
        self.story.add_sentence(ai_sentence)
        return ai_sentence
        
        
    def player_turn(self, player):
        sentence = input(f"{player.name}, add a sentence to the story: ")
        self.story.add_sentence(player.name, sentence)


