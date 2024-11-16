from player import Player
import random


class Voting:
    def __init__(self, players):
        self.players = players 
        self.votes = {}

    def start_voting(self):
        """Initialize the voting phase."""
        self.votes = {}
        active_players = [player for player in self.players if player.is_active()]
        for voter in active_players:
            options = [p.name for p in active_players if p.name != voter.name]
            vote = input(f"{voter.name}, vote to eliminate a player: {', '.join(options)}: ")

           
            while vote not in options:
                print("Invalid vote. Please choose a valid player.")
                vote = input(f"{voter.name}, vote to eliminate a player: {', '.join(options)}: ")

     
            self.votes[vote] = self.votes.get(vote, 0) + 1

    def tally_votes(self):
        max_votes = max(self.votes.values())
        voted_out_candidates = [name for name, count in self.votes.items() if count == max_votes]

        if len(voted_out_candidates) > 1:
            print(f"Tie detected! Candidates: {', '.join(voted_out_candidates)}. Resolving randomly...")
            voted_out = random.choice(voted_out_candidates)
        else:
            voted_out = voted_out_candidates[0]

        return voted_out




            


