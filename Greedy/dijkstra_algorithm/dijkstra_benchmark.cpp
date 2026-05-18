#include <iostream>
#include <fstream>
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <climits>

using namespace std;
using namespace std::chrono;

// Global variables for configuration
const int V_MIN = 100;
const int V_MAX = 2000;
const int INCREMENT = 100;
const int ITERATIONS = 5;
const double EDGE_PROBABILITY = 0.5;
const int MAX_WEIGHT = 100;

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

// Dijkstra's Algorithm — returns nothing, just computes shortest paths
void dijkstra(int** graph, int V, int src) {
    int* dist = new int[V];
    bool* visited = new bool[V];

    for (int i = 0; i < V; i++) {
        dist[i] = INT_MAX;
        visited[i] = false;
    }

    dist[src] = 0;

    for (int count = 0; count < V; count++) {
        int u = minDistance(dist, visited, V);
        if (u == -1) break;
        visited[u] = true;

        for (int v = 0; v < V; v++) {
            if (!visited[v] && graph[u][v] && dist[u] != INT_MAX
                && dist[u] + graph[u][v] < dist[v]) {
                dist[v] = dist[u] + graph[u][v];
            }
        }
    }

    delete[] dist;
    delete[] visited;
}

// Generate a random connected undirected weighted graph
int** generateRandomGraph(int V) {
    int** graph = new int*[V];
    for (int i = 0; i < V; i++) {
        graph[i] = new int[V];
        for (int j = 0; j < V; j++)
            graph[i][j] = 0;
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
            if (graph[i][j] == 0) {
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

    ofstream outFile("dijkstra_results.txt");

    if (!outFile) {
        cerr << "Error: Could not create output file!" << endl;
        return 1;
    }

    outFile << "Size,Time(microseconds)" << endl;

    cout << "==================================================" << endl;
    cout << "   DIJKSTRA'S ALGORITHM TIME COMPLEXITY ANALYSIS   " << endl;
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
            int** graph = generateRandomGraph(V);

            auto start = high_resolution_clock::now();
            dijkstra(graph, V, 0);
            auto end = high_resolution_clock::now();

            totalTime += duration_cast<nanoseconds>(end - start).count();

            freeGraph(graph, V);
        }

        double avgTimeUs = (totalTime / ITERATIONS) / 1000.0;

        outFile << V << "," << avgTimeUs << endl;

        cout << "Vertices: " << V << "\t\tAvg Time: " << avgTimeUs << " us" << endl;
    }

    outFile.close();

    cout << endl;
    cout << "==================================================" << endl;
    cout << "Results saved to: dijkstra_results.txt" << endl;
    cout << "==================================================" << endl;

    return 0;
}
