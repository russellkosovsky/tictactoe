
# Import necessary libraries
import tkinter as tk
from tkinter import messagebox

# Define the class for Tic Tac Toe
class TicTacToe:
    def __init__(self):
        # Initialize main tkinter window
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")

        # Initialize list to store button objects and the starting player
        self.buttons = []
        self.turn = 'O'

        # Generate 3x3 grid of buttons for Tic Tac Toe board
        for i in range(3):
            row = []
            for j in range(3):
                # Each button calls button_clicked() method when pressed
                button = tk.Button(self.root, width=10, height=3,
                                   command=lambda i=i, j=j: self.button_clicked(i, j))
                button.grid(row=i, column=j)  # Position button in grid
                row.append(button)  # Add button to row list
            self.buttons.append(row)  # Add row of buttons to buttons list

        # Label for showing whose turn it is
        self.turn_label = tk.Label(self.root, text="Player O's turn")
        self.turn_label.grid(row=3, column=0, columnspan=3)

        # Reset button calls reset() method when pressed
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset)
        self.reset_button.grid(row=4, column=0, columnspan=3)

    # Function called when a button is clicked
    def button_clicked(self, i, j):
        # Get button from grid
        button = self.buttons[i][j]
        # If button is empty, play turn and disable button
        if button['text'] == '':
            button.config(text=self.turn, state='disabled')
            # Check if turn resulted in a win
            winner = self.check_for_winner()
            # If there's a winner, end game
            if winner:
                self.end_game(winner)
            # If no winner, switch turn to AI and call ai_move
            else:
                self.turn = 'X'
                self.turn_label.config(text=f"Player {self.turn}'s turn")
                # Delay AI's move by 100ms for better UX
                self.root.after(100, self.ai_move)
            # If the board is full with no winner, it's a draw
            if self.check_board_full():
                self.end_game(None)

    # Function for the AI to make a move
    def ai_move(self):
        # If the board is not full, make a move
        if not self.check_board_full():
            # Find the best move using minimax algorithm
            best_move = self.minimax(0, True)
            # Place the AI's symbol on the best move spot
            self.buttons[best_move['i']][best_move['j']].config(text='X', state='disabled')
            # Check if AI's turn resulted in a win
            winner = self.check_for_winner()
            # If AI wins, end the game
            if winner:
                self.end_game(winner)
            # If no winner, switch turn to player
            else:
                self.turn = 'O'
                self.turn_label.config(text=f"Player {self.turn}'s turn")
            # If the board is full with no winner, it's a draw
            if self.check_board_full():
                self.end_game(None)

'''
Base case of the recursion: 
    The first part of the function checks for a terminal state, i.e., a state where the game has ended. 
    If there is a winner or if the board is full (a draw), it assigns a score to that state: +1 for AI win (X), 
    -1 for human win (O), and 0 for a draw. These scores represent the "value" of the game state from the AI's 
    perspective.

Maximizing player (AI) logic: 
    If it's the AI's turn (is_maximizing is True), the function will try to maximize the score. 
    It loops over all spots on the board, and for each empty spot, it places its own symbol (X) 
    there temporarily and calls minimax for the next depth with is_maximizing set to False 
    (simulating the opponent's turn). Then it undoes the move (removes the symbol). If the calculated score 
    is greater than the current best score, it updates the best score and records the move. 
    After considering all possible moves, it returns the best score and the corresponding move.

Minimizing player (human) logic: 
    If it's the opponent's turn (is_maximizing is False), the function will try to minimize the score, 
    as the opponent will try to win (which corresponds to minimizing the score from the AI's perspective). 
    The logic is the same as for the maximizing player, except that the function looks for a score smaller 
    than the current best score.

The minimax function is initially called by the AI with the current state of the board and is_maximizing 
set to True, which means it will return the best possible move for the AI considering all possible outcomes. 
'''

    # Minimax function for AI decision making
    def minimax(self, depth, is_maximizing):
        # Check for a winner. If there is, return score
        winner = self.check_for_winner()
        if winner:
            if winner == 'O':
                return {'score': -1}
            elif winner == 'X':
                return {'score': 1}
        # If board is full with no winner, it's a draw
        elif self.check_board_full():
            return {'score': 0}

        # If AI's turn, aim to maximize score
        if is_maximizing:
            best_score = {'score': -float('inf')}
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]['text'] == '':
                        self.buttons[i][j].config(text='X')
                        # Recurse minimax function to the next depth
                        score = self.minimax(depth + 1, False)
                        self.buttons[i][j].config(text='')
                        score['i'] = i
                        score['j'] = j
                        if score['score'] > best_score['score']:
                            best_score = score
            return best_score
        else:  # If player's turn, aim to minimize score
            best_score = {'score': float('inf')}
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]['text'] == '':
                        self.buttons[i][j].config(text='O')
                        score = self.minimax(depth + 1, True)
                        self.buttons[i][j].config(text='')
                        score['i'] = i
                        score['j'] = j
                        if score['score'] < best_score['score']:
                            best_score = score
            return best_score

    # Check rows, columns, and diagonals for winner
    def check_for_winner(self):
        for i in range(3):
            winner = self.check_row(i)
            if winner is not None:
                return winner
            winner = self.check_column(i)
            if winner is not None:
                return winner
        winner = self.check_diagonals()
        if winner is not None:
            return winner

    # Check if all spots in a row have the same symbol
    def check_row(self, row):
        if len(set(button['text'] for button in self.buttons[row])) == 1 and self.buttons[row][0]['text'] != '':
            return self.buttons[row][0]['text']

    # Check if all spots in a column have the same symbol
    def check_column(self, column):
        if len(set(self.buttons[i][column]['text'] for i in range(3))) == 1 and self.buttons[0][column]['text'] != '':
            return self.buttons[0][column]['text']

    # Check if all spots in the diagonals have the same symbol
    def check_diagonals(self):
        if (len(set(self.buttons[i][i]['text'] for i in range(3))) == 1 and self.buttons[0][0]['text'] != ''):
            return self.buttons[0][0]['text']
        elif (len(set(self.buttons[i][2-i]['text'] for i in range(3))) == 1 and self.buttons[0][2]['text'] != ''):
            return self.buttons[0][2]['text']

    # End game function
    def end_game(self, winner):
        for row in self.buttons:
            for button in row:
                button.config(state='disabled')
        if winner:
            result_text = f"Player {winner} wins! Click Reset to play again."
        else:
            result_text = "Draw! Click Reset to play again."
        self.turn_label.config(text=result_text)
        self.root.after(1000, lambda: messagebox.showinfo("Game Over", result_text))

    # Reset game function
    def reset(self):
        for row in self.buttons:
            for button in row:
                button.config(text='', state='normal')
        self.turn = 'O'
        self.turn_label.config(text="Player O's turn")

    # Check if the board is full
    def check_board_full(self):
        for row in self.buttons:
            for button in row:
                if button['text'] == '':
                    return False
        return True

# If this module is the main module, start the game
if __name__ == "__main__":
    game = TicTacToe()
    game.root.mainloop()



