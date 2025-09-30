"""
Scraps Desktop Pet 🐭
Version: 1.2 (Expanded Features)

✨ Features:
- Walks randomly, speech bubble system
- Right-click menu with many activities:
   🗨️ Talk
   🧀 Feed
   📖 Read
   😂 Joke
   🎶 Sing
   💃 Dance
   🎲 Play Game
   💤 Sleep / Wake
   ⚙️ Settings (with check for updates)
   ℹ️ About
- Speech bubbles above Scraps’ head
- Settings window with toggles + update checker
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random

class ScrapsPet:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "white")

        self.canvas = tk.Canvas(root, width=160, height=180, bg="white", highlightthickness=0)
        self.canvas.pack()

        # State
        self.speech_bubble = None
        self.speech_text = None
        self.is_moving = True
        self.is_sleeping = False
        self.hand = None
        self.food = None
        self.idle_counter = 0
        self.jokes_enabled = True

        # Draw Scraps
        self.draw_scraps()

        # Bind actions
        self.canvas.bind("<Button-1>", self.wake_up)
        self.canvas.bind("<Button-3>", self.show_menu)

        # Start moving
        self.move_scraps()

    def draw_scraps(self):
        # Body (no tail)
        self.body = self.canvas.create_rectangle(60, 80, 100, 160, fill="saddlebrown", outline="black")
        self.belly = self.canvas.create_oval(65, 110, 95, 160, fill="peru", outline="")
        self.head = self.canvas.create_oval(50, 30, 110, 90, fill="saddlebrown", outline="black")
        self.ear_left = self.canvas.create_oval(40, 20, 65, 45, fill="saddlebrown", outline="black")
        self.ear_right = self.canvas.create_oval(95, 20, 120, 45, fill="saddlebrown", outline="black")

        # Face
        self.eye_left = self.canvas.create_oval(70, 50, 76, 56, fill="black")
        self.eye_right = self.canvas.create_oval(84, 50, 90, 56, fill="black")
        self.nose = self.canvas.create_polygon(78, 70, 82, 70, 80, 75, fill="pink")
        self.mouth = self.canvas.create_line(72, 80, 88, 80, width=2, fill="black")

    # ========== MENU ==========
    def show_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="🗨️ Talk", command=self.talk_to_scraps)
        menu.add_command(label="🧀 Feed", command=self.feed_scraps)
        menu.add_command(label="😂 Joke", command=self.tell_joke)
        menu.add_command(label="📖 Read", command=self.read_book)
        menu.add_command(label="🎶 Sing", command=self.sing_song)
        menu.add_command(label="💃 Dance", command=self.dance)
        menu.add_command(label="🎲 Play Game", command=self.play_game)
        menu.add_separator()
        if self.is_sleeping:
            menu.add_command(label="🌞 Wake", command=self.wake_up)
        else:
            menu.add_command(label="💤 Sleep", command=self.fall_asleep)
        menu.add_separator()
        menu.add_command(label="⚙️ Settings", command=self.open_settings)
        menu.add_command(label="ℹ️ About", command=self.show_about)
        menu.tk_popup(event.x_root, event.y_root)

    # ========== FEATURES ==========
    def talk_to_scraps(self):
        user_input = simpledialog.askstring("Talk to Scraps", "What do you want to say?")
        if user_input:
            reply = random.choice(["Oh really?", "That’s funny!", "I didn’t know that.", "Tell me more!", "Hmm…"])
            messagebox.showinfo("Scraps", f"You said: {user_input}\nScraps: {reply}")
            self.show_message(reply)

    def feed_scraps(self):
        if self.food:
            self.canvas.delete(self.food)
        self.food = self.canvas.create_text(80, 20, text="🧀", font=("Arial", 24))
        self.root.after(1000, self.eat_food)

    def eat_food(self):
        if self.food:
            self.canvas.delete(self.food)
            self.food = None
        messagebox.showinfo("Scraps", "Yum! Cheese makes me happy!")
        self.show_message("Yum! Cheese makes me happy!")

    def tell_joke(self):
        if not self.jokes_enabled:
            self.show_message("Jokes are disabled in settings.")
            return
        joke = random.choice([
            "Why don’t mice ever win races? They stop for cheese!",
            "I’m a mouse, not a computer mouse!",
            "Cheese is the answer to everything.",
        ])
        self.show_message(joke)
        messagebox.showinfo("Scraps' Joke", joke)

    def read_book(self):
        lines = ["Once upon a time...", "There was a little mouse...", "Who loved cheese!", "The end."]
        for i, line in enumerate(lines):
            self.root.after(1500 * i, lambda l=line: self.show_message(l))

    def sing_song(self):
        song = "🎶 Squeak squeak, cheese is neat! 🎶"
        self.show_message(song)
        messagebox.showinfo("Scraps sings", song)

    def dance(self):
        self.show_message("💃 Scraps is dancing!")
        for i in range(6):
            dx = 10 if i % 2 == 0 else -10
            self.root.after(i * 200, lambda d=dx: self.root.geometry(f"+{self.root.winfo_x()+d}+{self.root.winfo_y()}"))

    def play_game(self):
        q = simpledialog.askstring("Game", "Riddle: What has 4 legs but can’t walk?")
        if q is not None:
            messagebox.showinfo("Scraps", "Answer: A chair!")
            self.show_message("A chair! 🪑")

    def show_about(self):
        messagebox.showinfo("About Scraps", "Scraps the Mouse 🐭\nVersion 1.2\nExpanded Features!")

    # ========== SLEEP ==========
    def fall_asleep(self):
        self.is_sleeping = True
        self.is_moving = False
        self.show_message("Zzz... Sleeping")

    def wake_up(self, event=None):
        if self.is_sleeping:
            self.is_sleeping = False
            self.is_moving = True
            messagebox.showinfo("Scraps", "I just woke up!")
            self.show_message("I just woke up!")

    # ========== SETTINGS ==========
    def open_settings(self):
        win = tk.Toplevel(self.root)
        win.title("Scraps Settings")
        win.geometry("300x250")

        # Check for updates
        def check_updates():
            found = random.choice([True, False])
            if found:
                messagebox.showinfo("Updates", "New version available! (Pretend download)")
            else:
                messagebox.showinfo("Updates", "Scraps is up to date!")

        ttk.Button(win, text="Check for Updates", command=check_updates).pack(pady=10)

        # Joke toggle
        def toggle_jokes():
            self.jokes_enabled = not self.jokes_enabled
            status = "enabled" if self.jokes_enabled else "disabled"
            messagebox.showinfo("Settings", f"Jokes are now {status}.")

        ttk.Button(win, text="Toggle Jokes", command=toggle_jokes).pack(pady=10)

        ttk.Label(win, text="(More settings can be added later)").pack(pady=20)

    # ========== MESSAGES ==========
    def show_message(self, text):
        if self.speech_bubble:
            self.canvas.delete(self.speech_bubble)
            self.canvas.delete(self.speech_text)
        x1, y1, x2, y2 = 20, -70, 150, -20
        self.speech_bubble = self.canvas.create_oval(x1, y1, x2, y2, fill="yellow", outline="black")
        self.speech_text = self.canvas.create_text((85, -45), text=text, font=("Arial", 9), fill="black")
        self.root.after(4000, self.hide_message)

    def hide_message(self):
        if self.speech_bubble:
            self.canvas.delete(self.speech_bubble)
            self.canvas.delete(self.speech_text)
            self.speech_bubble = None
            self.speech_text = None

    # ========== MOVEMENT ==========
    def move_scraps(self):
        if self.is_moving and not self.is_sleeping:
            screen_w = self.root.winfo_screenwidth()
            screen_h = self.root.winfo_screenheight()
            x = random.randint(0, screen_w - 160)
            y = random.randint(screen_h - 250, screen_h - 180)
            self.root.geometry(f"160x180+{x}+{y}")
        self.root.after(5000, self.move_scraps)


if __name__ == "__main__":
    root = tk.Tk()
    app = ScrapsPet(root)
    root.mainloop()
