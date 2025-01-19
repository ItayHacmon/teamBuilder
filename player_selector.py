import tkinter as tk
from tkinter import messagebox
import json
import os

# Paths
input_file_path = '/Users/ihacmon/Library/CloudStorage/GoogleDrive-ihacmon@paloaltonetworks.com/My Drive/Itay/Itay/TeamBuilder/soccer_players.json'
output_file_path = '/Users/ihacmon/Library/CloudStorage/GoogleDrive-ihacmon@paloaltonetworks.com/My Drive/Itay/Itay/TeamBuilder/current_soccer_players.json'
last_selected_file_path = '/Users/ihacmon/Library/CloudStorage/GoogleDrive-ihacmon@paloaltonetworks.com/My Drive/Itay/Itay/TeamBuilder/last_selected_players.json'

POSITION_ORDER = ["keeper", "defender", "attacker", "striker"]

class PlayerSelectionApp:
    def __init__(self, root, on_complete):
        self.root = root
        self.root.title("Player Selection App")
        self.root.geometry("800x1000")  # Make the window bigger
        self.on_complete = on_complete

        self.players = self.load_players()
        self.selected_players = []  # List to keep track of selected players

        tk.Label(root, text="Select Players to be Online:", font=("Arial", 14)).pack(pady=10)

        # Create a frame for the listbox and scrollbar
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        # Create a scrollbar
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)

        # Create a listbox with multiple selection mode
        self.listbox = tk.Listbox(self.frame, selectmode=tk.MULTIPLE, yscrollcommand=self.scrollbar.set, width=70, height=40)  # Adjust width and height
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        # Configure scrollbar
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Insert player names into the listbox
        self.update_listbox()

        # Label to display the number of selected players
        self.selected_counter_label = tk.Label(root, text=f"Players selected: 0/{len(self.players)}", font=("Arial", 12))
        self.selected_counter_label.pack(pady=10)

        # Button to save selections and proceed
        self.save_button = tk.Button(root, text="Save Selections", command=self.save_players)
        self.save_button.pack(pady=10)

        # Button to remove selection
        self.remove_button = tk.Button(root, text="Remove Selection", command=self.remove_selection)
        self.remove_button.pack(pady=10)

        # Button to close the window
        self.close_button = tk.Button(root, text="Close", command=self.root.destroy)
        self.close_button.pack(pady=10)

        # Label to display the main menu text
        self.main_menu_label = tk.Label(root, text="", font=("Arial", 12), justify=tk.LEFT)
        self.main_menu_label.pack(pady=10)

        # Bind the listbox selection event to update the counter
        self.listbox.bind('<<ListboxSelect>>', self.update_selected_counter)

        # Ask the user if they want to load the last selected players
        if self.load_last_selected_players():
            self.ask_to_load_last_selected()

    def load_players(self):
        if not os.path.exists(input_file_path):
            messagebox.showerror("Error", f"File not found: {input_file_path}")
            self.root.quit()
        with open(input_file_path, 'r') as file:
            players = json.load(file).get("Players", [])
        return sorted(players, key=lambda p: p["name"])

    def load_last_selected_players(self):
        if os.path.exists(last_selected_file_path):
            with open(last_selected_file_path, 'r') as file:
                self.last_selected_players = json.load(file)
                return True
        return False

    def ask_to_load_last_selected(self):
        response = messagebox.askyesno("Load Last Selected Players", "Do you want to load the last selected players?")
        if response:
            self.selected_players = self.last_selected_players
            self.reapply_selection()
            self.update_selected_counter()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for player in self.players:
            self.listbox.insert(tk.END, f'{player["name"]} - {", ".join(player["positions"])}')
        self.reapply_selection()

    def reapply_selection(self):
        for player in self.selected_players:
            if player in self.players:
                index = self.players.index(player)
                self.listbox.select_set(index)

    def update_selected_counter(self, event=None):
        selected_indices = self.listbox.curselection()
        self.selected_players = [self.players[i] for i in selected_indices]
        selected_players_count = len(self.selected_players)
        self.selected_counter_label.config(text=f"Players selected: {selected_players_count}/{len(self.players)}")
        if selected_players_count > 24:
            messagebox.showerror("Error", "You cannot select more than 24 players.")

    def save_players(self):
        if len(self.selected_players) > 24:
            messagebox.showerror("Error", "Please select 24 or fewer players.")
            return
        if callable(self.on_complete):
            self.on_complete(self.selected_players)
        if self.root.winfo_exists():
            self.root.withdraw()
        with open(last_selected_file_path, 'w') as file:
            json.dump(self.selected_players, file)

        # Calculate scores for each team
        team_scores = {}
        teams = {"team 1": [], "team 2": [], "team 3": []}

        for player in self.selected_players:
            team = player.get("team")
            score = player.get("score", 0)
            if team not in team_scores:
                team_scores[team] = 0
            team_scores[team] += score
            if team == "Team 1":
                teams["team 1"].append(player)
            elif team == "Team 2":
                teams["team 2"].append(player)
            elif team == "Team 3":
                teams["team 3"].append(player)

        # Save selected players to teams.txt with team details and total scores
        with open('teams.txt', 'w') as file:
            for team_name, players in teams.items():
                file.write(f'{team_name}:\n')
                for player in players:
                    file.write(f'{player["name"]}\n')

    def remove_selection(self):
        self.listbox.selection_clear(0, tk.END)
        self.selected_players.clear()
        self.update_selected_counter()

if __name__ == "__main__":
    def on_player_selection_complete(selected_players):
        print(f"Selected players: {selected_players}")

    root = tk.Tk()
    app = PlayerSelectionApp(root, on_player_selection_complete)
    root.mainloop()