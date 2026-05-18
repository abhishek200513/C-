#include <iostream>
#include <iomanip>
#include <algorithm>

using namespace std;

// Structure to represent an edge
struct Edge {
    int src, dest, weight;
};

// Structure to represent a subset for Union-Find
struct Subset {
    int parent;
    int rank;
};

// Comparator to sort edges by weight
bool compareEdges(Edge a, Edge b) {
    return a.weight < b.weight;
}

// Find the root of the set containing element i (with path compression)
int find(Subset subsets[], int i) {
    if (subsets[i].parent != i)
        subsets[i].parent = find(subsets, subsets[i].parent);
    return subsets[i].parent;
}

// Union of two sets (by rank)
void unionSets(Subset subsets[], int x, int y) {
    int rootX = find(subsets, x);
    int rootY = find(subsets, y);

    if (subsets[rootX].rank < subsets[rootY].rank) {
        subsets[rootX].parent = rootY;
    } else if (subsets[rootX].rank > subsets[rootY].rank) {
        subsets[rootY].parent = rootX;
    } else {
        subsets[rootY].parent = rootX;
        subsets[rootX].rank++;
    }
}

// Kruskal's Algorithm to find MST
void kruskalMST(Edge edges[], int V, int E) {

    // Step 1: Sort all edges by weight
    sort(edges, edges + E, compareEdges);

    cout << "\n====================================================" << endl;
    cout << "     SORTED EDGES (by weight)                        " << endl;
    cout << "====================================================" << endl;
    cout << left << setw(8) << "  #"
         << setw(8) << "Src"
         << setw(8) << "Dest"
         << setw(10) << "Weight" << endl;
    cout << "----------------------------------------------------" << endl;
    for (int i = 0; i < E; i++) {
        cout << "  " << left << setw(6) << i + 1
             << setw(8) << edges[i].src
             << setw(8) << edges[i].dest
             << setw(10) << edges[i].weight << endl;
    }
    cout << "====================================================" << endl;

    // Step 2: Create subsets for Union-Find
    Subset* subsets = new Subset[V];
    for (int v = 0; v < V; v++) {
        subsets[v].parent = v;
        subsets[v].rank = 0;
    }

    // Step 3: Pick edges one by one
    Edge* result = new Edge[V - 1];  // MST will have V-1 edges
    int mstEdgeCount = 0;
    int totalCost = 0;

    cout << "\n====================================================" << endl;
    cout << "     KRUSKAL'S ALGORITHM — STEP-BY-STEP              " << endl;
    cout << "====================================================" << endl;

    int step = 1;
    for (int i = 0; i < E && mstEdgeCount < V - 1; i++) {
        int srcRoot = find(subsets, edges[i].src);
        int destRoot = find(subsets, edges[i].dest);

        if (srcRoot != destRoot) {
            // No cycle — include this edge
            result[mstEdgeCount++] = edges[i];
            unionSets(subsets, srcRoot, destRoot);
            totalCost += edges[i].weight;

            cout << "  Step " << step++ << ": Add edge "
                 << edges[i].src << " - " << edges[i].dest
                 << " (weight " << edges[i].weight << ") ✓ Accepted" << endl;
        } else {
            cout << "  Step " << step++ << ": Edge "
                 << edges[i].src << " - " << edges[i].dest
                 << " (weight " << edges[i].weight << ") ✗ Rejected (cycle)" << endl;
        }
    }

    // Display the MST
    cout << "\n====================================================" << endl;
    cout << "           MINIMUM SPANNING TREE (MST)               " << endl;
    cout << "====================================================" << endl;
    cout << left << setw(10) << "  Edge"
         << setw(15) << "Weight" << endl;
    cout << "----------------------------------------------------" << endl;

    for (int i = 0; i < mstEdgeCount; i++) {
        cout << "  " << left << setw(3) << result[i].src
             << " - " << setw(5) << result[i].dest
             << setw(15) << result[i].weight << endl;
    }

    cout << "----------------------------------------------------" << endl;
    cout << "  Total Cost of MST = " << totalCost << endl;
    cout << "====================================================" << endl;

    delete[] subsets;
    delete[] result;
}

int main() {
    int V, E;

    cout << "====================================================" << endl;
    cout << "     KRUSKAL'S ALGORITHM — MINIMUM SPANNING TREE     " << endl;
    cout << "====================================================" << endl;

    cout << "\nEnter the number of vertices: ";
    cin >> V;
    cout << "Enter the number of edges: ";
    cin >> E;

    Edge* edges = new Edge[E];

    cout << "\nEnter each edge (source  destination  weight):" << endl;
    for (int i = 0; i < E; i++) {
        cout << "  Edge " << i + 1 << ": ";
        cin >> edges[i].src >> edges[i].dest >> edges[i].weight;
    }

    // Display the input edges
    cout << "\n====================================================" << endl;
    cout << "               INPUT EDGES                           " << endl;
    cout << "====================================================" << endl;
    cout << left << setw(8) << "  #"
         << setw(8) << "Src"
         << setw(8) << "Dest"
         << setw(10) << "Weight" << endl;
    cout << "----------------------------------------------------" << endl;
    for (int i = 0; i < E; i++) {
        cout << "  " << left << setw(6) << i + 1
             << setw(8) << edges[i].src
             << setw(8) << edges[i].dest
             << setw(10) << edges[i].weight << endl;
    }
    cout << "  Vertices: " << V << ", Edges: " << E << endl;
    cout << "====================================================" << endl;

    // Run Kruskal's Algorithm
    kruskalMST(edges, V, E);

    delete[] edges;

    return 0;
}
