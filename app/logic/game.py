import random
from player import Player
from story import Story
import getpass
from ai_responses import generate_intro, generate_sentence



class Game:
    def __init__(self, num_players):
        self.players = [Player("") for _ in range(num_players - 1)]  # Human players
        self.ai = Player("", is_ai=True)  # AI starts without an alias
        self.players.append(self.ai)
        self.story = Story()
        self.keywords = {}
        self.rounds = 0
        self.game_over = False

    def collect_keywords(self):
        """Collect keywords from players."""
        print("\nCollecting keywords...")
        for player in self.players:
            if player.is_ai:
                continue  # AI doesn't provide keywords
            keyword = input("Enter your keyword: ")
            self.keywords[player] = keyword
        print("\nAll keywords have been collected. Generating the story...")

    def assign_aliases(self):
        """Assign random aliases to players, hiding AI identity."""
        random.shuffle(self.players)  # Shuffle players for anonymity
        for i, player in enumerate(self.players, start=1):
            player.name = f"Player {i}"  # Assign generic aliases

    def generate_initial_story(self):
        """Generate the opening paragraph of the story using AI."""
        player_keywords = list(self.keywords.values())
        intro_text = generate_intro(player_keywords)  # Call AI function to generate intro
        self.story.add_sentence("AI", intro_text)
        print(f"\nThe story begins:\n{intro_text}\n")

        # Assign aliases after the story starts
        self.assign_aliases()
        print("\nPlayer Aliases:")
        for player in self.players:
            print(f"- {player.name}")

    def take_turn(self, player):
        """Handle a single turn for a player or the AI."""
        if player.is_ai:
            context = self.story.get_full_story()
            ai_sentence = generate_sentence(context)  # AI generates a sentence
            self.story.add_sentence(player.name, ai_sentence)
            print(f"{player.name}: {ai_sentence}")
        else:
            sentence = input(f"{player.name}, add a sentence to the story: ")
            self.story.add_sentence(player.name, sentence)

    def play_round(self):
        """Play a single round."""
        print(f"\n--- Round {self.rounds + 1} ---")
        random.shuffle(self.players)  # Shuffle turn order for fairness
        for player in self.players:
            if player.is_active():
                self.take_turn(player)
        self.rounds += 1

    def start_voting(self):
        """Conduct voting."""
        votes = {}
        active_players = [player for player in self.players if player.is_active()]
        for voter in active_players:
            options = [p.name for p in active_players if p.name != voter.name]
            vote = input(f"{voter.name}, vote to eliminate: {', '.join(options)}: ")
            votes[vote] = votes.get(vote, 0) + 1

        # Determine the player with the most votes
        max_votes = max(votes.values())
        voted_out_candidates = [name for name, count in votes.items() if count == max_votes]

        if len(voted_out_candidates) > 1:
            print(f"Tie detected between: {', '.join(voted_out_candidates)}. Resolving randomly...")
            voted_out = random.choice(voted_out_candidates)
        else:
            voted_out = voted_out_candidates[0]

        # Eliminate the player
        for player in self.players:
            if player.name == voted_out:
                player.eliminate()
                print(f"{player.name} has been eliminated!")

    def check_game_status(self):
        """Check if the game should end."""
        active_players = [player for player in self.players if player.is_active()]
        if self.ai not in active_players:
            print("The AI has been eliminated! The players win!")
            self.game_over = True
        elif len(active_players) == 1:
            remaining_player = active_players[0]
            print(f"Only {remaining_player.name} remains. {'The AI wins!' if remaining_player.is_ai else 'The players lose!'}")
            self.game_over = True
