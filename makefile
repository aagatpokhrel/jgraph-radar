CXX = g++
CXXFLAGS = -O3 -Wall -std=c++17
SRC = src/radar.cpp
EXEC = ./radar
JGRAPH = ./jgraph

# Put the team names, check the README for possible data
TEAMS = "Arsenal" "Everton" "CrystalPalace" "Wolves"

# Determines file name if empty, every team is compared so
ifeq ($(strip $(TEAMS)),)
    PDF_NAME = PLTeams.pdf
else
    PDF_NAME = $(TEAMS).pdf
endif

all: $(EXEC) radar_plot

# compilation
$(EXEC): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(EXEC)

# generate plot, pass in the args TEAMS along with the filename
radar_plot: $(EXEC)
	$(EXEC) $(TEAMS) | $(JGRAPH) -P | ps2pdf - $(PDF_NAME)
	@echo "Generated $(PDF_NAME)"

clean:
	rm -f $(EXEC) *.pdf