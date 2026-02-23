import math
import sys

# Dummy data for the 2025/26 Premier League Teams
# Format: Team: [Interceptions, Tackles, Passes, Possession, Goals, Shots, Fouls]
team_data = {
    "Man United": [12.5, 18.2, 540, 54.2, 1.8, 14.2, 11.5],
    "Liverpool": [10.2, 15.5, 610, 60.1, 2.4, 18.5, 9.2],
    "Man City": [8.5, 14.1, 720, 65.5, 2.8, 20.1, 8.4],
    "Chelsea": [11.0, 19.5, 580, 56.8, 1.6, 13.5, 12.1],
    "Arsenal": [9.8, 16.2, 630, 59.5, 2.1, 16.8, 10.5]
}

# Color mapping (RGB)
team_colors = {
    "Man United": "1.0 0.1 0.1",
    "Liverpool": "0.8 0.0 0.0",
    "Man City": "0.4 0.7 1.0",
    "Chelsea": "0.0 0.0 0.8",
    "Arsenal": "0.9 0.0 0.0"
}

def get_jgraph(team_name):
    if team_name not in team_data:
        print(f"(* Error: Team {team_name} not found *)")
        return

    stats = team_data[team_name]
    labels = ["Interceptions", "Tackles", "Passes", "Possession", "Goals", "Shots", "Fouls"]
    
    # Lab Requirement: Non-trivial data normalization
    # We scale each stat to a max value to ensure they fit the radar
    max_vals = [15, 25, 800, 70, 3.5, 25, 15] 
    
    center_x, center_y = 5, 5
    max_radius = 4
    num_axes = len(stats)

    print("newgraph")
    print("xaxis min 0 max 10 nodraw")
    print("yaxis min 0 max 10 nodraw")

    # Draw background web (concentric heptagons)
    for level in [0.2, 0.4, 0.6, 0.8, 1.0]:
        print(f"newcurve linetype solid gray .8 poly pfill -1 pts", end="")
        for i in range(num_axes):
            angle = (i * 2 * math.pi / num_axes) + (math.pi / 2)
            px = center_x + (level * max_radius * math.cos(angle))
            py = center_y + (level * max_radius * math.sin(angle))
            print(f" {px:.2f} {py:.2f}", end="")
        print()

    # Draw the team polygon
    color = team_colors.get(team_name, "0.5 0.5 0.5")
    print(f"newcurve linetype solid poly pcfill {color} color {color} linethickness 2 pts", end="")
    for i in range(num_axes):
        # Lab Requirement: Coordinate math (Trigonometry)
        normalized = stats[i] / max_vals[i]
        angle = (i * 2 * math.pi / num_axes) + (math.pi / 2)
        px = center_x + (normalized * max_radius * math.cos(angle))
        py = center_y + (normalized * max_radius * math.sin(angle))
        print(f" {px:.2f} {py:.2f}", end="")
    print()

    # Draw labels with rotation
    for i in range(num_axes):
        angle = (i * 2 * math.pi / num_axes) + (math.pi / 2)
        lx = center_x + (1.1 * max_radius * math.cos(angle))
        ly = center_y + (1.1 * max_radius * math.sin(angle))
        print(f"newstring hjc vjc font Helvetica fontsize 10 x {lx:.2f} y {ly:.2f} : {labels[i]}")

    print(f"newstring hjc vjc x 5 y 0.5 font Helvetica-Bold fontsize 16 : {team_name} - 2026 Profile")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("(* Usage: python3 gen_radar.py <TeamName> *)")
    else:
        get_jgraph(sys.argv[1])