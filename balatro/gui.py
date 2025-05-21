# balatro/gui.py
import tkinter as tk
from tkinter import messagebox, ttk
from .game import Game

class GameGUI(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.game = Game()
        self.selected = []
        self.setup_styles()
        self.show_welcome_screen()
        self.pack(expand=True, fill=tk.BOTH)
        self.master.geometry("800x600")
        self.master.configure(bg="#2e2e2e")

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", padding=6, font=('Arial', 10))
        self.style.configure("TLabel", font=('Arial', 10), background="#2e2e2e", foreground="white")
        self.style.configure("Selected.TButton", background="#4a6984")
        self.style.map("TButton",
            background=[("active", "#3a3a3a"), ("!disabled", "#2e2e2e")],
            foreground=[("!disabled", "white")]
        )
        self.style.configure("♥.TButton", foreground="#ff4444")
        self.style.configure("♦.TButton", foreground="#ff4444")
        self.style.configure("♣.TButton", foreground="#44ff44")
        self.style.configure("♠.TButton", foreground="#44ff44")

    def show_welcome_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        welcome_frame = ttk.Frame(self)
        welcome_frame.pack(expand=True, pady=50)

        ttk.Label(welcome_frame, text="BALATRO", font=('Arial', 24, 'bold')).pack(pady=20)
        ttk.Button(welcome_frame, text="Start Game", command=self.start_new_game).pack(pady=15, ipadx=20, ipady=10)
        ttk.Button(welcome_frame, text="Quit", command=self.master.destroy).pack(pady=15, ipadx=20, ipady=10)

    def start_new_game(self):
        self.game.reset_game()
        self.game.player.draw_hand()
        self.show_game_interface()

    def show_game_interface(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Status bar
        status_frame = ttk.Frame(self)
        status_frame.pack(fill=tk.X, padx=10, pady=5)

        self.round_label = ttk.Label(status_frame, text=f"Round: {self.game.round}")
        self.round_label.pack(side=tk.LEFT, padx=10)

        self.target_label = ttk.Label(status_frame, text=f"Target: {self.game.target_score}")
        self.target_label.pack(side=tk.LEFT, padx=10)

        self.chip_label = ttk.Label(status_frame, text=f"Chips: {self.game.player.chips}")
        self.chip_label.pack(side=tk.LEFT, padx=10)

        self.mult_label = ttk.Label(status_frame, text=f"Multiplier: {self.game.player.multiplier}x")
        self.mult_label.pack(side=tk.LEFT, padx=10)

        # Card display
        self.card_frame = ttk.Frame(self)
        self.card_frame.pack(pady=20, expand=True)

        # Control buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Play Selected", command=self.play_cards).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Discard All", command=self.discard_all).pack(side=tk.LEFT, padx=5)

        self.update_display()

    def update_display(self):
        # Clear current cards
        for widget in self.card_frame.winfo_children():
            widget.destroy()

        # Create new card buttons
        for idx, card in enumerate(self.game.player.hand):
            btn = ttk.Button(
                self.card_frame,
                text=str(card),
                style=f"{card.suit}.TButton",
                command=lambda i=idx: self.toggle_card(i)
            )
            if idx in self.selected:
                btn.configure(style="Selected.TButton")
            btn.grid(row=0, column=idx, padx=5, pady=5)

        # Update status labels
        self.round_label.config(text=f"Round: {self.game.round}")
        self.target_label.config(text=f"Target: {self.game.target_score}")
        self.chip_label.config(text=f"Chips: {self.game.player.chips}")
        self.mult_label.config(text=f"Multiplier: {self.game.player.multiplier}x")

    def toggle_card(self, index):
        if index in self.selected:
            self.selected.remove(index)
        else:
            self.selected.append(index)
        self.update_display()

    def play_cards(self):
        if not self.selected:
            messagebox.showwarning("No Selection", "Please select at least 1 card!")
            return

        played = [self.game.player.hand[i] for i in self.selected]
        hand_type = self.game.evaluate_hand(played)
        score = self.game.calculate_score(hand_type)

        if score >= self.game.target_score:
            self.handle_success(score)
        else:
            self.handle_failure(hand_type, score)

    def handle_success(self, score):
        self.game.player.chips += score // 10
        self.game.round += 1
        self.game.target_score = int(self.game.target_score * 1.5)
        self.game.player.discard_hand()
        self.game.player.draw_hand()
        self.selected = []
        self.update_display()
        self.show_shop()
        messagebox.showinfo("Success!", f"Scored {score} points!\nNext target: {self.game.target_score}")

    def handle_failure(self, hand_type, score):
        self.show_game_over(hand_type, score)

    def discard_all(self):
        self.game.player.discard_hand()
        self.game.player.draw_hand()
        self.selected = []
        self.update_display()

    def show_shop(self):
        shop = tk.Toplevel(self.master)
        shop.title("Shop")
        shop.geometry("400x300")
        shop.grab_set()

        ttk.Label(shop, text="Available Upgrades", font=('Arial', 14)).pack(pady=10)

        upgrades = [
            ("Multiplier +0.5x", 50, lambda: setattr(self.game.player, 'multiplier', self.game.player.multiplier + 0.5)),
            ("Chips +20", 30, lambda: setattr(self.game.player, 'chips', self.game.player.chips + 20)),
            ("Refresh Deck", 40, self.game.player.recycle_discard)
        ]

        for name, cost, effect in upgrades:
            frame = ttk.Frame(shop)
            frame.pack(fill=tk.X, padx=20, pady=5)

            ttk.Label(frame, text=name).pack(side=tk.LEFT)
            ttk.Label(frame, text=f"Cost: {cost}").pack(side=tk.LEFT, padx=20)

            ttk.Button(
                frame,
                text="Buy",
                command=lambda e=effect, c=cost: self.purchase_upgrade(e, c, shop)
            ).pack(side=tk.RIGHT)

    def purchase_upgrade(self, effect, cost, window):
        if self.game.player.chips >= cost:
            self.game.player.chips -= cost
            effect()
            self.update_display()
            window.destroy()
            messagebox.showinfo("Purchased", "Upgrade applied!")
        else:
            messagebox.showerror("Error", "Not enough chips!")

    def show_game_over(self, hand_type, score):
        game_over = tk.Toplevel(self.master)
        game_over.title("Game Over")
        game_over.geometry("300x200")

        ttk.Label(game_over, text="GAME OVER", font=('Arial', 16, 'bold')).pack(pady=10)
        ttk.Label(game_over, text=f"Final Hand: {hand_type}").pack()
        ttk.Label(game_over, text=f"Final Score: {score}").pack(pady=5)

        btn_frame = ttk.Frame(game_over)
        btn_frame.pack(pady=15)

        ttk.Button(
            btn_frame,
            text="New Game",
            command=lambda: [game_over.destroy(), self.start_new_game()]
        ).pack(side=tk.LEFT, padx=10)

        ttk.Button(
            btn_frame,
            text="Quit",
            command=self.master.destroy
        ).pack(side=tk.RIGHT, padx=10)