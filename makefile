CXX = g++
CXXFLAGS = -O3 -Wall -std=c++17
SRC = src/radar.cpp
EXEC = ./radar
JGRAPH = ./jgraph/jgraph

# Put the team names, check the README for possible data
TEAMS =

# this indicator is for file name, For example "Arsenal Everton" would be "AE.pdf"
INDICATOR = $(shell echo $(TEAMS) | awk '{for(i=1;i<=NF;i++) printf substr($$i,1,1)}')

# Determines file name if empty, every team is compared so
ifeq ($(strip $(TEAMS)),)
    PDF_NAME = PLTeams.pdf
else
    PDF_NAME = $(INDICATOR).pdf
endif

all: $(EXEC) radar_plot

# compilation
$(EXEC): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(EXEC)

# give jgraph execute permission
prep:
	@chmod +x $(JGRAPH)

# generate plot, pass in the args TEAMS along with the filename
radar_plot: $(EXEC)
	$(EXEC) $(TEAMS) | $(JGRAPH) -P | ps2pdf - $(PDF_NAME)
	@echo "Generated $(PDF_NAME)"

clean:
	rm -f $(EXEC) *.pdf