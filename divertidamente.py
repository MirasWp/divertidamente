import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import time


class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Divertidamente Game")
        self.root.geometry("600x700")

        self.images = self.load_images() * 2
        random.shuffle(self.images)

        self.revealed = []
        self.buttons = []
        self.matched_pairs = 0
        self.start_time = None
        self.timer_running = False

        self.timer_label = tk.Label(root, text="Time: 0s")
        self.timer_label.grid(row=5, column=0, columnspan=4)

        self.create_game_board()
        self.create_control_buttons()

    def load_images(self):
        images = []
        for i in range(1, 9):
            img = Image.open(f'test1/{i}.png')
            img = img.resize((150, 180), Image.LANCZOS)
            images.append(ImageTk.PhotoImage(img))
        return images

    def update_timer(self):
        if self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed_time}s")
            if elapsed_time <= 100:
                self.root.after(1000, self.update_timer)
            else:
                self.timer_running = False
                messagebox.showinfo(
                    "Time's up!", "You lost! Time exceeded 100 seconds.")
                self.disable_buttons()

    def create_game_board(self):
        for i in range(4):
            self.root.rowconfigure(i, weight=1)
            self.root.columnconfigure(i, weight=1)
            for j in range(4):
                idx = i * 4 + j
                button = tk.Button(self.root, text='', width=10, height=5,
                                   command=lambda idx=idx: self.reveal_image(idx))
                button.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                self.buttons.append(button)

    def reveal_image(self, idx):
        if not self.timer_running:
            return

        if not hasattr(self.buttons[idx], 'image_ref') and len(self.revealed) < 2:
            self.buttons[idx].config(image=self.images[idx])
            self.buttons[idx].image_ref = self.images[idx]
            self.revealed.append(idx)
            if len(self.revealed) == 2:
                self.root.after(1000, self.check_match)

        if self.matched_pairs == 8:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_running = False
            messagebox.showinfo("Game Over", f"Congratulations! You finished the game in {
                                elapsed_time} seconds.")
            self.disable_buttons()

    def check_match(self):
        idx1, idx2 = self.revealed
        if self.buttons[idx1].image_ref == self.buttons[idx2].image_ref:
            self.buttons[idx1].config(state='disabled')
            self.buttons[idx2].config(state='disabled')
            self.matched_pairs += 1
        else:
            self.buttons[idx1].config(image='', text='')
            self.buttons[idx2].config(image='', text='')
            del self.buttons[idx1].image_ref
            del self.buttons[idx2].image_ref
        self.revealed.clear()

        # Check if the game is finished
        if self.matched_pairs == 8:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_running = False
            messagebox.showinfo("Game Over", f"Congratulations! You finished the game in {
                                elapsed_time} seconds.")
            self.disable_buttons()

    def disable_buttons(self):
        for button in self.buttons:
            button.config(state='disabled')

    def start_game(self):
        self.start_time = time.time()
        self.timer_running = True
        self.matched_pairs = 0
        random.shuffle(self.images)
        for button in self.buttons:
            button.config(state='normal', image='', text='')
            if hasattr(button, 'image_ref'):
                del button.image_ref
        self.revealed.clear()
        self.update_timer()

    def restart_game(self):
        self.start_game()

    def end_game(self):
        self.root.quit()

    def create_control_buttons(self):
        start_button = tk.Button(
            self.root, text="Start", command=self.start_game)
        start_button.grid(row=6, column=0, columnspan=1, sticky="ew")

        restart_button = tk.Button(
            self.root, text="Restart", command=self.restart_game)
        restart_button.grid(row=6, column=1, columnspan=1, sticky="ew")

        end_button = tk.Button(
            self.root, text="End Game", command=self.end_game)
        end_button.grid(row=6, column=2, columnspan=2, sticky="ew")


if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
