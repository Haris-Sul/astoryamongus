from game import Game

if __name__ == "__main__":
    num_players = int(input("Enter the number of players (including AI): "))
    game = Game(num_players)
    game.collect_keywords()
    game.generate_initial_story()

    while not game.game_over:
        game.play_round()
        game.start_voting()
        game.check_game_status()
