import random
from player import Player
from story import Story
import getpass
from ai_responses import generate_intro, generate_sentence
import random


class Game:
    def __init__(self, num_players):
        self.players = [Player("") for _ in range(num_players - 1)]  # Human players
        self.ai = Player("", is_ai=True)  # AI starts without an alias
        self.players.append(self.ai)
        self.story = Story()
        self.keywords = {}
        self.rounds = 0
        self.game_over = False

    # method to return player from name
    def get_player(self, name):
        for player in self.players:
            if player.name == name:
                return player

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
        votes = []
        active_players = [player for player in self.players if player.is_active()]

        # Collect votes from all human players
        for voter in active_players:
            options = [p.name for p in active_players if p.name != voter.name]

            if voter.is_ai == False:
                vote = None
                while vote not in options:
                    vote = input(f"{voter.name}, vote to eliminate: {', '.join(options)} > ")
                    if vote not in options:
                        print(f"Invalid vote. Please try again.")
                    
                votes.append(vote)

        
        # Determine the non-ai player with the most votes
        if len(votes) < 2:
            votes += [active_players[0].name]
        else:
            non_ai_votes = [vote for vote in votes if not self.get_player(vote).is_ai]
            max_non_ai_votes = self.players_with_max_votes(non_ai_votes)
            if len(max_non_ai_votes) == 1:
                # add ai vote for player with most votes
                votes += [max_non_ai_votes[0]]
            else:
                # add ai vote for random player with most votes
                votes += [random.choice(max_non_ai_votes)]
        
        print("TEST: " + ", ".join(votes))
        print(self.ai.name + " votes to eliminate: " + votes[-1])

        # Determine the player with the most votes
        max_votes = self.players_with_max_votes(votes)
        if len(max_votes) == 1:
            eliminated_player = self.get_player(max_votes[0])
        else:
            eliminated_player = self.get_player(random.choice(max_votes))


        eliminated_player.eliminate()
        print(f"{eliminated_player.name} has been eliminated.")
        
        
    def players_with_max_votes(self, votes):
        if len(votes) == 1:
            return [votes[0]]
        vote_count = {}
        for vote in votes:
            if vote in vote_count:
                vote_count[vote] += 1
            else:
                vote_count[vote] = 1

        # Find the maximum number of votes
        max_votes = max(vote_count.values())

        # Find all players with the maximum number of votes
        return [player for player, count in vote_count.items() if count == max_votes]

    

    def check_game_status(self):
        """Check if the game should end."""
        active_players = [player for player in self.players if player.is_active()]
        if self.ai not in active_players:
            print("The AI has been eliminated! The players win!")
            self.game_over = True
        elif len(active_players) == 1:
            remaining_player = active_players[0]
            print(f"Only {remaining_player.name} remains. {'The AI wins!' if remaining_player.is_ai else 'The humans have been victorious!'}")
            self.game_over = True
