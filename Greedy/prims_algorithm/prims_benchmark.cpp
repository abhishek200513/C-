#include <iostream>
#include <fstream>
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <climits>

using namespace std;
using namespace std::chrono;

// Global variables for configuration
const int V_MIN = 100;           // Minimum number of vertices
const int V_MAX = 2000;          // Maximum number of vertices
const int INCREMENT = 100;       // Step size
const int ITERATIONS = 5;        // Number of runs per size (averaged)
const double EDGE_PROBABILITY = 0.5;  // Probability of edge existing
const int MAX_WEIGHT = 100;      // Maximum edge weight

// Find the vertex with minimum key value not yet in MST
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

// Prim's Algorithm — returns total MST cost
int primMST(int** graph, int V) {
    int* key = new int[V];
    bool* inMST = new bool[V];

    for (int i = 0; i < V; i++) {
        key[i] = INT_MAX;
        inMST[i] = false;
    }

    key[0] = 0;

    int totalCost = 0;

    for (int count = 0; count < V; count++) {
        int u = minKey(key, inMST, V);
        if (u == -1) break;  // disconnected graph
        inMST[u] = true;

        for (int v = 0; v < V; v++) {
            if (graph[u][v] && !inMST[v] && graph[u][v] < key[v]) {
                key[v] = graph[u][v];
            }
        }
    }

    // Calculate total cost
    for (int i = 0; i < V; i++) {
        if (key[i] != INT_MAX)
            totalCost += key[i];
    }

    delete[] key;
    delete[] inMST;

    return totalCost;
}

// Generate a random connected undirected weighted graph
int** generateRandomGraph(int V) {
    int** graph = new int*[V];
    for (int i = 0; i < V; i++) {
        graph[i] = new int[V];
        for (int j = 0; j < V; j++)
            graph[i][j] = 0;
    }

    // First, create a spanning tree to ensure connectivity
    for (int i = 1; i < V; i++) {
        int j = rand() % i;  // connect to a random earlier vertex
        int w = (rand() % MAX_WEIGHT) + 1;
        graph[i][j] = w;
        graph[j][i] = w;
    }

    // Then add random edges with given probability
    for (int i = 0; i < V; i++) {
        for (int j = i + 1; j < V; j++) {
            if (graph[i][j] == 0) {  // no edge yet
                double r = (double)rand() / RAND_MAX;
                if (r < EDGE_PROBABILITY) {
                    int w = (rand() % MAX_WEIGHT) + 1;
                    graph[i][j] = w;
                    graph[j][i] = w;
                }
            }
        }
    }

    return graph;
}

void freeGraph(int** graph, int V) {
    for (int i = 0; i < V; i++)
        delete[] graph[i];
    delete[] graph;
}

int main() {
    srand(static_cast<unsigned int>(time(0)));

    ofstream outFile("prims_results.txt");

    if (!outFile) {
        cerr << "Error: Could not create output file!" << endl;
        return 1;
    }

    outFile << "Size,Time(microseconds)" << endl;

    cout << "==================================================" << endl;
    cout << "     PRIM'S ALGORITHM TIME COMPLEXITY ANALYSIS     " << endl;
    cout << "==================================================" << endl;
    cout << "Vertices Min: " << V_MIN << endl;
    cout << "Vertices Max: " << V_MAX << endl;
    cout << "Increment:    " << INCREMENT << endl;
    cout << "Iterations:   " << ITERATIONS << " (random graphs, averaged)" << endl;
    cout << "Edge Prob:    " << EDGE_PROBABILITY << endl;
    cout << "Expected Complexity: O(V^2) [adjacency matrix]" << endl;
    cout << "==================================================" << endl;
    cout << endl;

    for (int V = V_MIN; V <= V_MAX; V += INCREMENT) {

        double totalTime = 0;

        for (int iter = 0; iter < ITERATIONS; iter++) {
            // Generate a random connected graph
            int** graph = generateRandomGraph(V);

            // Measure time for Prim's algorithm
            auto start = high_resolution_clock::now();
            primMST(graph, V);
            auto end = high_resolution_clock::now();

            totalTime += duration_cast<nanoseconds>(end - start).count();

            freeGraph(graph, V);
        }

        // Calculate average time in microseconds
        double avgTimeUs = (totalTime / ITERATIONS) / 1000.0;

        outFile << V << "," << avgTimeUs << endl;

        cout << "Vertices: " << V << "\t\tAvg Time: " << avgTimeUs << " us" << endl;
    }

    outFile.close();

    cout << endl;
    cout << "==================================================" << endl;
    cout << "Results saved to: prims_results.txt" << endl;
    cout << "==================================================" << endl;

    return 0;
}
