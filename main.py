import tkinter as tk
from ui import TeamBuilderUI
from player_selector import PlayerSelectionApp

def main():
    root = tk.Tk()

    # Callback function when player selection is complete
    def on_player_selection_complete():
        # Hide the current window (PlayerSelectionApp) and show the next one (TeamBuilderUI)
        root.deiconify()  # Show the main window again
        app = TeamBuilderUI(root)  # Create the TeamBuilderUI after selection is done

    # Start the PlayerSelectionApp and hide the root window
    root.withdraw()  # Hide the window initially
    select = PlayerSelectionApp(root, on_player_selection_complete)
    root.mainloop()

if __name__ == "__main__":
    main()
