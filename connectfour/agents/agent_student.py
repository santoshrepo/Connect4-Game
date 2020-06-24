from connectfour.agents.computer_player import Agent
import math

ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_LENGTH = 4
EMPTY_PIECE = 0
PLAYER1_PIECE = 1
PLAYER2_PIECE = 2


class StudentAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 2

    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.
        Returns:
            A tuple of two integers, (row, col)
        """

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            next_state = board.next_state(self.id, move[1])
            moves.append(move)
            vals.append(self.dfMiniMax(next_state, 1, -math.inf, math.inf))

        bestMove = moves[vals.index(max(vals))]
        return bestMove

    def dfMiniMax(self, board, depth, alpha, beta):

        if self.id == PLAYER2_PIECE:
            opponent = PLAYER1_PIECE
        else:
            opponent = PLAYER2_PIECE
        if board.terminal() is False:
            if self.checkWinMove(board, self.id):
                return 100000000000000
            elif self.checkWinMove(board, opponent):
                return -100000000000000
        else:
            return 0

        #Goal return column with maximized scores of all possible next states

        if depth == self.MaxDepth:
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            if depth % 2 == 1:
                next_state = board.next_state(self.id % 2 + 1, move[1])
            else:
                next_state = board.next_state(self.id, move[1])

            moves.append(move)
            vals.append(self.dfMiniMax(next_state, depth + 1, alpha, beta))

            if depth % 2 == 1:
                beta = min(min(vals), beta)
                if alpha >= beta:
                    break
            else:
                alpha = max(alpha, max(vals))
                if alpha >= beta:
                    break

        if depth % 2 == 1:
            bestVal = min(vals)
        else:
            bestVal = max(vals)

        return bestVal

    def evaluate_window(self, window, piece):
        score = 0

        opp_piece = PLAYER1_PIECE
        if piece == PLAYER1_PIECE:
            opp_piece = PLAYER2_PIECE

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY_PIECE) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY_PIECE) == 2:
            score += 2

        if window.count(opp_piece) == 4:
            score -= 100
        elif window.count(opp_piece) == 3 and window.count(EMPTY_PIECE) == 1:
            score -= 5
        elif window.count(opp_piece) == 2 and window.count(EMPTY_PIECE) == 2:
            score -= 2

        return score

    # check if player has won

    def checkWinMove(self, board, player):
        # Rows check
        for row in board.board:
            for col in range(board.width - 3):
                window = row[col:col + WINDOW_LENGTH]
                if window.count(player) == 4:
                    return True

        # Horizontal check
        for col in range(board.width):
            dummy_col = list()
            dummy_col.clear()
            for row in range(board.height):
                dummy_col.append(board.board[row][col])
            for j in range(board.height - 3):
                window = dummy_col[j: j + WINDOW_LENGTH]
                if window.count(player) == 4:
                    return True

        # Diagonal Up check
        for col in range(board.width + 1 - WINDOW_LENGTH):
            for row in range(board.height + 1 - WINDOW_LENGTH):
                window.clear()
                for i in range(WINDOW_LENGTH):
                    window.append(board.board[board.height - 1 - row - i][col + i])
                if window.count(player) == 4:
                    return True

        # Diagonal Down check
        for col in range(board.width + 1 - WINDOW_LENGTH):
            for row in range(board.height + 1 - WINDOW_LENGTH):
                window.clear()
                for i in range(WINDOW_LENGTH):
                    window.append(board.board[row + i][col + i])
                if window.count(player) == 4:
                    return True

        return False

    def evaluateBoardState(self, board):

        score = 0
        # Center column with highest score
        center_array = []
        for row in range(board.height):
            center_array.append(board.board[row][COLUMN_COUNT // 2])
        center_count = center_array.count(self.id)
        score += center_count * 3

        # Horizontal Scoring
        for row in board.board:
            for col in range(board.width - 3):
                window = row[col:col + WINDOW_LENGTH]
                score += self.evaluate_window(window, self.id)

        # Vertical Scoring
        for col in range(board.width):
            dummy_col = list()
            dummy_col.clear()
            for row in range(board.height):
                dummy_col.append(board.board[row][col])
            for j in range(board.height - 3):
                window = dummy_col[j: j + WINDOW_LENGTH]
                score += self.evaluate_window(window, self.id)

        # Diagonal Up Scoring
        for col in range(board.width + 1 - WINDOW_LENGTH):
            for row in range(board.height + 1 - WINDOW_LENGTH):
                window.clear()
                for i in range(WINDOW_LENGTH):
                    window.append(board.board[board.height - 1 - row - i][col + i])
                score += self.evaluate_window(window, self.id)

        # Diagonal Down Scoring
        for col in range(board.width + 1 - WINDOW_LENGTH):
            for row in range(board.height + 1 - WINDOW_LENGTH):
                window.clear()
                for i in range(WINDOW_LENGTH):
                    window.append(board.board[row + i][col + i])
                score += self.evaluate_window(window, self.id)

        return score

    """
    Your evaluation function should look at the current state and return a score for it.
    As an example, the random agent provided works as follows:
        If the opponent has won this game, return -1.
        If we have won the game, return 1.
        If neither of the players has won, return a random number.
    """

    """
    These are the variables and functions for board objects which may be helpful when creating your Agent.
    Look into board.py for more information/descriptions of each, or to look for any other definitions which may help you.
    Board Variables:
        board.width 
        board.height
        board.last_move
        board.num_to_connect
        board.winning_zones
        board.score_array 
        board.current_player_score
    Board Functions:
        get_cell_value(row, col)
        try_move(col)
        valid_move(row, col)
        valid_moves()
        terminal(self)
        legal_moves()
        next_state(turn)
        winner()
    """
