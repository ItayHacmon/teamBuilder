import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

input_file_path = '/Users/ihacmon/Google Drive/My Drive/Itay/Docs/Projects/teamBuilder/soccer_players.json'


class AddPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Add New Player")

        tk.Label(root, text="Add New Player", font=("Arial", 14)).pack(pady=10)

        tk.Label(root, text="Player Name:").pack(pady=5)
        self.name_entry = tk.Entry(root)
        self.name_entry.pack(pady=5)

        tk.Label(root, text="Player Positions:").pack(pady=5)
        self.position_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        for position in ["defender", "attacker", "striker", "keeper"]:
            self.position_listbox.insert(tk.END, position)
        self.position_listbox.pack(pady=5)

        tk.Label(root, text="Player Score (1-5, steps of 0.5):").pack(pady=5)
        self.score_entry = tk.Entry(root)
        self.score_entry.pack(pady=5)

        tk.Button(root, text="Save Player", command=self.save_player).pack(pady=10)

    def save_player(self):
        name = self.name_entry.get()
        positions = [self.position_listbox.get(i) for i in self.position_listbox.curselection()]
        score = self.score_entry.get()

        if not name or not positions or not score:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            score = float(score)
            if score < 1 or score > 5 or score % 0.5 != 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Score must be a number between 1 and 5, in steps of 0.5!")
            return

        new_player = {"name": name, "positions": positions, "score": score}

        if os.path.exists(input_file_path):
            with open(input_file_path, 'r') as file:
                data = json.load(file)
                players = data.get("Players", [])
        else:
            players = []

        players.append(new_player)

        with open(input_file_path, 'w') as file:
            json.dump({"Players": players}, file, indent=4)

        messagebox.showinfo("Success", "Player added successfully!")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AddPlayerApp(root)
    root.mainloop()