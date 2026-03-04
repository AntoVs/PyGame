import tkinter as tk
from tkinter import messagebox


class FastClickGame:

    def __init__(self):

        # Start Window
        self.root = tk.Tk()
        self.root.title("Fastest Click Wins")
        self.root.geometry("300x200")

        # round scores
        self.score1 = 0
        self.score2 = 0

        # match scoreboard
        self.player1_wins = 0
        self.player2_wins = 0

        self.target = 20
        self.game_active = False

        self.create_start_ui()
        self.root.mainloop()


    # ---------- Start Menu --------------------------
    def create_start_ui(self):

        title = tk.Label(self.root, text="Fastest Click Wins", font=("Arial",16,"bold"))
        title.pack(pady=20)

        start_btn = tk.Button(self.root, text="Start Game", width=15, command=self.open_game_window)
        start_btn.pack(pady=10)


    # ---------- Open Game Window -------------------
    def open_game_window(self):

        # destroy start window
        self.root.destroy()

        # create game window
        self.root = tk.Tk()
        self.root.title("Game Arena")
        self.root.geometry("800x400")

        title = tk.Label(self.root, text="Scoreboard", font=("Arial",16,"bold"))
        title.pack(pady=10)

        # match scoreboard
        self.match_label = tk.Label(
            self.root,
            text="Match Score  |  Player1: 0  -  Player2: 0",
            font=("Arial",12,"bold")
        )
        self.match_label.pack(pady=5)

        info = tk.Label(self.root, text=f"First to {self.target} clicks wins the round")
        info.pack()

        # round scores
        self.score1_label = tk.Label(self.root, text="Player 1: 0", font=("Arial",12))
        self.score1_label.pack(pady=5)

        self.score2_label = tk.Label(self.root, text="Player 2: 0", font=("Arial",12))
        self.score2_label.pack(pady=5)

        instructions = tk.Label(
            self.root,
            text="Player 1 → press A      Player 2 → press L",
            font=("Arial",11)
        )
        instructions.pack(pady=10)

        start_btn = tk.Button(self.root, text="Start Round", command=self.start_game)
        start_btn.pack(pady=5)

        reset_btn = tk.Button(self.root, text="Reset Scoreboard", command=self.reset_all)
        reset_btn.pack(pady=5)

        quit_btn = tk.Button(self.root, text="Quit", command=self.root.quit)
        quit_btn.pack(pady=5)

        # keyboard controls
        self.root.bind("a", self.player1_click)
        self.root.bind("l", self.player2_click)

        self.root.mainloop()


    def start_game(self):

        self.game_active = True
        self.score1 = 0
        self.score2 = 0
        self.update_display()


    def reset_all(self):

        self.score1 = 0
        self.score2 = 0
        self.player1_wins = 0
        self.player2_wins = 0
        self.game_active = False
        self.update_display()


    def player1_click(self, event):

        if self.game_active:
            self.score1 += 1
            self.update_display()
            self.check_winner()


    def player2_click(self, event):

        if self.game_active:
            self.score2 += 1
            self.update_display()
            self.check_winner()


    def update_display(self):

        self.score1_label.config(text=f"Player 1: {self.score1}")
        self.score2_label.config(text=f"Player 2: {self.score2}")

        self.match_label.config(
            text=f"Match Score  |  Player1: {self.player1_wins}  -  Player2: {self.player2_wins}"
        )


    def check_winner(self):

        if self.score1 >= self.target:

            self.player1_wins += 1
            self.game_active = False
            messagebox.showinfo("Round Winner", "Player 1 wins!")

            self.start_game()   # auto start next round


        elif self.score2 >= self.target:

            self.player2_wins += 1
            self.game_active = False
            messagebox.showinfo("Round Winner", "Player 2 wins!")

            self.start_game()   # auto start next round


FastClickGame()

