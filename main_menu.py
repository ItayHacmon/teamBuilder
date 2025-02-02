from tkinter import Tk, Toplevel, Button, Label
from player_selector import PlayerSelectionApp
from add_player import AddPlayerApp
from modify_player import ModifyPlayerApp
from ui_logic import TeamBuilderUI
import json

input_file_path = '/Users/ihacmon/Google Drive/My Drive/Itay/Docs/Projects/teamBuilder/soccer_players.json'
output_file_path = '/Users/ihacmon/Google Drive/My Drive/Itay/Docs/Projects/teamBuilder/current_soccer_players.json'

selected_players = []

def on_player_selection_complete(players):
    """Callback after players are selected."""
    global selected_players, player_selection_window
    selected_players = players
    save_selected_players(players)
    if player_selection_window.winfo_exists():
        player_selection_window.destroy()
    create_teams_button.config(state='normal')
    menu_window.deiconify()

def save_selected_players(players):
    """Save selected players to the output file."""
    with open(output_file_path, 'w') as file:
        json.dump({"Players": players}, file, indent=4)
    print(f"Selected players saved to {output_file_path}")

def open_player_selection():
    """Open the player selection window."""
    global player_selection_window
    player_selection_window = Toplevel(root)
    PlayerSelectionApp(player_selection_window, on_player_selection_complete)

def open_add_player():
    """Open the add player window."""
    add_player_window = Toplevel(root)
    AddPlayerApp(add_player_window)

def open_modify_player():
    """Open the modify player window."""
    modify_player_window = Toplevel(root)
    ModifyPlayerApp(modify_player_window)

def open_team_builder():
    """Open the team builder window."""
    if selected_players:
        team_window = Toplevel(root)
        TeamBuilderUI(team_window, selected_players)

def exit_app():
    """Exit the application."""
    root.quit()

def main():
    global root, menu_window, create_teams_button

    root = Tk()
    root.title("Main Menu")

    menu_window = Toplevel(root)
    menu_window.title("Main Menu")
    menu_window.geometry("400x400")  # Increase the size of the main menu window
    menu_window.protocol("WM_DELETE_WINDOW", exit_app)

    Label(menu_window, text="Main Menu", font=("Arial", 16)).pack(pady=20)

    Button(menu_window, text="Player Selection", command=open_player_selection).pack(pady=10)
    Button(menu_window, text="Add New Player", command=open_add_player).pack(pady=10)
    Button(menu_window, text="Modify Existing Player", command=open_modify_player).pack(pady=10)
    create_teams_button = Button(menu_window, text="Create Teams", command=open_team_builder, state='disabled')
    create_teams_button.pack(pady=10)
    Button(menu_window, text="Exit", command=exit_app).pack(pady=10)

    root.withdraw()
    root.mainloop()

if __name__ == "__main__":
    main()