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

if __name__ == "__main__":
    TicTacToe().run()
