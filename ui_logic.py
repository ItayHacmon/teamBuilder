import tkinter as tk
from team_logic import create_balanced_teams_with_constraints, print_teams_to_file
import threading
import random

class TeamBuilderUI:
    def __init__(self, root, players):
        self.root = root
        self.players = players
        self.teams = None
        self.show_scores = False  # Add a flag to track score visibility
        self.create_ui()

    def create_ui(self):
        tk.Label(self.root, text="Team Builder UI", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text=f"Players: {len(self.players)}").pack(pady=5)

        # Button to create teams
        self.create_teams_button = tk.Button(self.root, text="Create Teams", command=self.create_and_display_teams)
        self.create_teams_button.pack(pady=10)

        # Button to regenerate teams (initially hidden)
        self.regenerate_button = tk.Button(self.root, text="Regenerate Team", command=self.start_regenerate_team_thread)
        self.regenerate_button.pack(pady=10)
        self.regenerate_button.pack_forget()

        # Button to toggle score visibility
        self.toggle_scores_button = tk.Button(self.root, text="Show Scores", command=self.toggle_scores)
        self.toggle_scores_button.pack(pady=10)

        # Text area to show the teams
        self.teams_text = tk.Text(self.root, height=15, width=60, borderwidth=2, relief="solid")
        self.teams_text.pack(pady=10)

        # Button to save teams (initially hidden)
        self.save_teams_button = tk.Button(self.root, text="Save Teams", command=self.save_teams)
        self.save_teams_button.pack(pady=10)
        self.save_teams_button.pack_forget()

    def create_and_display_teams(self):
        try:
            self.teams = create_balanced_teams_with_constraints(self.players)
            self.update_display()
            self.regenerate_button.pack()  # Show regenerate button
            self.save_teams_button.pack()  # Show save teams button
        except ValueError as e:
            self.teams_text.delete(1.0, tk.END)
            self.teams_text.insert(tk.END, str(e))

    def update_display(self):
        self.teams_text.delete(1.0, tk.END)  # Clear previous text
        for i, team in enumerate(self.teams, start=1):
            self.teams_text.insert(tk.END, f"Team {i}:\n")
            for player in team:
                if self.show_scores:
                    self.teams_text.insert(tk.END, f"  {player['name']} (Score: {player['score']})\n")
                else:
                    self.teams_text.insert(tk.END, f"  {player['name']}\n")
            total_score = sum(player['score'] for player in team)
            self.teams_text.insert(tk.END, f"  Total Score: {total_score}\n\n")

    def regenerate_team(self):
        if self.teams:
            self.teams = self.reshuffle_teams_with_constraints(self.teams)
            self.update_display()

    def start_regenerate_team_thread(self):
        regenerate_thread = threading.Thread(target=self.regenerate_team)
        regenerate_thread.start()

    def reshuffle_teams_with_constraints(self, teams):
        all_players = [player for team in teams for player in team]
        random.shuffle(all_players)

        # Recreate balanced teams with constraints
        num_teams = len(teams)
        balanced_teams = create_balanced_teams_with_constraints(all_players, num_teams)

        return balanced_teams

    def toggle_scores(self):
        self.show_scores = not self.show_scores
        self.toggle_scores_button.config(text="Hide Scores" if self.show_scores else "Show Scores")
        self.update_display()

    def save_teams(self):
        file_path = 'teams.txt'
        print_teams_to_file(self.teams, file_path)
        tk.messagebox.showinfo("Success", f"Teams saved to {file_path}")

if __name__ == '__main__':
    # Example usage
    example_players = [
        {"name": "Player A", "position": "defender", "score": 4.8},
        {"name": "Player B", "position": "attacker", "score": 4.6},
        {"name": "Player C", "position": "striker", "score": 4.9},
        {"name": "Player D", "position": "keeper", "score": 4.7},
        {"name": "Player E", "position": "defender", "score": 3.0},
        {"name": "Player F", "position": "attacker", "score": 3.5},
        {"name": "Player G", "position": "striker", "score": 4.2},
        {"name": "Player H", "position": "keeper", "score": 4.1},
        {"name": "Player I", "position": "defender", "score": 4.3},
        {"name": "Player J", "position": "attacker", "score": 3.8},
        {"name": "Player K", "position": "defender", "score": 2.5}
    ]
    root = tk.Tk()
    app = TeamBuilderUI(root, example_players)
    root.mainloop()