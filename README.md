
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

## Installation and Setup

1. There is a shell script file. Give execute permission to the file with `chmod +x setup.sh`.
2. Execute the shell script. It pulls jgraph and compiles it and then compiles and runs our program.
3. The Makefile for our jgraph-radar is run which essentially compiles the file to which TEAMS need to be visually displayed. This is further explained in Usage.


## Usage


```bash
# build and generate the default radar PDF (which builds graph for all teams)
make

# build and generate graph for specific teams
make TEAMS="ManCity Arsenal"
```

This then creates a pdf file named `MA.pdf` taking in the first letter of both the teams. The lab contains team data in `data/pl_teams.csv`. The available teams are:

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
