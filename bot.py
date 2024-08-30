class OthelloAI:
    def __init__(self, game):
        self.game = game

    def minimax(self, depth, maximizing_player, alpha=float('-inf'), beta=float('inf')):
        """
        Minimax algorithm with Alpha-Beta Pruning.

        Parameters:
            depth (int): The maximum depth of the search tree.
            maximizing_player (bool): True if the current player is the AI (maximizing), False otherwise.
            alpha (float): The best value that the maximizer can guarantee at this level or above.
            beta (float): The best value that the minimizer can guarantee at this level or above.

        Returns:
            float: The evaluation score of the best move.
        """
        valid_moves = self.game.valid_moves(self.game.current_player if maximizing_player else -self.game.current_player)
        
        # Base case: depth limit or no valid moves
        if depth == 0 or not valid_moves:
            return self.evaluate_board()

        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                flip_positions = self.apply_move(move, self.game.current_player)
                eval = self.minimax(depth - 1, False, alpha, beta)
                self.undo_move(move, self.game.current_player, flip_positions)
                
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
            
            return max_eval
        
        else:
            min_eval = float('inf')
            for move in valid_moves:
                flip_positions = self.apply_move(move, -self.game.current_player)
                eval = self.minimax(depth - 1, True, alpha, beta)
                self.undo_move(move, -self.game.current_player, flip_positions)
                
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            
            return min_eval

    def evaluate_board(self):
        """
        Evaluates the current board state from the perspective of the AI player.
        
        Returns:
            float: A score representing the desirability of the board state.
        """
        score = 0
        
        # Coin Parity
        player_disk_count = sum(row.count(self.game.current_player) for row in self.game.board)
        opponent_disk_count = sum(row.count(-self.game.current_player) for row in self.game.board)
        coin_parity = player_disk_count - opponent_disk_count
        score += coin_parity
        
        # Mobility
        player_valid_moves = len(self.game.valid_moves(self.game.current_player))
        opponent_valid_moves = len(self.game.valid_moves(-self.game.current_player))
        mobility = player_valid_moves - opponent_valid_moves
        score += 2 * mobility
        
        # Corner Occupancy
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        corner_occupancy = sum(self.game.board[r][c] for r, c in corners)
        score += 5 * corner_occupancy
        
        # Edge Occupancy
        edge_occupancy = sum(self.game.board[i][j] for i in [0, 7] for j in range(1, 7)) + \
                         sum(self.game.board[i][j] for i in range(1, 7) for j in [0, 7])
        score += 2.5 * edge_occupancy
        
        return score

    def apply_move(self, move, player):
        """
        Apply the move to the board and return the positions of the pieces that will be flipped.

        Parameters:
            move (tuple): The move to apply.
            player (int): The player making the move.

        Returns:
            list: The positions of the pieces that will be flipped.
        """
        row, col = move
        flip_positions = []
        self.game.board[row][col] = player
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 8 and 0 <= nc < 8 and self.game.board[nr][nc] == -player:
                temp_flip_positions = []
                while 0 <= nr < 8 and 0 <= nc < 8:
                    if self.game.board[nr][nc] == 0:
                        break
                    if self.game.board[nr][nc] == player:
                        flip_positions.extend(temp_flip_positions)
                        break
                    temp_flip_positions.append((nr, nc))
                    nr += dr
                    nc += dc
        return flip_positions

    def undo_move(self, move, player, flip_positions):
        """
        Undo the move and revert the positions of the flipped pieces.

        Parameters:
            move (tuple): The move to undo.
            player (int): The player who made the move.
            flip_positions (list): The positions of the pieces that were flipped.
        """
        row, col = move
        self.game.board[row][col] = 0
        for fr, fc in flip_positions:
            self.game.board[fr][fc] = -player

    def best_move(self, depth):
        """
        Determine the best move for the AI by evaluating all possible moves.

        Parameters:
            depth (int): The maximum depth of the search tree.

        Returns:
            tuple: The best move for the AI.
        """
        best_eval = float('-inf')
        best_move = None
        for move in self.game.valid_moves(self.game.current_player):
            flip_positions = self.apply_move(move, self.game.current_player)
            self.game.switch_player()
            eval = self.minimax(depth - 1, False)
            self.game.switch_player()
            self.undo_move(move, self.game.current_player, flip_positions)
            if eval > best_eval:
                best_eval = eval
                best_move = move
        return best_move
