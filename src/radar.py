import math
import sys
import pandas as pd

# Loading data 
df = pd.read_csv("data/pl_teams.csv")
# Clean the column possession which represents in %
df['Possession'] = df['Possession'].str.rstrip('%').astype(float)

labels = ["Interceptions", "Tackles", "Passes", "Possession", "Goals", "Shots", "Fouls"]

team_data = {
    row['Teams']: [row[label] for label in labels] 
    for _, row in df.iterrows()
}

team_colors = {
    row['Teams']: row['Color'].replace(',', '') 
    for _, row in df.iterrows()
}

# multiply by 1.1 to extend the maximum
max_vals = [df[label].max() * 1.1 for label in labels]

def get_jgraph(team_names):
    if not(team_names):
        # include all teams
        team_names = team_data.keys()
    for name in team_names:
        if name not in team_data:
            print(f"(* Error: Team {name} not found *)")
            return

    center_x, center_y = 5, 5
    max_radius = 4
    num_axes = len(labels)

    print("newgraph")
    print("xaxis min 0 max 10 nodraw")
    print("yaxis min 0 max 10 nodraw")

    # Legend configuration
    print("legend top")

    # change as needed
    web_distance = [0.2, 0.4, 0.6, 0.8, 1.0]
    scale = 1.5
    # Background web
    for level in web_distance:
        print(f"newcurve linetype solid gray .8 poly pfill -1 pts", end="")
        for i in range(num_axes):
            angle = (i * 2 * math.pi / num_axes) + (math.pi / 2)
            px = center_x + (scale * level * max_radius * math.cos(angle))
            py = center_y + (scale * level * max_radius * math.sin(angle))
            print(f" {px:.2f} {py:.2f}", end="")
        print()

    #draw 7 lines from center_x, center_y to last polygon
    for i in range(num_axes):
        angle = (i * 2 * math.pi / num_axes) + (math.pi / 2)
        px = center_x + (scale * 1.0 * max_radius * math.cos(angle))
        py = center_y + (scale * 1.0 * max_radius * math.sin(angle))
        print(f"newcurve linetype solid gray .8 pts {center_x} {center_y} {px:.2f} {py:.2f}")

    # label each levels with a % level
    for level in web_distance:
        angle = (0 * 2 * math.pi / num_axes) + (math.pi / 2)
        lx = center_x + (scale * level * max_radius * math.cos(angle))
        ly = center_y + (scale * level * max_radius * math.sin(angle))
        # Offset the label slightly to the right for visibility
        print(f"newstring hjl vjc fontsize 8 x {lx+0.1:.2f} y {ly:.2f} : {int(level*100)}%")

    # Draw the team polygons with legends
    for index, name in enumerate(team_names):
        stats = team_data[name]
        color = team_colors.get(name, "0.5 0.5 0.5")
        
        # Polygon with label for the legend
        print(f"newline poly ", end="")
        print(f"color {color} linethickness 5 pfill -1 label : {name} \n pts", end="")
        
        points = []
        for i in range(num_axes):
            normalized = stats[i] / max_vals[i]
            angle = (i * 2 * math.pi / num_axes) + (math.pi / 2)
            px = center_x + (scale * normalized * max_radius * math.cos(angle))
            py = center_y + (scale * normalized * max_radius * math.sin(angle))
            points.append((px, py))
            print(f" {px:.2f} {py:.2f}", end="")
        print()


    # Labels
    for i in range(num_axes):
        angle = (i * 2 * math.pi / num_axes) + (math.pi / 2)
        lx = center_x + (1.1 * scale * max_radius * math.cos(angle))
        ly = center_y + (1.1 * scale * max_radius * math.sin(angle))
        print(f"newstring hjc vjc font Helvetica fontsize 10 x {lx:.2f} y {ly:.2f} : {labels[i]}")

    # Generating Title
    if len(team_names) == 2: title = " vs ".join(team_names) + " Stats"
    elif len(team_names) == 1: title = team_names[0] + " Playing Stats"
    else: title = "Premier League Teams Stats"
    print(f"newstring hjc vjc x 5 y -5 font Helvetica-Bold fontsize 10 : {title}")

if __name__ == "__main__":
    get_jgraph(sys.argv[1:])