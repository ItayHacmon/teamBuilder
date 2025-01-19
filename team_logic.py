import json
import random

def fetch_players(filepath):
    with open(filepath, 'r') as file:
        # Parse the JSON content into a Python dictionary
        data = json.load(file)

    # Return the list of players from the "Players" key
    return data.get("Players", [])

def create_balanced_teams_with_constraints(players, num_teams=3):
    if not players:  # Check if players is empty
        raise ValueError("No players available to create teams.")

    # Sort players by score in descending order
    players_sorted = sorted(players, key=lambda x: x['score'], reverse=True)

    # Initialize teams
    teams = [[] for _ in range(num_teams)]

    high_score_threshold = 4.5
    max_high_score_players_per_team = 3
    max_score_diff = 2.5

    # Function to check constraints
    def can_add_player_to_team(player, team):
        if 'positions' not in player:
            raise ValueError("Player dictionary must have a 'positions' key")
        if player['positions'] == 'keeper' and any(p['positions'] == 'keeper' for p in team):
            return False
        if player['score'] >= high_score_threshold and sum(1 for p in team if p['score'] >= high_score_threshold) >= max_high_score_players_per_team:
            return False
        return True

    # Distribute players to teams
    for player in players_sorted:
        for team in sorted(teams, key=lambda team: (sum(p['score'] for p in team), len(team))):
            if can_add_player_to_team(player, team):
                team.append(player)
                break
        else:
            # If player cannot be added to any team due to constraints, add to the team with the lowest total score
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
            for team in sorted(teams, key=lambda team: (sum(p['score'] for p in team), len(team))):
                if can_add_player_to_team(player, team):
                    team.append(player)
                    break
            else:
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