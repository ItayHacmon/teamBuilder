from tkinter import Tk, Toplevel, Label, Button
from player_selector import PlayerSelectionApp
from ui_logic import TeamBuilderUI
import json

input_file_path = '/Users/ihacmon/Google Drive/My Drive/Itay/Itay/TeamBuilder/soccer_players.json'
output_file_path = '/Users/ihacmon/Google Drive/My Drive/Itay/Itay/TeamBuilder/current_soccer_players.json'


def on_player_selection_complete(players):
    """Callback after players are selected."""
    save_selected_players(players)
    show_team_building_window(players)


def save_selected_players(players):
    """Save selected players to the output file."""
    with open(output_file_path, 'w') as file:
        json.dump({"Players": players}, file, indent=4)
    print(f"Selected players saved to {output_file_path}")


def show_team_building_window(players):
    """Open a new window to handle team building after player selection."""
    team_window = Toplevel(root)
    team_window.title("Team Builder")
    Label(team_window, text="Team Building", font=("Arial", 14)).pack(pady=20)

    team_builder_ui = TeamBuilderUI(team_window, players)

    Button(team_window, text="Close", command=team_window.destroy).pack(pady=10)

    # Add Modify Selection button
    Button(team_window, text="Modify Selection", command=lambda: reopen_player_selection(team_window)).pack(pady=10)


def reopen_player_selection(team_window):
    """Reopen player selection window from team building window."""
    team_window.destroy()
    player_selection_window = Toplevel(root)
    PlayerSelectionApp(player_selection_window, on_player_selection_complete)


if __name__ == "__main__":
    root = Tk()
    root.title("Player Selection")
    PlayerSelectionApp(root, on_player_selection_complete)
    root.mainloop()