import json

def fetch_players(filepath):
    with open(filepath, 'r') as file:
        # Parse the JSON content into a Python dictionary
        data = json.load(file)

    # Return the list of players from the "Players" key
    return data.get("Players", [])


def create_balanced_teams(online_players):
    if not online_players:  # Check if online_players is empty
        raise ValueError("No players available to create teams.")

    # Split players into their respective position groups
    defenders = [player for player in online_players if player["position"] == "defender"]
    attackers = [player for player in online_players if player["position"] == "attacker"]
    strikers = [player for player in online_players if player["position"] == "striker"]
    keepers = [player for player in online_players if player["position"] == "keeper"]

    # Sort each position group by score in descending order
    defenders.sort(key=lambda player: player["score"], reverse=True)
    attackers.sort(key=lambda player: player["score"], reverse=True)
    strikers.sort(key=lambda player: player["score"], reverse=True)
    keepers.sort(key=lambda player: player["score"], reverse=True)

    # Initialize teams as empty lists
    team1, team2, team3 = [], [], []
    teams = [team1, team2, team3]

    # Function to get the team with the lowest total score
    def get_team_with_lowest_score():
        return min(teams, key=lambda team: sum(player["score"] for player in team))

    # Total number of players
    total_players = len(defenders) + len(attackers) + len(strikers) + len(keepers)

    # Number of players per team (as evenly as possible)
    players_per_team = total_players // 3
    extra_players = total_players % 3  # Number of extra players to distribute

    # Function to distribute players evenly to teams
    def distribute_players(position_group):
        while position_group:
            team_with_lowest_score = get_team_with_lowest_score()
            team_with_lowest_score.append(position_group.pop(0))

    # Distribute players from each position
    distribute_players(defenders)
    distribute_players(attackers)
    distribute_players(strikers)
    distribute_players(keepers)

    # If there are extra players, distribute them evenly across teams
    remaining_players = defenders + attackers + strikers + keepers

    for _ in range(extra_players):
        team_with_lowest_score = get_team_with_lowest_score()
        team_with_lowest_score.append(remaining_players.pop(0))

    # Return the teams with an equal number of players
    return team1, team2, team3


def print_teams_to_file(teams, file_path):
    with open(file_path, 'w') as f:
        for i, team in enumerate(teams, start=1):
            # Write team name
            f.write(f"team{i}\n")

            # Write player names in the team
            for player in team:
                f.write(f"{player['name']}\n")

            # Calculate and write total score
            total_score = sum(player['score'] for player in team)
            f.write(f"Total Score - {total_score}\n\n")


def calculate_team_score(team):
    # Sum the scores of players in each team
    team_score = sum(player["score"] for player in team)
    return team_score
