import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

input_file_path = '/Users/ihacmon/Library/CloudStorage/GoogleDrive-ihacmon@paloaltonetworks.com/My Drive/Itay/Itay/TeamBuilder/soccer_players.json'


class ModifyPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modify Existing Player")

        tk.Label(root, text="Modify Existing Player", font=("Arial", 14)).pack(pady=10)

        tk.Label(root, text="Select Player:").pack(pady=5)
        self.player_dropdown = ttk.Combobox(root)
        self.player_dropdown.pack(pady=5)

        tk.Label(root, text="Player Positions:").pack(pady=5)
        self.position_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        for position in ["defender", "attacker", "striker", "keeper"]:
            self.position_listbox.insert(tk.END, position)
        self.position_listbox.pack(pady=5)

        tk.Label(root, text="Player Score (1-5, steps of 0.5):").pack(pady=5)
        self.score_entry = tk.Entry(root)
        self.score_entry.pack(pady=5)

        tk.Button(root, text="Save Player", command=self.save_player).pack(pady=10)

        self.load_players()
        self.player_dropdown.bind("<<ComboboxSelected>>", self.populate_fields)

    def load_players(self):
        if os.path.exists(input_file_path):
            with open(input_file_path, 'r') as file:
                data = json.load(file)
                self.players = data.get("Players", [])
                self.player_dropdown['values'] = [player["name"] for player in self.players]
        else:
            self.players = []
            self.player_dropdown['values'] = []

    def populate_fields(self, event):
        selected_player_name = self.player_dropdown.get()
        player = next((p for p in self.players if p["name"] == selected_player_name), None)
        if player:
            self.position_listbox.selection_clear(0, tk.END)
            for position in player["positions"]:
                index = self.position_listbox.get(0, tk.END).index(position)
                self.position_listbox.select_set(index)
            self.score_entry.delete(0, tk.END)
            self.score_entry.insert(0, player["score"])

    def save_player(self):
        selected_player_name = self.player_dropdown.get()
        player = next((p for p in self.players if p["name"] == selected_player_name), None)

        if player:
            player["positions"] = [self.position_listbox.get(i) for i in self.position_listbox.curselection()]
            try:
                player["score"] = float(self.score_entry.get())
                if player["score"] < 1 or player["score"] > 5 or player["score"] % 0.5 != 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Score must be a number between 1 and 5, in steps of 0.5!")
                return

            with open(input_file_path, 'w') as file:
                json.dump({"Players": self.players}, file, indent=4)

            messagebox.showinfo("Success", "Player modified successfully!")
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Player not found!")


if __name__ == "__main__":
    root = tk.Tk()
    app = ModifyPlayerApp(root)
    root.mainloop()