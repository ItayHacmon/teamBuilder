import tkinter as tk
from tkinter import messagebox
import json
import os

class PlayerSelectionApp:
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete  # Store the callback function
        self.root.title("Player Selection App")
        self.root.geometry("800x600")  # Adjust window size

        self.players = self.load_players()  # Correct method call
        self.check_vars = []

        tk.Label(root, text="Select Players to be Online:", font=("Arial", 16, "bold")).pack(pady=10)

        self.create_checkboxes()
        tk.Button(root, text="Save Selections", command=self.save_players).pack(pady=10)

    def load_players(self):
        """Load players from the JSON file."""
        input_file_path = '/Users/ihacmon/Google Drive/My Drive/Itay/Itay/TeamBuilder/soccer_players.json'
        if not os.path.exists(input_file_path):
            messagebox.showerror("Error", f"File not found: {input_file_path}")
            self.root.quit()
        with open(input_file_path, 'r') as file:
            return json.load(file).get("Players", [])

    def create_checkboxes(self):
        """Create checkboxes for player selection."""
        for player in self.players:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(self.root, text=f'{player["name"]} - {player["position"]}', variable=var)
            cb.pack(anchor='w')
            self.check_vars.append((player, var))

    def save_players(self):
        """Save selected players and call the callback."""
        online_players = [player for player, var in self.check_vars if var.get()]
        self.on_complete(online_players)  # Use callback to notify completion
        self.root.destroy()
