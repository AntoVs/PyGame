import tkinter as tk
from tkinter import messagebox, ttk
import random

class FastClickGame:
    def __init__(self):
        self.history_data = []
        self.p1_wins = 0
        self.p2_wins = 0
        self.show_main_menu()

    # ---------- Main Menu ----------
    def show_main_menu(self):
        self.root = tk.Tk()
        self.root.title("Fastest Click Wins - Menu")
        self.root.geometry("400x500")
        self.root.configure(bg="#121212") 

        # Title Section
        header_frame = tk.Frame(self.root, bg="#1a1a1a", pady=40)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="⚡ Mr.Clicky ⚡", font=("Impact", 35), fg="#00d2ff", bg="#1a1a1a").pack()
        tk.Label(header_frame, text="Battle Royale", font=("Impact", 25), fg="white", bg="#1a1a1a").pack()
        
        # Button Container
        btn_frame = tk.Frame(self.root, bg="#121212", pady=30)
        btn_frame.pack()

        # Start Button
        tk.Button(btn_frame, text="▶", width=22, height=2, bg="#2ecc71", fg="white", 
                  font=("Arial", 12, "bold"), relief="flat", command=self.open_game_window).pack(pady=10)
        
        # Match History Button
        tk.Button(btn_frame, text="↺ History ↺", width=22, height=2, bg="#34495e", fg="white", 
                  font=("Arial", 11), relief="flat", command=self.show_history_popup).pack(pady=10)
        
        # Red Exit Button
        tk.Button(btn_frame, text="EXIT", width=22, bg="#c0392b", fg="white", 
                  font=("Arial", 10), relief="flat", command=self.root.quit).pack(pady=30)

        self.root.mainloop()

    # MatchHistory-Popup
    def show_history_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Battle Logs")
        popup.geometry("350x400")
        popup.configure(bg="#1f1f1f")
        
        tk.Label(popup, text="RECENT MATCHES", font=("Arial", 12, "bold"), fg="#00d2ff", bg="#1f1f1f", pady=15).pack()
        list_frame = tk.Frame(popup, bg="#1f1f1f")
        list_frame.pack(padx=20, pady=10, fill="both", expand=True)
        history_list = tk.Listbox(list_frame, bg="#2d2d2d", fg="white", font=("Consolas", 10), borderwidth=0, highlightthickness=0)
        history_list.pack(side="left", fill="both", expand=True)
        scroll = tk.Scrollbar(list_frame, command=history_list.yview)
        scroll.pack(side="right", fill="y")
        history_list.config(yscrollcommand=scroll.set)

        if not self.history_data:
            history_list.insert(tk.END, " You Have No Legacy ,The world is not for the weak !")
        else:
            for record in self.history_data:
                history_list.insert(tk.END, f" {record}")
        tk.Button(popup, text="CLOSE", command=popup.destroy, bg="#444", fg="white", relief="flat").pack(pady=15)

    # ---------- Game Window
    def open_game_window(self):
        self.root.destroy()
        
        self.root = tk.Tk()
        self.root.title("")
        self.root.geometry("800x600")
        self.root.configure(bg="#0a0a0a")

        self.score1, self.score2 = 0, 0
        self.p1_wins, self.p2_wins = 0, 0
        self.target = 20
        self.win_limit = 3
        self.game_active = False

        self.match_label = tk.Label(self.root, text="", font=("Arial", 14), bg="#222", fg="#00ffcc", pady=10)
        self.match_label.pack(fill="x")

        self.status_label = tk.Label(self.root, text="READY?", font=("Impact", 60), fg="#f1c40f", bg="#0a0a0a", pady=20)
        self.status_label.pack()

        battle_frame = tk.Frame(self.root, bg="#0a0a0a")
        battle_frame.pack(expand=True, fill="both", padx=20)

        self.setup_player_ui(battle_frame)  # Player UI
        footer = tk.Frame(self.root, bg="#0a0a0a", pady=30)
        footer.pack(side="bottom")

        self.start_btn = tk.Button(footer, text="START ROUND", font=("Arial", 12, "bold"), bg="#2ecc71", fg="white", width=15, relief="flat", command=self.start_countdown)
        self.start_btn.pack(side="left", padx=10)

        tk.Button(footer, text="RESET MATCH", bg="#e67e22", fg="white", width=15, relief="flat", command=self.reset_all).pack(side="left", padx=10)
        
        tk.Button(footer, text="MAIN MENU", bg="#3498db", fg="white", width=15, relief="flat", command=self.return_to_menu).pack(side="left", padx=10)

        self.root.bind("a", self.player1_click); self.root.bind("A", self.player1_click)
        self.root.bind("l", self.player2_click); self.root.bind("L", self.player2_click)

        self.update_display()
        self.root.mainloop()

    def setup_player_ui(self, parent):
        # Player 1
        p1_f = tk.Frame(parent, bg="#0a0a0a")
        p1_f.pack(side="left", expand=True)
        tk.Label(p1_f, text="PLAYER 1", font=("Arial", 14, "bold"), fg="#3498db", bg="#0a0a0a").pack()
        self.score1_label = tk.Label(p1_f, text="0", font=("Arial", 70, "bold"), fg="white", bg="#0a0a0a")
        self.score1_label.pack()
        self.bar1 = ttk.Progressbar(p1_f, length=220)
        self.bar1.pack(pady=10)
        self.p1_rounds_label = tk.Label(p1_f, text="Wins: 0", font=("Arial", 11), fg="#777", bg="#0a0a0a")
        self.p1_rounds_label.pack()

        # Player 2
        p2_f = tk.Frame(parent, bg="#0a0a0a")
        p2_f.pack(side="right", expand=True)
        tk.Label(p2_f, text="PLAYER 2", font=("Arial", 14, "bold"), fg="#e74c3c", bg="#0a0a0a").pack()
        self.score2_label = tk.Label(p2_f, text="0", font=("Arial", 70, "bold"), fg="white", bg="#0a0a0a")
        self.score2_label.pack()
        self.bar2 = ttk.Progressbar(p2_f, length=220)
        self.bar2.pack(pady=10)
        self.p2_rounds_label = tk.Label(p2_f, text="Wins: 0", font=("Arial", 11), fg="#777", bg="#0a0a0a")
        self.p2_rounds_label.pack()

    # ---------- GameLogic
    def return_to_menu(self):
        self.root.destroy()
        self.show_main_menu()

    def start_countdown(self, count=3):
        self.game_active = False
        self.start_btn.config(state="disabled")
        if count > 0:
            self.status_label.config(text=str(count), fg="#e67e22")
            self.root.after(1000, lambda: self.start_countdown(count - 1))
        else:
            self.status_label.config(text="GO!", fg="#2ecc71")
            self.start_game()

    def start_game(self):
        self.target = random.randint(15, 30)
        self.bar1["maximum"] = self.target
        self.bar2["maximum"] = self.target
        self.game_active = True
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
        self.score1_label.config(text=self.score1)
        self.score2_label.config(text=self.score2)
        self.bar1["value"] = self.score1
        self.bar2["value"] = self.score2
        self.p1_rounds_label.config(text=f"Wins: {self.p1_wins}")
        self.p2_rounds_label.config(text=f"Wins: {self.p2_wins}")
        self.match_label.config(text=f"Series: Best of {self.win_limit}  |  Target: {self.target if self.game_active else '??'}")

    def check_winner(self):
        if self.score1 >= self.target or self.score2 >= self.target:
            self.game_active = False
            self.start_btn.config(state="normal")
            p1_won = self.score1 >= self.target
            
            if p1_won: self.p1_wins += 1
            else: self.p2_wins += 1

            if self.p1_wins >= self.win_limit or self.p2_wins >= self.win_limit:
                winner_name = "Player 1" if self.p1_wins >= self.win_limit else "Player 2"
                self.history_data.insert(0, f"{winner_name} won ({self.p1_wins}-{self.p2_wins})")
                messagebox.showinfo("Match Over", f"🏆 {winner_name} wins the match! 🏆")
                self.reset_all()
            else:
                messagebox.showinfo("Round Over", f"{'Player 1' if p1_won else 'Player 2'} wins the round!")
                self.score1, self.score2 = 0, 0 # Instant reset
                self.status_label.config(text="READY?", fg="#f1c40f")
                self.update_display()

    def reset_all(self):
        self.score1, self.score2 = 0, 0
        self.p1_wins, self.p2_wins = 0, 0
        self.game_active = False
        self.start_btn.config(state="normal")
        self.status_label.config(text="READY?", fg="#f1c40f")
        self.update_display()

if __name__ == "__main__":
    FastClickGame()

