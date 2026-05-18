#include <iostream>
#include <iomanip>
#include <climits>
#include <string>
#include <vector>

using namespace std;

const int INF = INT_MAX;

// Print a distance matrix in table format
void printMatrix(int** matrix, int V) {
    // Header row: "v" followed by column indices
    cout << setw(6) << "v";
    for (int j = 0; j < V; j++)
        cout << setw(6) << j;
    cout << endl;

    // Data rows
    for (int i = 0; i < V; i++) {
        cout << setw(6) << i;
        for (int j = 0; j < V; j++) {
            if (matrix[i][j] == INF)
                cout << setw(6) << "INF";
            else
                cout << setw(6) << matrix[i][j];
        }
        cout << endl;
    }
}

// Floyd-Warshall Algorithm with detailed iteration output
void floydWarshall(int** graph, int V) {

    // Initialize distance matrix
    int** dist = new int*[V];
    for (int i = 0; i < V; i++) {
        dist[i] = new int[V];
        for (int j = 0; j < V; j++) {
            dist[i][j] = graph[i][j];
        }
    }

    // Print initial matrix
    cout << "Initial Matrix:" << endl;
    printMatrix(dist, V);
    cout << endl;

    // DP iterations — consider each vertex as intermediate
    for (int k = 0; k < V; k++) {
        cout << "Iteration k=" << k << " (Intermediate Vertex = " << k << ")" << endl;

        // Collect updates for this iteration
        struct Update {
            int i, j, oldVal, newVal, ik, kj;
        };
        vector<Update> updates;

        for (int i = 0; i < V; i++) {
            for (int j = 0; j < V; j++) {
                if (dist[i][k] != INF && dist[k][j] != INF
                    && dist[i][k] + dist[k][j] < dist[i][j]) {
                    Update u;
                    u.i = i;
                    u.j = j;
                    u.oldVal = dist[i][j];
                    u.newVal = dist[i][k] + dist[k][j];
                    u.ik = dist[i][k];
                    u.kj = dist[k][j];
                    updates.push_back(u);
                }
            }
        }

        if (updates.empty()) {
            cout << "Why change/no change: No update in this iteration." << endl;
        } else {
            for (size_t u = 0; u < updates.size(); u++) {
                string oldStr = (updates[u].oldVal == INF) ? "INF" : to_string(updates[u].oldVal);
                cout << "  dist[" << updates[u].i << "][" << updates[u].j
                     << "] changed from " << oldStr
                     << " to " << updates[u].newVal
                     << " because dist[" << updates[u].i << "][" << k
                     << "] + dist[" << k << "][" << updates[u].j
                     << "] = " << updates[u].ik << " + " << updates[u].kj
                     << " = " << updates[u].newVal
                     << " < " << oldStr << "." << endl;

                // Apply the update
                dist[updates[u].i][updates[u].j] = updates[u].newVal;
            }
        }

        cout << "Resulting Matrix (After k=" << k << "):" << endl;
        printMatrix(dist, V);
        cout << endl;
    }

    // Final output
    cout << "Output:" << endl;
    printMatrix(dist, V);
    cout << endl;

    // Cleanup
    for (int i = 0; i < V; i++) {
        delete[] dist[i];
    }
    delete[] dist;
}

// Run a single test case
void runTestCase(int caseNum, const string& label, int n, int rawMatrix[]) {

    cout << "============================================================" << endl;
    cout << "Test Case " << caseNum << " (" << label << ")" << endl;
    cout << "============================================================" << endl;

    // Print input
    cout << "Input:" << endl;
    cout << "n = " << n << endl;

    // Print raw input values in a single line
    for (int i = 0; i < n * n; i++) {
        cout << rawMatrix[i];
        if (i < n * n - 1) cout << " ";
    }
    cout << endl << endl;

    // Build adjacency matrix
    int** graph = new int*[n];
    for (int i = 0; i < n; i++) {
        graph[i] = new int[n];
        for (int j = 0; j < n; j++) {
            int val = rawMatrix[i * n + j];
            graph[i][j] = (val == -1) ? INF : val;
        }
    }

    // Run Floyd-Warshall
    floydWarshall(graph, n);

    // Cleanup
    for (int i = 0; i < n; i++) {
        delete[] graph[i];
    }
    delete[] graph;

    cout << endl;
}

int main() {

  //cout << "============================================================" << endl;
  //cout << "              Experiment 12" << endl;
    cout << "  All-Pairs Shortest Path (APSP) using" << endl;
    cout << "         Floyd-Warshall Algorithm" << endl;
  //cout << "============================================================" << endl;
    cout << endl;

    // ---- Test Case 1 (Normal Case) ----
    {
        int n = 4;
        int raw[] = {
            0,  5, -1, 10,
           -1,  0,  3, -1,
           -1, -1,  0,  1,
           -1, -1, -1,  0
        };
        runTestCase(1, "Normal Case", n, raw);
    }

    // ---- Test Case 2 (Small Input Case) ----
    {
        int n = 2;
        int raw[] = {
            0, 7,
           -1, 0
        };
        runTestCase(2, "Small Input Case", n, raw);
    }

    // ---- Test Case 3 (Edge Case: Single Vertex) ----
    {
        int n = 1;
        int raw[] = { 0 };
        runTestCase(3, "Edge Case: Single Vertex", n, raw);
    }

    // ---- Test Case 4 (Larger Input Case) ----
    {
        int n = 5;
        int raw[] = {
            0,  4,  2, -1, -1,
           -1,  0,  1,  5, -1,
           -1, -1,  0,  8, 10,
           -1, -1, -1,  0,  2,
            3, -1, -1, -1,  0
        };
        runTestCase(4, "Larger Input Case", n, raw);
    }

    // ---- Test Case 5 (Special/Tricky Case) ----
    {
        int n = 5;
        int raw[] = {
            0, 10,  3, -1, -1,
           -1,  0,  1,  2, -1,
           -1,  4,  0,  8,  2,
           -1, -1, -1,  0,  7,
           -1, -1, -1,  9,  0
        };
        runTestCase(5, "Special/Tricky Case", n, raw);
    }

    cout << "============================================================" << endl;
    cout << "Result:" << endl;
    cout << "All predefined test cases were executed with full" << endl;
    cout << "iteration-wise updates." << endl;
    cout << "============================================================" << endl;
    cout << endl;
    // cout << "Conclusion:" << endl;
    // cout << "The Floyd-Warshall algorithm successfully found the shortest" << endl;
    // cout << "paths between all pairs of points by checking if any vertex" << endl;
    // cout << "could serve as a better shortcut. By testing every possible" << endl;
    // cout << "middle step, the algorithm updated distances only when it" << endl;
    // cout << "found a shorter way to get from one point to another." << endl;

    return 0;
}
