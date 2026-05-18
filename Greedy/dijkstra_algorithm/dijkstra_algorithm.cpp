#include <iostream>
#include <iomanip>
#include <climits>

using namespace std;

// Find the vertex with minimum distance not yet processed
int minDistance(int dist[], bool visited[], int V) {
    int min = INT_MAX, minIndex = -1;

    for (int v = 0; v < V; v++) {
        if (!visited[v] && dist[v] < min) {
            min = dist[v];
            minIndex = v;
        }
    }
    return minIndex;
}

// Print the shortest path from source to a vertex
void printPath(int parent[], int v) {
    if (parent[v] == -1) {
        cout << v;
        return;
    }
    printPath(parent, parent[v]);
    cout << " -> " << v;
}

// Dijkstra's Algorithm for single-source shortest path
void dijkstra(int** graph, int V, int src) {

    int* dist    = new int[V];    // Shortest distance from source
    bool* visited = new bool[V]; // Track processed vertices
    int* parent  = new int[V];   // Store shortest path tree

    // Initialize
    for (int i = 0; i < V; i++) {
        dist[i] = INT_MAX;
        visited[i] = false;
        parent[i] = -1;
    }

    dist[src] = 0;

    cout << "\n====================================================" << endl;
    cout << "     DIJKSTRA'S ALGORITHM — STEP-BY-STEP EXECUTION   " << endl;
    cout << "====================================================" << endl;

    for (int count = 0; count < V; count++) {
        int u = minDistance(dist, visited, V);
        if (u == -1) break;  // remaining vertices unreachable

        visited[u] = true;

        cout << "\n  Step " << count + 1
             << ": Process vertex " << u
             << " (dist = " << dist[u] << ")" << endl;

        // Update distances of adjacent vertices
        for (int v = 0; v < V; v++) {
            if (!visited[v] && graph[u][v] && dist[u] != INT_MAX
                && dist[u] + graph[u][v] < dist[v]) {

                dist[v] = dist[u] + graph[u][v];
                parent[v] = u;

                cout << "       Update: dist[" << v << "] = " << dist[v]
                     << "  (via " << u << " -> " << v
                     << ", edge weight = " << graph[u][v] << ")" << endl;
            }
        }
    }

    // ========== Display Results ==========
    cout << "\n====================================================" << endl;
    cout << "        SHORTEST PATHS FROM SOURCE " << src << "                " << endl;
    cout << "====================================================" << endl;
    cout << left << setw(10) << "  Vertex"
         << setw(12) << "Distance"
         << "Path" << endl;
    cout << "----------------------------------------------------" << endl;

    for (int i = 0; i < V; i++) {
        cout << "  " << left << setw(8) << i;
        if (dist[i] == INT_MAX) {
            cout << setw(12) << "INF" << "No path" << endl;
        } else {
            cout << setw(12) << dist[i];
            printPath(parent, i);
            cout << endl;
        }
    }
    cout << "====================================================" << endl;

    delete[] dist;
    delete[] visited;
    delete[] parent;
}

int main() {
    int V, src;

    cout << "====================================================" << endl;
    cout << "    DIJKSTRA'S ALGORITHM — SINGLE SOURCE SHORTEST PATH" << endl;
    cout << "====================================================" << endl;

    cout << "\nEnter the number of vertices: ";
    cin >> V;

    // Dynamically allocate adjacency matrix
    int** graph = new int*[V];
    for (int i = 0; i < V; i++) {
        graph[i] = new int[V];
    }

    cout << "\nEnter the adjacency matrix (" << V << " x " << V << "):" << endl;
    cout << "(Enter 0 if no edge exists between two vertices)\n" << endl;

    for (int i = 0; i < V; i++) {
        for (int j = 0; j < V; j++) {
            cin >> graph[i][j];
        }
    }

    cout << "\nEnter the source vertex (0 to " << V - 1 << "): ";
    cin >> src;

    // Display the input graph
    cout << "\n====================================================" << endl;
    cout << "              ADJACENCY MATRIX                       " << endl;
    cout << "====================================================" << endl;
    cout << "     ";
    for (int i = 0; i < V; i++)
        cout << setw(5) << i;
    cout << endl;
    cout << "     ";
    for (int i = 0; i < V; i++)
        cout << "-----";
    cout << endl;

    for (int i = 0; i < V; i++) {
        cout << setw(3) << i << " |";
        for (int j = 0; j < V; j++) {
            cout << setw(5) << graph[i][j];
        }
        cout << endl;
    }
    cout << "  Source vertex: " << src << endl;
    cout << "====================================================" << endl;

    // Run Dijkstra's Algorithm
    dijkstra(graph, V, src);

    // Cleanup
    for (int i = 0; i < V; i++) {
        delete[] graph[i];
    }
    delete[] graph;

    return 0;
}
