class Player:
    def __init__(self, socket_id, alias, is_ai=False,):
        self.socket_id = socket_id
        self.alias = alias
        self.is_ai = is_ai
        self.alive = True

    def eliminate(self):
        self.alive = False

    def is_active(self):
        return self.alive
