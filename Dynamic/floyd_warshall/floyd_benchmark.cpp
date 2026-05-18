#include <iostream>
#include <fstream>
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <climits>

using namespace std;
using namespace std::chrono;

// Global variables for configuration
const int V_MIN = 50;
const int V_MAX = 500;
const int INCREMENT = 25;
const int ITERATIONS = 5;
const double EDGE_PROBABILITY = 0.5;
const int MAX_WEIGHT = 100;
const int INF = INT_MAX;

// Floyd-Warshall Algorithm — computes all-pairs shortest paths
void floydWarshall(int** dist, int V) {
    for (int k = 0; k < V; k++) {
        for (int i = 0; i < V; i++) {
            for (int j = 0; j < V; j++) {
                if (dist[i][k] != INF && dist[k][j] != INF
                    && dist[i][k] + dist[k][j] < dist[i][j]) {
                    dist[i][j] = dist[i][k] + dist[k][j];
                }
            }
        }
    }
}

// Generate a random connected undirected weighted graph (adjacency matrix)
int** generateRandomGraph(int V) {
    int** graph = new int*[V];
    for (int i = 0; i < V; i++) {
        graph[i] = new int[V];
        for (int j = 0; j < V; j++) {
            if (i == j)
                graph[i][j] = 0;
            else
                graph[i][j] = INF;
        }
    }

    // Spanning tree for connectivity
    for (int i = 1; i < V; i++) {
        int j = rand() % i;
        int w = (rand() % MAX_WEIGHT) + 1;
        graph[i][j] = w;
        graph[j][i] = w;
    }

    // Random additional edges
    for (int i = 0; i < V; i++) {
        for (int j = i + 1; j < V; j++) {
            if (graph[i][j] == INF) {
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

// Copy a matrix (so original graph is preserved)
int** copyMatrix(int** src, int V) {
    int** copy = new int*[V];
    for (int i = 0; i < V; i++) {
        copy[i] = new int[V];
        for (int j = 0; j < V; j++)
            copy[i][j] = src[i][j];
    }
    return copy;
}

void freeGraph(int** graph, int V) {
    for (int i = 0; i < V; i++)
        delete[] graph[i];
    delete[] graph;
}

int main() {
    srand(static_cast<unsigned int>(time(0)));

    ofstream outFile("floyd_results.txt");

    if (!outFile) {
        cerr << "Error: Could not create output file!" << endl;
        return 1;
    }

    outFile << "Size,Time(microseconds)" << endl;

    cout << "==================================================" << endl;
    cout << "  FLOYD-WARSHALL ALGORITHM TIME COMPLEXITY ANALYSIS" << endl;
    cout << "==================================================" << endl;
    cout << "Vertices Min: " << V_MIN << endl;
    cout << "Vertices Max: " << V_MAX << endl;
    cout << "Increment:    " << INCREMENT << endl;
    cout << "Iterations:   " << ITERATIONS << " (random graphs, averaged)" << endl;
    cout << "Edge Prob:    " << EDGE_PROBABILITY << endl;
    cout << "Expected Complexity: O(V^3)" << endl;
    cout << "==================================================" << endl;
    cout << endl;

    for (int V = V_MIN; V <= V_MAX; V += INCREMENT) {

        double totalTime = 0;

        for (int iter = 0; iter < ITERATIONS; iter++) {
            int** graph = generateRandomGraph(V);

            // Copy the graph since Floyd-Warshall modifies the matrix in-place
            int** dist = copyMatrix(graph, V);

            auto start = high_resolution_clock::now();
            floydWarshall(dist, V);
            auto end = high_resolution_clock::now();

            totalTime += duration_cast<nanoseconds>(end - start).count();

            freeGraph(graph, V);
            freeGraph(dist, V);
        }

        double avgTimeUs = (totalTime / ITERATIONS) / 1000.0;

        outFile << V << "," << avgTimeUs << endl;

        cout << "Vertices: " << V << "\t\tAvg Time: " << avgTimeUs << " us" << endl;
    }

    outFile.close();

    cout << endl;
    cout << "==================================================" << endl;
    cout << "Results saved to: floyd_results.txt" << endl;
    cout << "==================================================" << endl;

    return 0;
}
