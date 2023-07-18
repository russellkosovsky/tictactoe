import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.buttons = []
        self.turn = 'X'
        self.game_state = [['' for _ in range(3)] for _ in range(3)]
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.root, width=10, height=5,
                                   command=lambda i=i, j=j: self.button_clicked(i, j))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)
        self.turn_label = tk.Label(self.root, text="Player X's turn")
        self.turn_label.grid(row=3, column=0, columnspan=3)
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset)
        self.reset_button.grid(row=4, column=0, columnspan=3)

    def button_clicked(self, i, j):
        button = self.buttons[i][j]
        if button['text'] == '' and self.game_state[i][j] == '':
            button.config(text=self.turn, state='disabled')
            self.game_state[i][j] = self.turn
            if self.check_for_winner():
                self.end_game(self.turn)
            else:
                self.turn = 'O' if self.turn == 'X' else 'X'
                self.turn_label.config(text=f"Player {self.turn}'s turn")
                if not self.check_for_winner() and not self.check_board_full():
                    self.computer_move()

    def check_for_winner(self):
        for i in range(3):
            if self.game_state[i][0] == self.game_state[i][1] == self.game_state[i][2] != '':
                return True
            if self.game_state[0][i] == self.game_state[1][i] == self.game_state[2][i] != '':
                return True
        if self.game_state[0][0] == self.game_state[1][1] == self.game_state[2][2] != '':
            return True
        if self.game_state[0][2] == self.game_state[1][1] == self.game_state[2][0] != '':
            return True
        return False

    def check_board_full(self):
        for row in self.game_state:
            for cell in row:
                if cell == '':
                    return False
        return True

    def end_game(self, winner):
        for row in self.buttons:
            for button in row:
                button.config(state='disabled')
        result_text = f"{'Player ' + winner + ' wins' if winner else 'Draw'}! Click Reset to play again."
        self.turn_label.config(text=result_text)
        messagebox.showinfo("Game Over", result_text)

    def reset(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='', state='normal')
                self.game_state[i][j] = ''
        self.turn = 'X'
        self.turn_label.config(text="Player X's turn")

 
    def evaluate_board(self):
        for i in range(3):
            if self.game_state[i][0] == self.game_state[i][1] == self.game_state[i][2] != '':
                return 1 if self.game_state[i][0] == 'O' else -1
            if self.game_state[0][i] == self.game_state[1][i] == self.game_state[2][i] != '':
                return 1 if self.game_state[0][i] == 'O' else -1
        if self.game_state[0][0] == self.game_state[1][1] == self.game_state[2][2] != '':
            return 1 if self.game_state[0][0] == 'O' else -1
        if self.game_state[0][2] == self.game_state[1][1] == self.game_state[2][0] != '':
            return 1 if self.game_state[0][2] == 'O' else -1
        return 0
   
    def minimax(self, game_state, depth, is_maximizing, player):
        score = self.evaluate_board()
    
        if player == 'O':
            if score == 1:
                return score * (10 - depth)
            if self.check_board_full():
                return 0

            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if game_state[i][j] == '':
                        game_state[i][j] = player
                        score = self.minimax(game_state, depth + 1, not is_maximizing, 'X')
                        game_state[i][j] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            if score == -1:
                return score * (10 - depth)
            if self.check_board_full():
                return 0

            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if game_state[i][j] == '':
                        game_state[i][j] = player
                        score = self.minimax(game_state, depth + 1, not is_maximizing, 'O')
                        game_state[i][j] = ''
                        best_score = min(score, best_score)
            return best_score

    def computer_move(self):
        best_score = -float('inf')
        move = (None, None)
        for i in range(3):
            for j in range(3):
                if self.game_state[i][j] == '':
                    self.game_state[i][j] = 'O'
                    score = self.minimax(self.game_state, 0, False, 'X')
                    self.game_state[i][j] = ''
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        self.buttons[move[0]][move[1]].config(text='O', state='disabled')
        self.game_state[move[0]][move[1]] = 'O'
        if self.check_for_winner():
            self.end_game('O')
        else:
            self.turn = 'X'
            self.turn_label.config(text="Player X's turn")

if __name__ == "__main__":
    game = TicTacToe()
    game.root.mainloop()





