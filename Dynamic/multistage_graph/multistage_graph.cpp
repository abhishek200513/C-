#include <iostream>
#include <iomanip>
#include <climits>

using namespace std;

const int INF = INT_MAX;

// Multistage Graph — Shortest Path using Dynamic Programming (Forward Approach)
void multistageGraphForward(int** graph, int V, int stages, int stageOf[]) {

    int* cost = new int[V];    // Minimum cost from vertex i to sink
    int* next = new int[V];    // Next vertex on the shortest path from i
    int sink = V - 1;

    // Initialize
    for (int i = 0; i < V; i++) {
        cost[i] = INF;
        next[i] = -1;
    }
    cost[sink] = 0;

    cout << "\n====================================================" << endl;
    cout << "   FORWARD APPROACH — COMPUTING COSTS (RIGHT TO LEFT)" << endl;
    cout << "====================================================" << endl;

    // Fill cost[] from right to left (sink to source)
    for (int i = V - 2; i >= 0; i--) {
        cout << "\n  Vertex " << i << " (Stage " << stageOf[i] << "):" << endl;

        for (int j = i + 1; j < V; j++) {
            if (graph[i][j] != INF && graph[i][j] != 0) {
                if (cost[j] != INF && graph[i][j] + cost[j] < cost[i]) {
                    cost[i] = graph[i][j] + cost[j];
                    next[i] = j;

                    cout << "       Edge " << i << " -> " << j
                         << " (weight " << graph[i][j]
                         << ") : cost = " << graph[i][j] << " + " << cost[j]
                         << " = " << cost[i] << "  <-- new minimum" << endl;
                } else if (graph[i][j] != 0) {
                    int pathCost = (cost[j] != INF) ? graph[i][j] + cost[j] : INF;
                    cout << "       Edge " << i << " -> " << j
                         << " (weight " << graph[i][j]
                         << ") : cost = ";
                    if (pathCost == INF)
                        cout << "INF  (skipped)" << endl;
                    else
                        cout << pathCost << "  (not minimum)" << endl;
                }
            }
        }

        if (next[i] != -1)
            cout << "       => cost[" << i << "] = " << cost[i]
                 << ", next[" << i << "] = " << next[i] << endl;
        else
            cout << "       => No outgoing edges found." << endl;
    }

    // Display cost table
    cout << "\n====================================================" << endl;
    cout << "              COST TABLE (Forward)                   " << endl;
    cout << "====================================================" << endl;
    cout << left << setw(12) << "  Vertex"
         << setw(10) << "Stage"
         << setw(15) << "Cost to Sink"
         << "Next Vertex" << endl;
    cout << "----------------------------------------------------" << endl;

    for (int i = 0; i < V; i++) {
        cout << "  " << left << setw(10) << i
             << setw(10) << stageOf[i];
        if (cost[i] == INF)
            cout << setw(15) << "INF";
        else
            cout << setw(15) << cost[i];
        if (next[i] == -1)
            cout << "-" << endl;
        else
            cout << next[i] << endl;
    }
    cout << "====================================================" << endl;

    // Display the shortest path
    cout << "\n====================================================" << endl;
    cout << "        SHORTEST PATH (Source to Sink)               " << endl;
    cout << "====================================================" << endl;

    if (cost[0] == INF) {
        cout << "  No path exists from source (0) to sink (" << sink << ")." << endl;
    } else {
        cout << "  Minimum Cost: " << cost[0] << endl;
        cout << "  Path: ";

        int current = 0;
        cout << current;
        while (current != sink) {
            current = next[current];
            cout << " -> " << current;
        }
        cout << endl;
    }
    cout << "====================================================" << endl;

    delete[] cost;
    delete[] next;
}

// Multistage Graph — Shortest Path using Dynamic Programming (Backward Approach)
void multistageGraphBackward(int** graph, int V, int stages, int stageOf[]) {

    int* cost = new int[V];    // Minimum cost from source to vertex i
    int* prev = new int[V];    // Previous vertex on the shortest path to i
    int sink = V - 1;

    // Initialize
    for (int i = 0; i < V; i++) {
        cost[i] = INF;
        prev[i] = -1;
    }
    cost[0] = 0;

    cout << "\n====================================================" << endl;
    cout << "  BACKWARD APPROACH — COMPUTING COSTS (LEFT TO RIGHT)" << endl;
    cout << "====================================================" << endl;

    // Fill cost[] from left to right (source to sink)
    for (int j = 1; j < V; j++) {
        cout << "\n  Vertex " << j << " (Stage " << stageOf[j] << "):" << endl;

        for (int i = 0; i < j; i++) {
            if (graph[i][j] != INF && graph[i][j] != 0) {
                if (cost[i] != INF && cost[i] + graph[i][j] < cost[j]) {
                    cost[j] = cost[i] + graph[i][j];
                    prev[j] = i;

                    cout << "       Edge " << i << " -> " << j
                         << " (weight " << graph[i][j]
                         << ") : cost = " << cost[i] << " + " << graph[i][j]
                         << " = " << cost[j] << "  <-- new minimum" << endl;
                } else if (graph[i][j] != 0) {
                    int pathCost = (cost[i] != INF) ? cost[i] + graph[i][j] : INF;
                    cout << "       Edge " << i << " -> " << j
                         << " (weight " << graph[i][j]
                         << ") : cost = ";
                    if (pathCost == INF)
                        cout << "INF  (skipped)" << endl;
                    else
                        cout << pathCost << "  (not minimum)" << endl;
                }
            }
        }

        if (prev[j] != -1)
            cout << "       => cost[" << j << "] = " << cost[j]
                 << ", prev[" << j << "] = " << prev[j] << endl;
        else
            cout << "       => No incoming edges found." << endl;
    }

    // Display cost table
    cout << "\n====================================================" << endl;
    cout << "             COST TABLE (Backward)                   " << endl;
    cout << "====================================================" << endl;
    cout << left << setw(12) << "  Vertex"
         << setw(10) << "Stage"
         << setw(18) << "Cost from Source"
         << "Prev Vertex" << endl;
    cout << "----------------------------------------------------" << endl;

    for (int i = 0; i < V; i++) {
        cout << "  " << left << setw(10) << i
             << setw(10) << stageOf[i];
        if (cost[i] == INF)
            cout << setw(18) << "INF";
        else
            cout << setw(18) << cost[i];
        if (prev[i] == -1)
            cout << "-" << endl;
        else
            cout << prev[i] << endl;
    }
    cout << "====================================================" << endl;

    // Display the shortest path (trace backward from sink)
    cout << "\n====================================================" << endl;
    cout << "        SHORTEST PATH (Source to Sink)               " << endl;
    cout << "====================================================" << endl;

    if (cost[sink] == INF) {
        cout << "  No path exists from source (0) to sink (" << sink << ")." << endl;
    } else {
        cout << "  Minimum Cost: " << cost[sink] << endl;

        // Trace path backward
        int* path = new int[V];
        int pathLen = 0;
        int current = sink;
        while (current != -1) {
            path[pathLen++] = current;
            current = prev[current];
        }

        cout << "  Path: ";
        for (int i = pathLen - 1; i >= 0; i--) {
            cout << path[i];
            if (i > 0) cout << " -> ";
        }
        cout << endl;

        delete[] path;
    }
    cout << "====================================================" << endl;

    delete[] cost;
    delete[] prev;
}

int main() {
    int V, stages;

    cout << "====================================================" << endl;
    cout << " MULTISTAGE GRAPH SHORTEST PATH (DYNAMIC PROGRAMMING)" << endl;
    cout << "====================================================" << endl;

    cout << "\nEnter the number of vertices: ";
    cin >> V;
    cout << "Enter the number of stages: ";
    cin >> stages;

    // Assign vertices to stages
    int* stageOf = new int[V];
    cout << "\nEnter the stage number for each vertex (1 to " << stages << "):" << endl;
    for (int i = 0; i < V; i++) {
        cout << "  Vertex " << i << " belongs to stage: ";
        cin >> stageOf[i];
    }

    // Dynamically allocate adjacency matrix
    int** graph = new int*[V];
    for (int i = 0; i < V; i++) {
        graph[i] = new int[V];
        for (int j = 0; j < V; j++)
            graph[i][j] = INF;
        graph[i][i] = 0;
    }

    int E;
    cout << "\nEnter the number of edges: ";
    cin >> E;

    cout << "\nEnter each edge (source  destination  weight):" << endl;
    cout << "(Edges go from earlier stages to later stages)" << endl;
    for (int i = 0; i < E; i++) {
        int u, v, w;
        cout << "  Edge " << i + 1 << ": ";
        cin >> u >> v >> w;
        graph[u][v] = w;
    }

    // Display the input graph
    cout << "\n====================================================" << endl;
    cout << "              INPUT ADJACENCY MATRIX                 " << endl;
    cout << "====================================================" << endl;
    cout << "     ";
    for (int i = 0; i < V; i++)
        cout << setw(6) << i;
    cout << endl;
    cout << "     ";
    for (int i = 0; i < V; i++)
        cout << "------";
    cout << endl;

    for (int i = 0; i < V; i++) {
        cout << setw(3) << i << " |";
        for (int j = 0; j < V; j++) {
            if (graph[i][j] == INF)
                cout << setw(6) << "INF";
            else
                cout << setw(6) << graph[i][j];
        }
        cout << "    (Stage " << stageOf[i] << ")" << endl;
    }

    cout << "\n  Stage Assignment:" << endl;
    for (int s = 1; s <= stages; s++) {
        cout << "    Stage " << s << ": ";
        bool first = true;
        for (int i = 0; i < V; i++) {
            if (stageOf[i] == s) {
                if (!first) cout << ", ";
                cout << i;
                first = false;
            }
        }
        cout << endl;
    }
    cout << "====================================================" << endl;

    // Run Forward Approach
    multistageGraphForward(graph, V, stages, stageOf);

    // Run Backward Approach
    multistageGraphBackward(graph, V, stages, stageOf);

    // Cleanup
    for (int i = 0; i < V; i++)
        delete[] graph[i];
    delete[] graph;
    delete[] stageOf;

    return 0;
}
