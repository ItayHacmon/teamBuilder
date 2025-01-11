import tkinter as tk
from tkinter import messagebox
import json
import os

# Paths
input_file_path = '/Users/ihacmon/Google Drive/My Drive/Itay/Itay/TeamBuilder/soccer_players.json'
output_file_path = '/Users/ihacmon/Google Drive/My Drive/Itay/Itay/TeamBuilder/current_soccer_players.json'
last_selected_file_path = '/Users/ihacmon/Google Drive/My Drive/Itay/Itay/TeamBuilder/last_selected_players.json'


class PlayerSelectionApp:
    def __init__(self, root, on_complete):
        self.root = root
        self.root.title("Player Selection App")
        self.on_complete = on_complete

        self.players = self.load_players()
        self.last_selected_players = self.load_last_selected_players()

        tk.Label(root, text="Select Players to be Online:", font=("Arial", 14)).pack(pady=10)

        # Create a frame for the listbox and scrollbar
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        # Create a scrollbar
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)

        # Create a listbox with multiple selection mode
        self.listbox = tk.Listbox(self.frame, selectmode=tk.MULTIPLE, yscrollcommand=self.scrollbar.set, width=50,
                                  height=20)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        # Configure scrollbar
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Insert player names into the listbox
        for player in self.players:
            self.listbox.insert(tk.END, f'{player["name"]} - {player["position"]}')

        # Label to display the number of selected players
        self.selected_counter_label = tk.Label(root, text=f"Players selected: 0/{len(self.players)}",
                                               font=("Arial", 12))
        self.selected_counter_label.pack(pady=10)

        # Button to save selections and proceed
        self.save_button = tk.Button(root, text="Save Selections", command=self.save_players)
        self.save_button.pack(pady=10)

        # Bind the listbox selection event to update the counter
        self.listbox.bind('<<ListboxSelect>>', self.update_selected_counter)

        # Ask the user if they want to load the last selected players
        if self.last_selected_players:
            self.ask_to_load_last_selected()

    def load_players(self):
        if not os.path.exists(input_file_path):
            messagebox.showerror("Error", f"File not found: {input_file_path}")
            self.root.quit()
        with open(input_file_path, 'r') as file:
            return json.load(file).get("Players", [])

    def load_last_selected_players(self):
        if os.path.exists(last_selected_file_path):
            with open(last_selected_file_path, 'r') as file:
                return json.load(file)
        return []

    def ask_to_load_last_selected(self):
        response = messagebox.askyesno("Load Last Selected Players", "Do you want to load the last selected players?")
        if response:
            for player in self.last_selected_players:
                index = next((i for i, p in enumerate(self.players) if p["name"] == player["name"]), None)
                if index is not None:
                    self.listbox.select_set(index)
            self.update_selected_counter()

    def update_selected_counter(self, event=None):
        # Count the number of selected players
        selected_players = len(self.listbox.curselection())
        # Update the label with the current count of selected players
        self.selected_counter_label.config(text=f"Players selected: {selected_players}/{len(self.players)}")

        # Show error if more than 24 players are selected
        if selected_players > 24:
            messagebox.showerror("Error", "You cannot select more than 24 players.")

    def save_players(self):
        """Handles the action of saving selected players."""
        selected_indices = self.listbox.curselection()
        online_players = [self.players[i] for i in selected_indices]
        if len(online_players) > 24:
            messagebox.showerror("Error", "Please select 24 or fewer players.")
            return
        if callable(self.on_complete):
            self.on_complete(online_players)
        try:
            self.root.withdraw()
            self.root.update()
        except Exception as e:
            print(f"Error: {e}")
        # Save the last selected players
        with open(last_selected_file_path, 'w') as file:
            json.dump(online_players, file)


if __name__ == "__main__":
    # Example of how to use this app in the main loop
    def on_player_selection_complete(selected_players):
        print(f"Selected players: {selected_players}")


    root = tk.Tk()
    app = PlayerSelectionApp(root, on_player_selection_complete)
    root.mainloop()