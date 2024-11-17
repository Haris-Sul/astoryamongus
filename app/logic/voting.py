from player import Player
import random


class Voting:
    def __init__(self, players):
        self.players = players 
        self.votes = {}
    
    def start_voting(self):
        self.votes = {player.alias: 0 for player in self.players.values() if player.is_active()}
    
    def cast_vote(self, vote_id, alias):
        if alias in self.votes:
            self.votes[alias] += 1
            return True
        return False


    def tally_votes(self):
        max_votes = max(self.votes.values())
        voted_out_candidates = [alias for alias, count in self.votes.items() if count == max_votes]
        if len(voted_out_candidates) > 1:
            print(f"Tie detected! Candidates: {', '.join(voted_out_candidates)}. Resolving randomly...")
            voted_out = random.choice(voted_out_candidates)
        else:
            voted_out = voted_out_candidates[0]

        return voted_out




            


