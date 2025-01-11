import json
import random


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

    for _ in range(len(remaining_players)):
        if remaining_players:  # Ensure there are remaining players to distribute
            team_with_lowest_score = get_team_with_lowest_score()
            team_with_lowest_score.append(remaining_players.pop(0))

    # Return the teams with an equal number of players
    return team1, team2, team3


def create_balanced_teams_with_constraints(players, num_teams=3):
    if not players:  # Check if players is empty
        raise ValueError("No players available to create teams.")

    # Sort players by score in descending order
    players_sorted = sorted(players, key=lambda x: x['score'], reverse=True)

    # Initialize teams
    teams = [[] for _ in range(num_teams)]
    team_scores = [0] * num_teams

    high_score_threshold = 4.5
    max_high_score_players_per_team = 3
    max_score_diff = 2.5

    # Distribute players to teams
    for player in players_sorted:
        # Find the team with the least high score players
        teams_with_fewest_high_score_players = sorted(teams, key=lambda team: sum(
            1 for p in team if p['score'] >= high_score_threshold))

        # Find the team to add this player to
        for team in teams_with_fewest_high_score_players:
            high_score_players_in_team = sum(1 for p in team if p['score'] >= high_score_threshold)
            if high_score_players_in_team < max_high_score_players_per_team:
                team.append(player)
                break
        else:
            # If all teams have reached the high score player limit, add to the team with the lowest total score
            team_with_lowest_score = min(teams, key=lambda team: sum(p['score'] for p in team))
            team_with_lowest_score.append(player)

    # Check if the team score difference constraint is met
    def teams_score_diff_within_limit():
        team_totals = [sum(player['score'] for player in team) for team in teams]
        max_score = max(team_totals)
        min_score = min(team_totals)
        return (max_score - min_score) <= max_score_diff

    for _ in range(100):  # Try up to 100 times to balance teams
        if teams_score_diff_within_limit():
            return teams
        random.shuffle(players_sorted)
        teams = [[] for _ in range(num_teams)]
        for player in players_sorted:
            team_with_lowest_score = min(teams, key=lambda team: sum(p['score'] for p in team))
            team_with_lowest_score.append(player)

    raise ValueError("Unable to balance teams within score difference constraint")


def print_teams_to_file(teams, file_path):
    with open(file_path, 'w') as f:
        for i, team in enumerate(teams, start=1):
            # Write team name
            f.write(f"Team {i}:\n")

            # Write player names in the team
            for player in team:
                f.write(f"  {player['name']} (Score: {player['score']})\n")

            # Calculate and write total score
            total_score = sum(player['score'] for player in team)
            f.write(f"  Total Score: {total_score}\n\n")


def calculate_team_score(team):
    # Sum the scores of players in each team
    return sum(player["score"] for player in team)