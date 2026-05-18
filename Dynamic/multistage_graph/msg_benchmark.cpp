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
const int ITERATIONS = 10;
const int REPEATS = 50;       // repeat algorithm this many times per graph for stable timing
const int MAX_WEIGHT = 100;
const int INF = INT_MAX;

// Multistage Graph — Forward Approach (right to left DP)
void multistageForward(int** graph, int V) {
    int* cost = new int[V];
    int sink = V - 1;

    for (int i = 0; i < V; i++)
        cost[i] = INF;
    cost[sink] = 0;

    for (int i = V - 2; i >= 0; i--) {
        for (int j = i + 1; j < V; j++) {
            if (graph[i][j] != INF && graph[i][j] != 0) {
                if (cost[j] != INF && graph[i][j] + cost[j] < cost[i]) {
                    cost[i] = graph[i][j] + cost[j];
                }
            }
        }
    }

    delete[] cost;
}

// Generate a random multistage graph with dense inter-stage connectivity
int** generateMultistageGraph(int V, int numStages, int* stageOf) {
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

    // Assign vertices to stages
    stageOf[0] = 1;
    stageOf[V - 1] = numStages;

    int innerVertices = V - 2;
    int innerStages = numStages - 2;

    if (innerStages > 0 && innerVertices > 0) {
        int perStage = innerVertices / innerStages;
        int extra = innerVertices % innerStages;

        int idx = 1;
        for (int s = 2; s <= numStages - 1; s++) {
            int count = perStage + (s - 2 < extra ? 1 : 0);
            for (int c = 0; c < count && idx < V - 1; c++) {
                stageOf[idx++] = s;
            }
        }
    }

    // Add edges: every vertex connects to every vertex in the next stage
    // Also add skip edges for more density
    for (int i = 0; i < V; i++) {
        for (int j = i + 1; j < V; j++) {
            if (stageOf[j] == stageOf[i] + 1) {
                // Full connectivity to next stage
                graph[i][j] = (rand() % MAX_WEIGHT) + 1;
            } else if (stageOf[j] == stageOf[i] + 2) {
                // 30% chance for skip-one-stage edges
                if ((double)rand() / RAND_MAX < 0.3) {
                    graph[i][j] = (rand() % MAX_WEIGHT) + 1;
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

    ofstream outFile("msg_results.txt");

    if (!outFile) {
        cerr << "Error: Could not create output file!" << endl;
        return 1;
    }

    outFile << "Size,Time(microseconds)" << endl;

    cout << "==================================================" << endl;
    cout << "  MULTISTAGE GRAPH — TIME COMPLEXITY ANALYSIS      " << endl;
    cout << "==================================================" << endl;
    cout << "Vertices Min: " << V_MIN << endl;
    cout << "Vertices Max: " << V_MAX << endl;
    cout << "Increment:    " << INCREMENT << endl;
    cout << "Iterations:   " << ITERATIONS << " graphs x " << REPEATS << " repeats each" << endl;
    cout << "Expected Complexity: O(V^2) [adjacency matrix DP]" << endl;
    cout << "==================================================" << endl;
    cout << endl;

    for (int V = V_MIN; V <= V_MAX; V += INCREMENT) {

        int numStages = max(3, V / 20);

        double totalTime = 0;

        for (int iter = 0; iter < ITERATIONS; iter++) {
            int* stageOf = new int[V];
            int** graph = generateMultistageGraph(V, numStages, stageOf);

            // Run the algorithm REPEATS times on the same graph to accumulate time
            auto start = high_resolution_clock::now();
            for (int r = 0; r < REPEATS; r++) {
                multistageForward(graph, V);
            }
            auto end = high_resolution_clock::now();

            // Divide by REPEATS to get per-run time
            totalTime += (double)duration_cast<nanoseconds>(end - start).count() / REPEATS;

            freeGraph(graph, V);
            delete[] stageOf;
        }

        double avgTimeUs = (totalTime / ITERATIONS) / 1000.0;

        outFile << V << "," << avgTimeUs << endl;

        cout << "Vertices: " << V << " (Stages: " << numStages
             << ")\tAvg Time: " << avgTimeUs << " us" << endl;
    }

    outFile.close();

    cout << endl;
    cout << "==================================================" << endl;
    cout << "Results saved to: msg_results.txt" << endl;
    cout << "==================================================" << endl;

    return 0;
}
