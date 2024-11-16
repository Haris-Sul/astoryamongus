import random
class Voting:
    def __init__(self, players):
        self.players = players 
        self.votes = {}

    def start_voting(self):
        self.votes = {player.name: 0 for player in self.players if player.is_active()}

    def cast_vote(self, voter, target):
        """Record a vote."""
        if target in self.votes:
            self.votes[target] += 1

    def tally_votes(self):
        """Determine who has the most votes."""
        max_votes = max(self.votes.values())
        voted_out = [player for player, count in self.votes.items() if count == max_votes]
        if len(voted_out) > 1:
            return random.choice(voted_out)  # Resolve ties randomly
        return voted_out[0]
