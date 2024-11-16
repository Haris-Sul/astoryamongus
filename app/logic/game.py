import random
from player import Player
from story import Story
from voting import Voting

class Game:
    def __init__(self, num_players):
        self.players = [Player(f"Player {i+1}") for i in range(num_players - 1)]
        self.ai = Player("AI", is_ai=True)
        self.players.append(self.ai)
        self.story = Story()
        self.rounds = 0
        self.game_over = False
        self.voting = Voting(self.players)

    def collect_keywords(self):
        self.keywords = {}
        for player in self.players:
            if player.is_ai:
                keyword = "mystical"  # Example AI keyword
                print(f"{player.name} generated the keyword: {keyword}")
            else:
                keyword = input(f"{player.name}, enter a keyword: ")
            self.keywords[player.name] = keyword

    def generate_initial_story(self):
        combined_keywords = ", ".join(self.keywords.values())
        initial_story = f"The story begins with these elements: {combined_keywords}."
        self.story.add_sentence("AI", initial_story)
        print(f"AI: {initial_story}")

    def randomize_turn_order(self):
        random.shuffle(self.players)

    def take_turn(self, player):
        if player.is_ai:
            sentence = f"The AI adds a twist to the story involving '{self.keywords[player.name]}'."
            self.story.add_sentence(player.name, sentence)
            print(f"AI: {sentence}")
        else:
            sentence = input(f"{player.name}, add a sentence to the story: ")
            self.story.add_sentence(player.name, sentence)

    def play_round(self):
        print(f"\n--- Round {self.rounds + 1} ---")
        self.randomize_turn_order()
        for player in self.players:
            if player.is_active():
                self.take_turn(player)
        self.rounds += 1

    def vote_to_eliminate(self):
        self.voting.start_voting()
        voted_out = self.voting.tally_votes()

        for player in self.players:
            if player.name == voted_out:
                player.eliminate()
                print(f"{player.name} has been eliminated!")
                return player

    def check_game_status(self):
        active_players = [player for player in self.players if player.is_active()]
        if self.ai not in active_players:
            print("The AI has been eliminated. Players win!")
            self.game_over = True
        elif len(active_players) == 1:
            print("Only one player remains with the AI. The AI wins!")
            self.game_over = True

    def play_game(self):
        self.collect_keywords()
        self.generate_initial_story()

        while not self.game_over:
            self.play_round()
            self.vote_to_eliminate()
            self.check_game_status()

        print("\nFinal Story:")
        print(self.story.get_full_story())
