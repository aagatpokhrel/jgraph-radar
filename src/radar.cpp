#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <map>
#include <cmath>
#include <iomanip>
#include <algorithm>
#include <random>

using namespace std;

struct Team {
    string name;
    vector<double> stats;
};

// cleaning text strings
string trim(string s, char extra = ' ') {
    s.erase(remove(s.begin(), s.end(), extra), s.end());
    return s;
}

// metrics
const vector<string> labels = {"Interceptions", "Tackles", "Passes", "Possession", "Goals", "Shots", "Fouls"};
const double center_x = 5.0, center_y = 5.0, max_radius = 4.0;
const double scale = 1.5; // scale of the graph

// function to provide x and y, based on centre and radius
void get_coords(int index, double radius, double &x, double &y) {
    int num_axes = labels.size();
    double angle = (index * 2 * M_PI / num_axes) + (M_PI / 2);
    x = center_x + (scale * radius * max_radius * cos(angle));
    y = center_y + (scale * radius * max_radius * sin(angle));
}

// get random color for each team polygon (got from google search)
string get_random_color() {
    static mt19937 gen(time(0));
    uniform_real_distribution<> dis(0.0, 1.0);
    stringstream ss;
    ss << fixed << setprecision(2) << dis(gen) << " " << dis(gen) << " " << dis(gen);
    return ss.str();
}

map<string, Team> load_data(const string& filename, vector<double>& max_vals) {
    ifstream file(filename);
    map<string, Team> team_map;
    string line, word;

    if (!file.is_open()) return team_map;

    // this skips the header
    getline(file, line);
    max_vals.assign(labels.size(), 0.0);

    while (getline(file, line)) {
        stringstream ss(line);
        vector<string> row;
        while (getline(ss, word, ',')) row.push_back(word);
        
        // there needs to be 8 colums (team name + 7 metrics)
        if (row.size() < 8) continue;

        Team t;
        t.name = row[0];

        for (int i = 0; i < 7; ++i) {
            string val_str = row[i + 1];
            // the possession contains the value in %, remove '%' sign
            val_str.erase(remove(val_str.begin(), val_str.end(), '%'), val_str.end());
            double val = stod(val_str);
            t.stats.push_back(val);
            if (val > max_vals[i]) max_vals[i] = val;
        }
        team_map[t.name] = t;
    }
    // scale max vals by 1.1 just to stretch the radar
    for (double &m : max_vals) m *= 1.1;
    return team_map;
}

void render_jgraph(const vector<string>& team_names, map<string, Team>& team_map, const vector<double>& max_vals) {
    vector<double> web_distance = {0.2, 0.4, 0.6, 0.8, 1.0};
    int num_axes = labels.size();

    cout << fixed << setprecision(2);
    cout << "newgraph\nxaxis min 0 max 10 nodraw\nyaxis min 0 max 10 nodraw\nlegend top\n";

    // background web
    for (double level : web_distance) {
        cout << "newcurve linetype solid gray .8 poly pfill -1 pts";
        for (int i = 0; i < num_axes; ++i) {
            double px, py;
            get_coords(i, level, px, py);
            cout << " " << px << " " << py;
        }
        cout << endl;
    }
    // the lines from center to the last web
    for (int i = 0; i < num_axes; ++i) {
        double px, py;
        get_coords(i, 1.0, px, py);
        cout << "newcurve linetype solid gray .8 pts " << center_x << " " << center_y << " " << px << " " << py << endl;
    }

    // percentage labels on the web
    for (double level : web_distance) {
        double lx, ly;
        get_coords(0, level, lx, ly);
        cout << "newstring hjl vjc fontsize 8 x " << (lx + 0.1) << " y " << ly << " : " << (int)(level * 100) << "%\n";
    }

    // constructing polygons for each team
    for (const string& name : team_names) {
        if (team_map.find(name) == team_map.end()) continue;
        Team& t = team_map[name];
        cout << "newline poly color " << get_random_color() << " linethickness 5 pfill -1 label : " << name << "\npts";
        for (int i = 0; i < num_axes; ++i) {
            double px, py;
            get_coords(i, (t.stats[i] / max_vals[i]), px, py);
            cout << " " << px << " " << py;
        }
        cout << endl;
    }

    // the labels representing metrics at the end of each axis
    for (int i = 0; i < num_axes; ++i) {
        double lx, ly;
        get_coords(i, 1.15, lx, ly);
        cout << "newstring hjc vjc font Helvetica fontsize 10 x " << lx << " y " << ly << " : " << labels[i] << endl;
    }
}


int main(int argc, char* argv[]) {
    vector<double> max_vals;
    map<string, Team> team_map = load_data("data/pl_teams.csv", max_vals);

    if (team_map.empty()) {
        cerr << "(* Error: No data loaded *)" << endl;
        return 1;
    }

    // if team name is specified in arg use it to create a file, if not use all files
    vector<string> requested_teams;
    if (argc > 1) {
        for (int i = 1; i < argc; ++i) requested_teams.push_back(argv[i]);
    } else {
        for (auto const& [name, data] : team_map) requested_teams.push_back(name);
    }

    render_jgraph(requested_teams, team_map, max_vals);

    return 0;
}