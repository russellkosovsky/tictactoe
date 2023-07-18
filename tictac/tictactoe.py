# Import tkinter for GUI and messagebox for showing message dialogues
import tkinter as tk
from tkinter import messagebox

# Define the class for Tic Tac Toe
class TicTacToe:
    def __init__(self):
        # Initialize main tkinter window
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")  # Set title of window

        self.buttons = []  # Initialize list to store button objects
        self.turn = 'X'    # 'X' goes first... will switch between 'X' and 'O'

        # Generate 3x3 grid of buttons for Tic Tac Toe board
        for i in range(3):
            row = []
            for j in range(3):
                # Each button calls button_clicked() method when pressed
                # Lambda function used to pass i and j arguments
                button = tk.Button(self.root, width=10, height=5,
                                   command=lambda i=i, j=j: self.button_clicked(i, j))
                button.grid(row=i, column=j)  # Position button in grid
                row.append(button)  # Add button to row list
            self.buttons.append(row)  # Add row of buttons to buttons list

        # Label for showing whose turn it is
        self.turn_label = tk.Label(self.root, text="Player X's turn")
        self.turn_label.grid(row=3, column=0, columnspan=3)

        # Reset button calls reset() method when pressed
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset)
        self.reset_button.grid(row=4, column=0, columnspan=3)

    def button_clicked(self, i, j):
        # Respond to button click
        button = self.buttons[i][j]  # Get button object
        if button['text'] == '':  # Only if the button hasn't been pressed
            button.config(text=self.turn, state='disabled')  # Mark button with 'X' or 'O' and disable it
            self.check_for_winner()  # Check if game is over
            # Swap turns
            self.turn = 'O' if self.turn == 'X' else 'X'
            self.turn_label.config(text=f"Player {self.turn}'s turn")  # Update turn label

    def check_for_winner(self):
        # Check rows, columns, and diagonals for winner
        for i in range(3):
            if self.check_row(i) or self.check_column(i):
                self.end_game(self.buttons[i][0]['text'])  # End game with current player as winner
        if self.check_diagonals():
            self.end_game(self.buttons[1][1]['text'])  # End game with current player as winner
        elif self.check_board_full():
            self.end_game(None)  # End game as draw

    def check_row(self, row):
        # Return True if all buttons in row contain the same text (and are not empty)
        return len(set(button['text'] for button in self.buttons[row])) == 1 and self.buttons[row][0]['text'] != ''

    def check_column(self, column):
        # Return True if all buttons in column contain the same text (and are not empty)
        return len(set(self.buttons[i][column]['text'] for i in range(3))) == 1 and self.buttons[0][column]['text'] != ''

    def check_diagonals(self):
        # Return True if all buttons in either diagonal contain the same text (and are not empty)
        return (len(set(self.buttons[i][i]['text'] for i in range(3))) == 1 and self.buttons[0][0]['text'] != '') or \
               (len(set(self.buttons[i][2-i]['text'] for i in range(3))) == 1 and self.buttons[0][2]['text'] != '')

    def check_board_full(self):
        # Return True if all buttons have been clicked (i.e., no empty buttons)
        return all(button['text'] != '' for row in self.buttons for button in row)

    def end_game(self, winner):
        # Disable all buttons and show end game message
        for row in self.buttons:
            for button in row:
                button.config(state='disabled')  # Disable button
        result_text = f"{'Player ' + winner + ' wins' if winner else 'Draw'}! Click Reset to play again."  # Generate result text
        self.turn_label.config(text=result_text)  # Show result on turn label
        messagebox.showinfo("Game Over", result_text)  # Show result in message box

    def reset(self):
        # Reset game to initial state
        for row in self.buttons:
            for button in row:
                button.config(text='', state='normal')  # Clear button text and enable button
        self.turn = 'X'  # 'X' goes first
        self.turn_label.config(text="Player X's turn")  # Update turn label


# If this module is the main module, start the game
if __name__ == "__main__":
    game = TicTacToe()  # Create game object
    game.root.mainloop()  # Start Tkinter event loop



