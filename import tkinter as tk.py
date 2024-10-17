import tkinter as tk
from tkinter import messagebox
import time

# Create the game window
class TicTacToeGame:
    def __init__(self, root, grid_size=3, time_limit=10):
        self.root = root
        self.grid_size = grid_size
        self.time_limit = time_limit
        self.root.title("Tic Tac Toe")
        self.turn = "Star"  # First player is Star
        self.board = [[None] * grid_size for _ in range(grid_size)]
        self.moves = []
        self.timer_running = False
        self.time_left = time_limit

        # Set up the main frame and grid
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)

        # Create the menu and place it at the top center
        self.create_menu()

        # Create the game grid
        self.build_grid()

        # Turn and timer display
        self.turn_label = tk.Label(self.main_frame, text=f"{self.turn}'s turn", font=('Helvetica', 16))
        self.turn_label.grid(row=self.grid_size, column=0, columnspan=self.grid_size)

        self.time_label = tk.Label(self.main_frame, text=f"Time left: {self.time_left}s", font=('Helvetica', 14))
        self.time_label.grid(row=self.grid_size + 1, column=0, columnspan=self.grid_size)

        # Start the timer
        self.update_timer()

    def create_menu(self):
        # Centered and prominent options button
        self.options_button = tk.Button(self.root, text="Options", font=('Helvetica', 14, 'bold'), command=self.show_options)
        self.options_button.pack(pady=10)  # Centered and above the game grid

    def show_options(self):
        options_window = tk.Toplevel(self.root)
        options_window.title("Options")
        options_label = tk.Label(options_window, text="Options Menu", font=('Helvetica', 16, 'bold'))
        options_label.pack(pady=10)

        undo_button = tk.Button(options_window, text="Undo", font=('Helvetica', 12), command=self.undo_move)
        undo_button.pack(pady=5)

        restart_button = tk.Button(options_window, text="Restart", font=('Helvetica', 12), command=self.restart_game)
        restart_button.pack(pady=5)

    def build_grid(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                button = tk.Button(self.main_frame, width=6, height=3, font=('Helvetica', 48),  # Bigger and visually appealing symbols
                                   command=lambda r=row, c=col: self.handle_click(r, c))
                button.grid(row=row, column=col)
                self.board[row][col] = button

    def handle_click(self, row, col):
        button = self.board[row][col]
        if not button["text"]:  # If the cell is empty
            if self.turn == "Star":
                button["text"] = "★"
                button["fg"] = "gold"  # Color for the star symbol
                self.turn = "Moon"
            else:
                button["text"] = "☽"
                button["fg"] = "blue"  # Color for the moon symbol
                self.turn = "Star"

            self.turn_label.config(text=f"{self.turn}'s turn")
            self.moves.append((row, col))
            self.time_left = self.time_limit  # Reset timer after every move

            if self.check_winner():
                self.end_game(f"{button['text']} wins!")
            elif len(self.moves) == self.grid_size ** 2:
                self.end_game("It's a draw!")

    def check_winner(self):
        # Check rows, columns, and diagonals
        for i in range(self.grid_size):
            if all(self.board[i][j]["text"] == self.board[i][0]["text"] and self.board[i][0]["text"] != ""
                   for j in range(self.grid_size)):
                return True
            if all(self.board[j][i]["text"] == self.board[0][i]["text"] and self.board[0][i]["text"] != ""
                   for j in range(self.grid_size)):
                return True
        if all(self.board[i][i]["text"] == self.board[0][0]["text"] and self.board[0][0]["text"] != ""
               for i in range(self.grid_size)):
            return True
        if all(self.board[i][self.grid_size - 1 - i]["text"] == self.board[0][self.grid_size - 1]["text"] and
               self.board[0][self.grid_size - 1]["text"] != "" for i in range(self.grid_size)):
            return True
        return False

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.root.quit()

    def undo_move(self):
        if self.moves:
            last_move = self.moves.pop()
            self.board[last_move[0]][last_move[1]].config(text="")
            self.turn = "Moon" if self.turn == "Star" else "Star"
            self.turn_label.config(text=f"{self.turn}'s turn")
            self.time_left = self.time_limit  # Reset the timer

    def restart_game(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.board[row][col].config(text="")
        self.turn = "Star"
        self.turn_label.config(text=f"{self.turn}'s turn")
        self.moves.clear()

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.time_label.config(text=f"Time left: {self.time_left}s")
            self.root.after(1000, self.update_timer)
        else:
            self.turn = "Moon" if self.turn == "Star" else "Star"
            self.turn_label.config(text=f"{self.turn}'s turn (Timeout!)")
            self.time_left = self.time_limit
            self.update_timer()


# Initialize the game window
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGame(root, grid_size=3, time_limit=10)
    root.mainloop()
