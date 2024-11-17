class Player:
    def __init__(self, name, is_ai=False):
        self.name = name
        self.is_ai = is_ai
        self.alive = True

    def eliminate(self):
        """Eliminate the player."""
        self.alive = False

    def is_active(self):
        """Check if the player is still active."""
        return self.alive

