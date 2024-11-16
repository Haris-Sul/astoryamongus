from game import Game

if __name__ == "__main__":
    num_players = int(input("Enter the number of players (including AI): "))
    game = Game(num_players)
    game.play_game()
