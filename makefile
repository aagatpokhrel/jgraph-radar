GEN = python3 src/radar.py
JGRAPH = ./jgraph
TEAMS = "Man United" "Liverpool" "Man City" "Chelsea" "Arsenal"

all: radars

radars:
	# Loop through teams and generate PDFs
	for team in $(TEAMS); do \
		$(GEN) "$$team" | $(JGRAPH) -P | ps2pdf - "$$team.pdf"; \
	done

clean:
	rm -f *.pdf