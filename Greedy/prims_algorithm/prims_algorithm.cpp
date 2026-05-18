#include <iostream>
#include <iomanip>
#include <climits>

using namespace std;

// Function to find the vertex with the minimum key value
// that is not yet included in the MST
int minKey(int key[], bool inMST[], int V) {
    int min = INT_MAX, minIndex = -1;

    for (int v = 0; v < V; v++) {
        if (!inMST[v] && key[v] < min) {
            min = key[v];
            minIndex = v;
        }
    }
    return minIndex;
}

// Prim's Algorithm to find MST
void primMST(int** graph, int V) {

    int* parent = new int[V];   // Stores the MST structure
    int* key    = new int[V];   // Key values to pick minimum weight edge
    bool* inMST = new bool[V]; // Track vertices included in MST

    // Initialize all keys as infinite, no vertex in MST
    for (int i = 0; i < V; i++) {
        key[i] = INT_MAX;
        inMST[i] = false;
        parent[i] = -1;
    }

    // Start from vertex 0
    key[0] = 0;
    parent[0] = -1;  // First node is the root of MST

    cout << "\n====================================================" << endl;
    cout << "     PRIM'S ALGORITHM — STEP-BY-STEP EXECUTION      " << endl;
    cout << "====================================================" << endl;

    int totalCost = 0;

    for (int count = 0; count < V; count++) {
        // Pick the minimum key vertex not yet in MST
        int u = minKey(key, inMST, V);
        inMST[u] = true;

        cout << "\n  Step " << count + 1
             << ": Pick vertex " << u
             << " (key = " << (key[u] == INT_MAX ? 0 : key[u]) << ")" << endl;

        // Update key values of adjacent vertices
        for (int v = 0; v < V; v++) {
            // graph[u][v] != 0  -> edge exists
            // !inMST[v]        -> v is not yet in MST
            // graph[u][v] < key[v] -> new weight is smaller
            if (graph[u][v] && !inMST[v] && graph[u][v] < key[v]) {
                parent[v] = u;
                key[v] = graph[u][v];
                cout << "       Update: key[" << v << "] = " << key[v]
                     << "  (edge " << u << " - " << v << ")" << endl;
            }
        }
    }

    // ========== Display the MST ==========
    cout << "\n====================================================" << endl;
    cout << "           MINIMUM SPANNING TREE (MST)               " << endl;
    cout << "====================================================" << endl;
    cout << left << setw(10) << "  Edge"
         << setw(15) << "Weight" << endl;
    cout << "----------------------------------------------------" << endl;

    for (int i = 1; i < V; i++) {
        cout << "  " << left << setw(3) << parent[i]
             << " - " << setw(5) << i
             << setw(15) << graph[i][parent[i]] << endl;
        totalCost += graph[i][parent[i]];
    }

    cout << "----------------------------------------------------" << endl;
    cout << "  Total Cost of MST = " << totalCost << endl;
    cout << "====================================================" << endl;

    // Cleanup
    delete[] parent;
    delete[] key;
    delete[] inMST;
}

int main() {
    int V;

    cout << "====================================================" << endl;
    cout << "       PRIM'S ALGORITHM — MINIMUM SPANNING TREE     " << endl;
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
    cout << "====================================================" << endl;

    // Run Prim's Algorithm
    primMST(graph, V);

    // Cleanup
    for (int i = 0; i < V; i++) {
        delete[] graph[i];
    }
    delete[] graph;

    return 0;
}
