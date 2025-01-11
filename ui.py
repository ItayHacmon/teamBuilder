import tkinter as tk
from tkinter import filedialog, messagebox
from models import fetch_players, create_balanced_teams, calculate_team_score


class TeamBuilderUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Team Builder App")

        self.file_label = tk.Label(root, text="No file selected")
        self.file_label.pack()

        self.upload_button = tk.Button(root, text="Select players file", command=self.load_players)
        self.upload_button.pack()

        self.generate_button = tk.Button(root, text="Generate Teams", command=self.generate_teams, state=tk.DISABLED)
        self.generate_button.pack()

        self.output_text = tk.Text(root, height=15, width=50)
        self.output_text.pack()

    def load_players(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.file_label.config(text=f"Loaded: {file_path}")
            self.players_data = fetch_players(file_path)
            self.generate_button.config(state=tk.NORMAL)

    def generate_teams(self):
        team1, team2, team3 = create_balanced_teams(self.players_data)
        self.display_teams(team1, team2, team3)

    def display_teams(self, team1, team2, team3):
        self.output_text.delete(1.0, tk.END)

        def format_team(team, name):
            return f"{name}\n" + "\n".join(f'{p["name"]} - {p["position"]} (Score: {p["score"]})' for p in team) + \
                f"\nTotal Score: {calculate_team_score(team)}\n\n"

        self.output_text.insert(tk.END, format_team(team1, "Team 1"))
        self.output_text.insert(tk.END, format_team(team2, "Team 2"))
        self.output_text.insert(tk.END, format_team(team3, "Team 3"))
