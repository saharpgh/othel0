from othelo import Othello
from bot import OthelloAI
import time

def play_othello():
    game = Othello()
    ai = OthelloAI(game)
    
    # Implementing an iterative deepening approach combined with a time-bound search strategy for the AI's decision-making process.

    # Summary:
    # Othello is a complex game with an enormous number of possible board states, making it impractical to explore the entire game tree, even with alpha-beta pruning.
    # To ensure that the AI can make decisions within a reasonable time frame, we use iterative deepening.
    # This technique starts the search at a shallow depth and incrementally deepens the search level until a preset time limit is reached.
    # The AI begins with a depth of 1 and continues deepening the search until the time limit (e.g., 4 seconds) is exceeded.
    # By doing so, we strike a balance between making well-informed moves and maintaining a responsive gameplay experience.
    # The AI selects the best move found within the time limit, ensuring that the game remains playable and challenging without excessive delays.

    # Set the time limit for AI to make a move
    time_limit = 4.0  # seconds
    
    # Starting depth for iterative deepening
    initial_depth = 1 

    while True:
        game.print_board()
        if game.has_valid_move(game.current_player):
            if game.current_player == 1:  # Human player
                print("Moves: ", game.valid_moves(game.current_player))
               
                row, col = map(int, input("Enter your move (row col): ").split())
                if (row, col) in game.valid_moves(game.current_player):
                    game.make_move(row, col, game.current_player)
                else:
                    print("Invalid move. Try again.")
                    continue
            else:  # AI player
                print("AI is making a move...")
                start_time = time.time()
                best_move = None

                for depth in range(initial_depth, 100):  # Arbitrary large upper limit
                    elapsed_time = time.time() - start_time
                    if elapsed_time > time_limit:
                        break  # Stop deepening if time exceeds the limit

                    move = ai.best_move(depth=depth)
                    if move:
                        best_move = move

                if best_move:
                    game.make_move(best_move[0], best_move[1], game.current_player)
                    print(f"AI played: {best_move}")
                else:
                    print("AI could not find a valid move within the time limit.")
        else:
            print(f"Player {game.current_player} has no valid moves.")
        
        game.switch_player()

        if not game.has_valid_move(game.current_player):
            print("Game over!")
            break

    game.print_board()
    score = sum(sum(row) for row in game.board)
    if score > 0:
        print("Player 1 (X) wins!")
    elif score < 0:
        print("Player 2 (O) wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    play_othello()
