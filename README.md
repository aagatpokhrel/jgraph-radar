
# jgraph-radar

A simple project for radar visualization for PL teams using JGraph. It compares teams using seven metrics: Interceptions, Tackles, Passes, Possession, Goals, Shots, and Fouls.

The tool supports multiple plotting modes:

- Single-team plot (visualize one team)
- Head-to-head (Team A vs Team B)
- Multi-team comparison (3+ teams)
- All-teams overview

Select which teams to plot by passing the `TEAMS` variable in the on the command line when building with make, for example:

```bash
make TEAMS="ManCity Arsenal"
```

See the Usage section below for examples and details.

## Project Structure

```
jgraph-radar/
├── README.md
├── Makefile
├── setup.sh
├── data/
│   └── pl_teams.csv
├── examples/
├── jgraph/ (this is pulled from setup.sh)
└── src/
	└── radar.cpp
```

## Generating Radar JGraphs (How?)

The radar visualization is created in four main steps:

### 1. Parsing Data

The whole data is read from the csv. The first column is team name, and other 7 are stats. So we safecheck for 8 columns. And normalize the 7 stats for the radar plot visualization.
```cpp
// For each team, normalize their stats to 0-1 by dividing by the max value
stat_normalized = team_stat / max_value_for_metric
```

### 2. Converting Coordinates

Since its a circle we need to convert the polar coordinated graph to X,Y coordinates so we could draw the graph.

```cpp
// num_axes = 7 (one for each metric)
angle = (metric_index × 360° / num_axes) + 90°
x = center_x + radius × cos(angle)
y = center_y + radius × sin(angle)
```

The normalized stat value is the radius. Ex: 1.0 reaches the outer edge, 0.5 reaches halfway.

### 3. Draw the Web/Grid

Create concentric circles (0%, 20%, 40%, 60%, 80%, 100%) and radial lines from center to outer edge. Add percentage labels along one axis.

### 4. Draw Team Polygons

For each team, I plot a point for every metric at the normalized radius, then connect all points into a filled polygon with a random color and label.


## Installation and Setup

1. There is a shell script file. Give execute permission to the file with `chmod +x setup.sh`.
2. Execute the shell script. It pulls jgraph and compiles it and then compiles and runs our program.
3. The Makefile for our jgraph-radar is run which essentially compiles the file to which TEAMS need to be visually displayed. This is further explained in Usage.


## Usage


```bash
# build and generate the default radar PDF (which builds graph for all teams)
make

# build and generate graph for specific teams
make TEAMS="Arsenal Wolves"
```
The upper command creates a graph for all the teams which is hard to see (but it can still be important to know which one is coming on top or bottom seeing the graph). 

The specific teams command creates a pdf file named `AW.pdf` taking in the first letter of both the teams. This compares two teams with the polygons, with all the metrics.

The lab contains team data in `data/pl_teams.csv`. The available teams are:

| Team |
|-----:|
| ManCity |
| Arsenal |
| ManUnited |
| Liverpool |
| Chelsea |
| Everton |
| CrystalPalace |
| AstonVilla |
| Newcastle |
| Bournemouth |
| Brentford |
| Brighton |
| Sunderland |
| Tottenham |
| Leeds |
| NottinghamForest |
| Fulham |
| WestHam |
| Burnley |
| Wolves |

The `makefile` uses the `TEAMS` value to build an indicator and create a PDF file.

## Requisites

- `g++` with C++17 support (the project is compiled with `-std=c++17`)
- `make`
- `awk` (used by the `makefile` to build the output name)
- `ps2pdf` (provided by Ghostscript) to convert the jgraph PostScript output to PDF
- Basic build tools (e.g., `gcc`, `make`) for compiling `jgraph` when `setup.sh` runs
