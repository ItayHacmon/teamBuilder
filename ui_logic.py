import tkinter as tk
from team_logic import create_balanced_teams, print_teams_to_file

class TeamBuilderUI:
    def __init__(self, root, players):
        self.root = root
        self.players = players
        self.create_ui()

    def create_ui(self):
        tk.Label(self.root, text="Team Builder UI", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text=f"Players: {len(self.players)}").pack(pady=5)

        # Button to create teams
        create_teams_button = tk.Button(self.root, text="Create Teams", command=self.create_and_display_teams)
        create_teams_button.pack(pady=10)

        # Text area to show the teams
        self.teams_text = tk.Text(self.root, height=15, width=60, borderwidth=2, relief="solid")
        self.teams_text.pack(pady=10)

    def create_and_display_teams(self):
        try:
            team1, team2, team3 = create_balanced_teams(self.players)
            self.display_teams_in_text_area([team1, team2, team3])
            file_path = 'teams.txt'
            print_teams_to_file([team1, team2, team3], file_path)
        except ValueError as e:
            self.teams_text.delete(1.0, tk.END)
            self.teams_text.insert(tk.END, str(e))

    def display_teams_in_text_area(self, teams):
        self.teams_text.delete(1.0, tk.END)  # Clear previous text

        for i, team in enumerate(teams, start=1):
            self.teams_text.insert(tk.END, f"Team {i}:\n")
            for player in team:
                self.teams_text.insert(tk.END, f"  {player['name']}\n")
            total_score = sum(player['score'] for player in team)
            self.teams_text.insert(tk.END, f"  Total Score: {total_score}\n\n")

if __name__ == '__main__':
    # Example usage
    example_players = [
        {"name": "Player A", "position": "defender", "score": 80},
        {"name": "Player B", "position": "attacker", "score": 75},
        {"name": "Player C", "position": "striker", "score": 90},
        {"name": "Player D", "position": "keeper", "score": 85},
        {"name": "Player E", "position": "defender", "score": 60},
        {"name": "Player F", "position": "attacker", "score": 70},
        {"name": "Player G", "position": "striker", "score": 88},
        {"name": "Player H", "position": "keeper", "score": 92},
        {"name": "Player I", "position": "defender", "score": 75},
        {"name": "Player J", "position": "attacker", "score": 80},
        {"name": "Player K", "position": "defender", "score": 65}
    ]
    root = tk.Tk()
    app = TeamBuilderUI(root, example_players)
    root.mainloop()