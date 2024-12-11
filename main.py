import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.board = [""] * 9
        self.current_player = "X"
        self.difficulty = "Easy"
        self.create_widgets()

    def create_widgets(self):
        self.buttons = []
        for i in range(9):
            button = tk.Button(self.window, text="", font=("Arial", 20), width=5, height=2,
                               command=lambda i=i: self.player_move(i))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

        self.difficulty_menu = tk.StringVar(value="Easy")
        dropdown = tk.OptionMenu(self.window, self.difficulty_menu, "Easy", "Medium", "Impossible")
        dropdown.grid(row=3, column=0, columnspan=3)

        reset_button = tk.Button(self.window, text="Reset", command=self.reset_game)
        reset_button.grid(row=4, column=0, columnspan=3)

    def player_move(self, index):
        if self.board[index] == "" and self.current_player == "X":
            self.board[index] = "X"
            self.buttons[index].config(text="X")
            if self.check_winner("X"):
                self.show_winner("Player")
                return
            elif "" not in self.board:
                self.show_winner("Nobody")
                return
            self.current_player = "O"
            self.ai_move()

    def ai_move(self):
        if self.difficulty_menu.get() == "Easy":
            move = self.random_move()
        elif self.difficulty_menu.get() == "Medium":
            move = self.medium_ai()
        else:
            move = self.minimax(self.board, "O")[1]

        if move is not None:
            self.board[move] = "O"
            self.buttons[move].config(text="O")
            if self.check_winner("O"):
                self.show_winner("AI")
                return
            elif "" not in self.board:
                self.show_winner("Nobody")
                return
            self.current_player = "X"

    def random_move(self):
        return random.choice([i for i, spot in enumerate(self.board) if spot == ""])

    def medium_ai(self):
        # 1. Cerca di vincere
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                if self.check_winner("O"):
                    self.board[i] = ""
                    return i
                self.board[i] = ""

        # 2. Blocca l'avversario
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "X"
                if self.check_winner("X"):
                    self.board[i] = ""
                    return i
                self.board[i] = ""

        # 3. Gioca al centro se disponibile
        if self.board[4] == "":
            return 4

        # 4. Gioca in un angolo libero
        for i in [0, 2, 6, 8]:
            if self.board[i] == "":
                return i

        # 5. Mosse casuali per rimanenti
        return self.random_move()


    def minimax(self, board, player):
        if self.check_winner("O", board):
            return 10, None
        if self.check_winner("X", board):
            return -10, None
        if "" not in board:
            return 0, None

        moves = []
        for i in range(9):
            if board[i] == "":
                board[i] = player
                score = self.minimax(board, "X" if player == "O" else "O")[0]
                moves.append((score, i))
                board[i] = ""

        if player == "O":
            return max(moves)
        else:
            return min(moves)

    def check_winner(self, player, board=None):
        if board is None:
            board = self.board
        wins = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                (0, 4, 8), (2, 4, 6)]
        return any(all(board[i] == player for i in combo) for combo in wins)

    def show_winner(self, winner):
        messagebox.showinfo("Game Over", f"{winner} wins!")
        self.reset_game()

    def reset_game(self):
        self.board = [""] * 9
        self.current_player = "X"
        for button in self.buttons:
            button.config(text="")

    def run(self):
        self.window.mainloop()



class SuperTicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Super Tic-Tac-Toe")
        self.board = [[""] * 9 for _ in range(9)]
        self.sub_boards_status = [[""] * 3 for _ in range(3)]
        self.current_player = "X"
        self.active_board = None
        self.bg_colors = {
            "X": "#ffcdd2",  # Light red
            "O": "#c8e6c9",  # Light green
            "Draw": "#f5f5f5",  # Light gray
            "Active": "#e3f2fd"  # Light blue
        }
        self.difficulty = "Easy"
        self.difficulty_menu = tk.StringVar(value="Easy")

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.window)
        self.main_frame.grid(padx=10, pady=10)
        
        # Create 3x3 frames for sub-boards
        self.sub_frames = []
        for i in range(3):
            row_frames = []
            for j in range(3):
                frame = tk.Frame(self.main_frame, relief="solid", borderwidth=2)
                frame.grid(row=i, column=j, padx=3, pady=3)
                row_frames.append(frame)
            self.sub_frames.append(row_frames)
        
        # Create buttons inside each sub-board
        self.buttons = []
        for i in range(9):
            row_buttons = []
            for j in range(9):
                sub_i, sub_j = i // 3, j // 3
                frame = self.sub_frames[sub_i][sub_j]
                button = tk.Button(frame, text="", font=("Arial", 16), width=2, height=1,
                                 command=lambda i=i, j=j: self.player_move(i, j))
                button.grid(row=i%3, column=j%3, padx=1, pady=1)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        reset_button = tk.Button(self.window, text="Reset Game", command=self.reset_game)
        reset_button.grid(row=1, column=0, pady=10)
        # difficulty dropdown
        dropdown = tk.OptionMenu(self.window, self.difficulty_menu, "Easy", "Medium", "Impossible")
        dropdown.grid(row=2, column=0, pady=5)

    def update_board_colors(self):
        # Reset all backgrounds
        for i in range(9):
            for j in range(9):
                self.buttons[i][j].config(bg="white")
        
        # Color completed sub-boards
        for i in range(3):
            for j in range(3):
                if self.sub_boards_status[i][j] in self.bg_colors:
                    color = self.bg_colors[self.sub_boards_status[i][j]]
                    for sub_i in range(3):
                        for sub_j in range(3):
                            button_i = i * 3 + sub_i
                            button_j = j * 3 + sub_j
                            self.buttons[button_i][button_j].config(bg=color)
        
        # Highlight active board
        if self.active_board is not None:
            i, j = self.active_board
            for sub_i in range(3):
                for sub_j in range(3):
                    button_i = i * 3 + sub_i
                    button_j = j * 3 + sub_j
                    if self.sub_boards_status[i][j] == "":
                        self.buttons[button_i][button_j].config(bg=self.bg_colors["Active"])

    def get_sub_board_index(self, i, j):
        return i // 3, j // 3

    def is_valid_move(self, i, j):
        if self.board[i][j] != "":
            return False
        if self.active_board is None:
            return True
        board_i, board_j = self.get_sub_board_index(i, j)
        return self.active_board == (board_i, board_j)

    def check_sub_board_winner(self, board_i, board_j):
        sub_board = [self.board[board_i*3 + x][board_j*3 + y] for x in range(3) for y in range(3)]
        wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for combo in wins:
            if sub_board[combo[0]] == sub_board[combo[1]] == sub_board[combo[2]] != "":
                return sub_board[combo[0]]
        if "" not in sub_board:
            return "Draw"
        return None

    def check_game_winner(self):
        wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for combo in wins:
            if self.sub_boards_status[combo[0]//3][combo[0]%3] == self.sub_boards_status[combo[1]//3][combo[1]%3] == self.sub_boards_status[combo[2]//3][combo[2]%3] != "":
                return self.sub_boards_status[combo[0]//3][combo[0]%3]
        if all(self.sub_boards_status[i][j] != "" for i in range(3) for j in range(3)):
            return "Draw"
        return None

    def player_move(self, i, j):
        if self.current_player == "X" and self.is_valid_move(i, j):
            self.make_move(i, j, "X")
            if not self.check_game_over():
                self.current_player = "O"
                self.window.after(500, self.ai_move)

    def ai_move(self):
        if self.difficulty_menu.get() == "Easy":
            self.make_random_move()
        elif self.difficulty_menu.get() == "Medium":
            self.make_medium_move()
        else:
            self.make_best_move()
        
    def make_random_move(self):
        valid_moves = [(i, j) for i in range(9) for j in range(9) if self.is_valid_move(i, j)]
        if valid_moves:
            i, j = random.choice(valid_moves)
            self.make_move(i, j, "O")
            self.check_game_over()
            self.current_player = "X"

    def make_medium_move(self):
        valid_moves = [(i, j) for i in range(9) for j in range(9) if self.is_valid_move(i, j)]
        
        # Try to win
        for i, j in valid_moves:
            board_copy = [row[:] for row in self.board]
            board_copy[i][j] = "O"
            board_i, board_j = self.get_sub_board_index(i, j)
            if self.would_win_sub_board(board_copy, board_i, board_j, "O"):
                self.make_move(i, j, "O")
                self.check_game_over()
                self.current_player = "X"
                return
        
        # Block opponent's win
        for i, j in valid_moves:
            board_copy = [row[:] for row in self.board]
            board_copy[i][j] = "X"
            board_i, board_j = self.get_sub_board_index(i, j)
            if self.would_win_sub_board(board_copy, board_i, board_j, "X"):
                self.make_move(i, j, "O")
                self.check_game_over()
                self.current_player = "X"
                return
        
        # Otherwise make random move
        self.make_random_move()

    def would_win_sub_board(self, board, board_i, board_j, player):
        sub_board = [board[board_i*3 + x][board_j*3 + y] for x in range(3) for y in range(3)]
        wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        return any(all(sub_board[pos] == player for pos in combo) for combo in wins)

    def make_best_move(self):
        # Implementing a full minimax for Super TicTacToe would be very complex
        self.make_medium_move()

    def make_move(self, i, j, player):
        self.board[i][j] = player
        self.buttons[i][j].config(text=player)
        board_i, board_j = self.get_sub_board_index(i, j)
        result = self.check_sub_board_winner(board_i, board_j)
        if result:
            self.sub_boards_status[board_i][board_j] = result
        next_board_i, next_board_j = i % 3, j % 3
        if self.sub_boards_status[next_board_i][next_board_j] == "":
            self.active_board = (next_board_i, next_board_j)
        else:
            self.active_board = None
        self.update_board_colors()

    def check_game_over(self):
        winner = self.check_game_winner()
        if winner:
            if winner == "Draw":
                messagebox.showinfo("Game Over", "It's a draw!")
            else:
                messagebox.showinfo("Game Over", f"Player {winner} wins!")
            self.reset_game()
            return True
        return False

    def reset_game(self):
        self.board = [[""] * 9 for _ in range(9)]
        self.sub_boards_status = [[""] * 3 for _ in range(3)]
        self.current_player = "X"
        self.active_board = None
        for i in range(9):
            for j in range(9):
                self.buttons[i][j].config(text="", bg="white")

    def run(self):
        self.window.mainloop()

def main_menu():
    root = tk.Tk()
    root.title("Game Selection")
    
    def start_tictactoe():
        root.destroy()
        game = TicTacToe()
        game.run()
    
    def start_supertictactoe():
        root.destroy()
        game = SuperTicTacToe()
        game.run()

    tk.Button(root, text="TicTacToe", command=start_tictactoe).pack(pady=10)
    tk.Button(root, text="Super TicTacToe", command=start_supertictactoe).pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    main_menu()


def main_menu():
    root = tk.Tk()
    root.title("Game Selection")
    
    def start_tictactoe():
        root.destroy()
        game = TicTacToe()
        game.run()
    
    def start_supertictactoe():
        root.destroy()
        game = SuperTicTacToe()
        game.run()

    tk.Button(root, text="TicTacToe", command=start_tictactoe).pack(pady=10)
    tk.Button(root, text="Super TicTacToe", command=start_supertictactoe).pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    main_menu()
