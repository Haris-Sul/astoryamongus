import random

class Game:
    def __init__(self):
        self.players = ["AI"]
        self.keywords = []
        self.player_sentences = []
        self.ai_sentence = ''
        self.rounds = 0
        self.votes = {}
        self.game_over = False

    def add_players(self, socket_number):
        self.players.append(socket_number)
        return self.players
    
    def add_player_sentence(self, sentence):
        self.player_sentences.append(sentence)
        return self.player_sentence
    

    

        
    
    





