// =============================================================================
// Experiment: Graph Coloring using Backtracking
// Subject   : Algorithm Design and Analysis (ADA)
// Language  : C++
// =============================================================================
//
// THEORY:
// -------
// Graph Coloring is the assignment of colors (labels) to vertices of a graph
// such that no two adjacent vertices share the same color.
//
// Key Definitions:
//   • Vertex Coloring : Assigning colors to vertices satisfying the constraint
//     that adjacent vertices (connected by an edge) have different colors.
//   • Chromatic Number (χ): The minimum number of colors required to color a
//     graph. For a graph G, χ(G) is the smallest m such that G is m-colorable.
//   • m-Coloring Problem: Given a graph G and m colors, determine if every
//     vertex can be colored using at most m colors without conflicts.
//
// Algorithm: Backtracking
// -----------------------
// 1. Attempt to assign color 1 to vertex 0.
// 2. For each subsequent vertex, try each color in [1..m].
// 3. Before assigning, check all adjacent vertices — if any neighbor already
//    holds the same color, skip (conflict).
// 4. If a valid color is found, assign it and recurse to the next vertex.
// 5. If no valid color can be assigned (all conflict), BACKTRACK:
//    reset the current vertex's color to 0 and return false.
// 6. If all vertices are successfully colored, print the solution.
//
// Time Complexity : O(m^V) in the worst case (V = vertices, m = colors)
// Space Complexity: O(V) for the color array + O(V) recursion stack
// =============================================================================

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>

using namespace std;

// ---------------------------------------------------------------------------
// Global log buffer (mirrors every printed line → output file)
// ---------------------------------------------------------------------------
vector<string> logLines;

void logMsg(const string& msg = "") {
    cout << msg << "\n";
    logLines.push_back(msg);
}

// Echo a user-supplied value into the log so the saved file is self-contained
void logInput(const string& label, const string& value) {
    string line = "  > " + value + "        ← " + label;
    cout << line << "\n";
    logLines.push_back(line);
}

// ---------------------------------------------------------------------------
// Helper: format a vector as [a, b, c]
// ---------------------------------------------------------------------------
string vecToStr(const vector<int>& v) {
    string s = "[";
    for (int i = 0; i < (int)v.size(); i++) {
        s += to_string(v[i]);
        if (i + 1 < (int)v.size()) s += ", ";
    }
    s += "]";
    return s;
}

// ---------------------------------------------------------------------------
// Helper: color name from number
// ---------------------------------------------------------------------------
string colorName(int c) {
    static const vector<string> NAMES = {
        "None", "Red", "Green", "Blue", "Yellow", "Orange",
        "Purple", "Cyan", "Magenta", "Brown", "Pink"
    };
    if (c >= 0 && c < (int)NAMES.size()) return NAMES[c];
    return "Color" + to_string(c);
}

// ---------------------------------------------------------------------------
// Globals for backtracking
// ---------------------------------------------------------------------------
int V_global, m_global;
vector<vector<int>> adj_global;
vector<vector<int>> allSolutions;

int            callDepth     = 0;   // indentation depth in trace
long long      callCount     = 0;   // total recursive calls made
long long      callIdCounter = 0;

// FIX: renamed findAll → stopAtFirst for unambiguous semantics.
//   stopAtFirst = false  →  enumerate ALL solutions
//   stopAtFirst = true   →  halt after the first solution
bool stopAtFirst = false;

string indent(int depth) {
    return string(depth * 2, ' ');
}

// ---------------------------------------------------------------------------
// isSafe: check if color c can be assigned to vertex v
// ---------------------------------------------------------------------------
bool isSafe(const vector<int>& colors, int vertex, int c) {
    for (int nbr : adj_global[vertex]) {
        if (colors[nbr] == c) return false;
    }
    return true;
}

// ---------------------------------------------------------------------------
// Core Backtracking
// ---------------------------------------------------------------------------
bool graphColor(vector<int>& colors, int vertex) {
    callCount++;
    long long myCall = ++callIdCounter;
    string pad = indent(callDepth);

    logMsg("  " + pad + "CALL #" + to_string(myCall) +
           "  graphColor(vertex=" + to_string(vertex) +
           ", colors=" + vecToStr(colors) + ")");
    logMsg();

    if (vertex == V_global) {
        // All vertices colored — record solution
        allSolutions.push_back(colors);
        logMsg("  " + pad + "=> SOLUTION FOUND " + vecToStr(colors));
        logMsg("  " + pad + "RETURN #" + to_string(myCall));
        logMsg();
        // FIX: return true (stop) when stopAtFirst is set, otherwise keep going
        return stopAtFirst;
    }

    for (int c = 1; c <= m_global; c++) {
        ostringstream oss;
        oss << "  " << pad
            << "TRY    v" << vertex
            << " <- " << colorName(c) << " (c=" << c << ")";

        if (isSafe(colors, vertex, c)) {
            colors[vertex] = c;
            logMsg(oss.str() + "   [SAFE]");
            logMsg("  " + pad + "ASSIGN v" + to_string(vertex) +
                   " = " + colorName(c) + "   colors=" + vecToStr(colors));

            callDepth++;
            bool done = graphColor(colors, vertex + 1);
            callDepth--;

            if (done) return true;  // propagate early-stop upward

            // Backtrack
            colors[vertex] = 0;
            logMsg("  " + pad + "BACKTRACK v" + to_string(vertex) +
                   " (remove " + colorName(c) + ")   colors=" + vecToStr(colors));
            logMsg();
        } else {
            logMsg(oss.str() + "   [CONFLICT]");
        }
    }

    logMsg("  " + pad + "RETURN #" + to_string(myCall));
    logMsg();
    return false;  // no color worked for this vertex
}

// ---------------------------------------------------------------------------
// Run one test case
// ---------------------------------------------------------------------------
void runExperiment(int testNum,
                   int V, int m, bool saf,
                   const vector<vector<int>>& adjMatrix,
                   const string& graphDesc) {
    // Reset all globals for this run
    allSolutions.clear();
    callCount     = 0;
    callDepth     = 0;
    callIdCounter = 0;
    V_global      = V;
    m_global      = m;
    stopAtFirst   = saf;

    // Build adjacency list from matrix
    adj_global.assign(V, {});
    for (int i = 0; i < V; i++)
        for (int j = 0; j < V; j++)
            if (adjMatrix[i][j]) adj_global[i].push_back(j);

    string sep(72, '=');
    logMsg();
    logMsg(sep);
    logMsg("  TEST CASE " + to_string(testNum) + " : " + graphDesc);
    logMsg(sep);
    logMsg("  Vertices       : " + to_string(V));
    logMsg("  Colors (m)     : " + to_string(m));
    logMsg("  Stop at first  : " + string(saf ? "Yes" : "No (find all)"));
    logMsg();

    // Print adjacency matrix
    logMsg("  Adjacency Matrix:");
    // Build column header
    string header = "       ";
    for (int i = 0; i < V; i++) header += "  v" + to_string(i);
    logMsg(header);

    for (int i = 0; i < V; i++) {
        ostringstream row;
        row << "    v" << i << "  [";
        for (int j = 0; j < V; j++) {
            row << " " << adjMatrix[i][j];
            if (j < V - 1) row << ",";
        }
        row << " ]";
        logMsg(row.str());
    }
    logMsg();

    // Print adjacency list
    logMsg("  Adjacency List:");
    for (int i = 0; i < V; i++) {
        string s = "    v" + to_string(i) + " -> { ";
        for (int ni : adj_global[i]) s += "v" + to_string(ni) + " ";
        s += "}";
        logMsg(s);
    }
    logMsg();
    logMsg(sep);
    logMsg("  Backtracking Trace:");
    logMsg();

    vector<int> colors(V, 0);
    graphColor(colors, 0);

    logMsg();
    logMsg(sep);
    logMsg("  Total recursive calls : " + to_string(callCount));
    logMsg("  Solutions found       : " + to_string(allSolutions.size()));
    logMsg();

    if (allSolutions.empty()) {
        logMsg("  [FAIL]  Graph is NOT " + to_string(m) + "-colorable.");
    } else {
        logMsg("  [OK]    Graph IS " + to_string(m) + "-colorable.");
        logMsg();
        for (int s = 0; s < (int)allSolutions.size(); s++) {
            logMsg("  Solution " + to_string(s + 1) +
                   "  ->  Color Assignment:");
            for (int v = 0; v < V; v++) {
                logMsg("      Vertex " + to_string(v) +
                       "  ->  " + colorName(allSolutions[s][v]) +
                       "  (color " + to_string(allSolutions[s][v]) + ")");
            }
            logMsg();
        }
    }
    logMsg(sep);
    logMsg();
}

// ===========================================================================
// MAIN
// ===========================================================================
int main() {
    string sep(72, '=');
    string dash(72, '-');

    logMsg(sep);
    logMsg("  EXPERIMENT: GRAPH COLORING USING BACKTRACKING");
    logMsg("  Subject     : Algorithm Design and Analysis (ADA)");
    logMsg("  Language    : C++");
    logMsg(sep);
    logMsg();
    logMsg("  INPUT");
    logMsg("  Enter graph details below.");
    logMsg(dash);

    // ---- Number of vertices ----
    int V;
    logMsg("  Number of vertices (V):");
    cout << "  > ";
    if (!(cin >> V) || V <= 0) {
        cerr << "[ERROR] Invalid number of vertices.\n";
        return 1;
    }
    logInput("V", to_string(V));

    // ---- Number of colors ----
    int m;
    logMsg("  Number of colors (m):");
    cout << "  > ";
    if (!(cin >> m) || m <= 0) {
        cerr << "[ERROR] Invalid color count.\n";
        return 1;
    }
    logInput("m", to_string(m));

    // ---- Find all / stop at first ----
    // FIX: prompt wording now matches the renamed variable (stopAtFirst)
    logMsg("  Stop at first solution? (1 = Yes, 0 = Find all):");
    cout << "  > ";
    int safInput = 0;
    if (!(cin >> safInput) || (safInput != 0 && safInput != 1)) {
        cerr << "[ERROR] Enter 0 or 1.\n";
        return 1;
    }
    bool saf = (safInput == 1);
    logInput("stop-at-first", to_string(safInput));

    // ---- Adjacency matrix ----
    logMsg("  Adjacency matrix (" + to_string(V) + " x " + to_string(V) + "):");
    logMsg("  Use 0/1 entries, row by row.");
    logMsg();

    vector<vector<int>> A(V, vector<int>(V, 0));
    for (int i = 0; i < V; i++) {
        cout << "  Row " << i << " > ";
        ostringstream rowEcho;
        for (int j = 0; j < V; j++) {
            if (!(cin >> A[i][j]) || (A[i][j] != 0 && A[i][j] != 1)) {
                cerr << "[ERROR] Invalid entry at (" << i << ", " << j
                     << "). Use 0 or 1.\n";
                return 1;
            }
            rowEcho << A[i][j];
            if (j < V - 1) rowEcho << " ";
        }
        // Echo each row into log for a self-contained output file
        logInput("row " + to_string(i), rowEcho.str());
    }

    // Validate: no self-loops, must be symmetric (undirected)
    for (int i = 0; i < V; i++) {
        if (A[i][i] != 0) {
            cerr << "[ERROR] Diagonal must be 0 (no self-loops) at ("
                 << i << ", " << i << ").\n";
            return 1;
        }
        for (int j = i + 1; j < V; j++) {
            if (A[i][j] != A[j][i]) {
                cerr << "[ERROR] Matrix must be symmetric (undirected graph): "
                     << "A[" << i << "][" << j << "]=" << A[i][j]
                     << " vs A[" << j << "][" << i << "]=" << A[j][i] << "\n";
                return 1;
            }
        }
    }

    runExperiment(1, V, m, saf, A, "User Input Graph");

    logMsg(sep);
    logMsg("  END OF EXPERIMENT");
    logMsg(sep);

    // -------------------------------------------------------------------------
    // FIX: use a portable output path instead of a hardcoded absolute path.
    //      Writes "graph_coloring_output.txt" in the current working directory.
    //      If a custom directory is needed, set the OUTPUT_DIR environment
    //      variable before running, e.g.:
    //        OUTPUT_DIR=/tmp/ada ./graph_coloring
    // -------------------------------------------------------------------------
    string outputPath;
    const char* envDir = getenv("OUTPUT_DIR");
    if (envDir && envDir[0] != '\0') {
        string dir(envDir);
        if (dir.back() != '/') dir += '/';
        outputPath = dir + "output.txt";
    } else {
        outputPath = "graph_coloring_output.txt";   // current directory
    }

    ofstream outFile(outputPath);
    if (!outFile) {
        cerr << "[ERROR] Cannot open output file: " << outputPath << "\n";
        cerr << "        Set OUTPUT_DIR to a writable directory and retry.\n";
        return 1;
    }
    for (const auto& line : logLines) outFile << line << "\n";
    cout << "[INFO] Output saved to: " << outputPath << "\n";

    return 0;
}