#include <iostream>
#include <fstream>
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <algorithm>
#include <set>
#include <utility>

using namespace std;
using namespace std::chrono;

// Global variables for configuration
const int V_MIN = 100;
const int V_MAX = 2000;
const int INCREMENT = 100;
const int ITERATIONS = 15;           // increased from 5 for smoother averaging
const double EDGE_PROBABILITY = 0.5;
const int MAX_WEIGHT = 100;

struct Edge {
    int src, dest, weight;
};

struct Subset {
    int parent;
    int rank;
};

bool compareEdges(Edge a, Edge b) {
    return a.weight < b.weight;
}

int find(Subset subsets[], int i) {
    if (subsets[i].parent != i)
        subsets[i].parent = find(subsets, subsets[i].parent);
    return subsets[i].parent;
}

void unionSets(Subset subsets[], int x, int y) {
    int rootX = find(subsets, x);
    int rootY = find(subsets, y);

    if (subsets[rootX].rank < subsets[rootY].rank)
        subsets[rootX].parent = rootY;
    else if (subsets[rootX].rank > subsets[rootY].rank)
        subsets[rootY].parent = rootX;
    else {
        subsets[rootY].parent = rootX;
        subsets[rootX].rank++;
    }
}

void kruskalMST(Edge edges[], int V, int E) {
    sort(edges, edges + E, compareEdges);

    Subset* subsets = new Subset[V];
    for (int v = 0; v < V; v++) {
        subsets[v].parent = v;
        subsets[v].rank = 0;
    }

    int mstEdgeCount = 0;
    for (int i = 0; i < E && mstEdgeCount < V - 1; i++) {
        int srcRoot = find(subsets, edges[i].src);
        int destRoot = find(subsets, edges[i].dest);

        if (srcRoot != destRoot) {
            mstEdgeCount++;
            unionSets(subsets, srcRoot, destRoot);
        }
    }

    delete[] subsets;
}

int main() {
    srand(static_cast<unsigned int>(time(0)));

    ofstream outFile("kruskal_results.txt");

    if (!outFile) {
        cerr << "Error: Could not create output file!" << endl;
        return 1;
    }

    outFile << "Size,Time(microseconds)" << endl;

    cout << "==================================================" << endl;
    cout << "   KRUSKAL'S ALGORITHM TIME COMPLEXITY ANALYSIS    " << endl;
    cout << "==================================================" << endl;
    cout << "Vertices Min: " << V_MIN << endl;
    cout << "Vertices Max: " << V_MAX << endl;
    cout << "Increment:    " << INCREMENT << endl;
    cout << "Iterations:   " << ITERATIONS << " (random graphs, averaged)" << endl;
    cout << "Edge Prob:    " << EDGE_PROBABILITY << endl;
    cout << "Expected Complexity: O(E log E)" << endl;
    cout << "==================================================" << endl;
    cout << endl;

    for (int V = V_MIN; V <= V_MAX; V += INCREMENT) {

        // Pre-generate all graphs BEFORE timing
        // Store edge arrays and counts for each iteration
        int** allSrc = new int*[ITERATIONS];
        int** allDest = new int*[ITERATIONS];
        int** allWeight = new int*[ITERATIONS];
        int* allE = new int[ITERATIONS];

        for (int iter = 0; iter < ITERATIONS; iter++) {
            int maxEdges = V * (V - 1) / 2;
            
            // Use a set for O(log n) duplicate checking instead of O(n) scan
            set<pair<int,int>> edgeSet;
            
            int* srcArr = new int[maxEdges];
            int* destArr = new int[maxEdges];
            int* weightArr = new int[maxEdges];
            int E = 0;

            // Create spanning tree for connectivity
            for (int i = 1; i < V; i++) {
                int j = rand() % i;
                int u = min(i, j);
                int v = max(i, j);
                edgeSet.insert({u, v});
                srcArr[E] = i;
                destArr[E] = j;
                weightArr[E] = (rand() % MAX_WEIGHT) + 1;
                E++;
            }

            // Add random edges (using set for fast duplicate check)
            for (int i = 0; i < V; i++) {
                for (int j = i + 1; j < V; j++) {
                    double r = (double)rand() / RAND_MAX;
                    if (r < EDGE_PROBABILITY) {
                        if (edgeSet.find({i, j}) == edgeSet.end()) {
                            edgeSet.insert({i, j});
                            srcArr[E] = i;
                            destArr[E] = j;
                            weightArr[E] = (rand() % MAX_WEIGHT) + 1;
                            E++;
                        }
                    }
                }
            }

            allSrc[iter] = srcArr;
            allDest[iter] = destArr;
            allWeight[iter] = weightArr;
            allE[iter] = E;
        }

        // Now time only the algorithm, not the graph generation
        double totalTime = 0;

        for (int iter = 0; iter < ITERATIONS; iter++) {
            int E = allE[iter];

            // Copy edges into Edge array (this is part of the measured work
            // since in practice you'd have the edges ready)
            Edge* edges = new Edge[E];
            for (int i = 0; i < E; i++) {
                edges[i].src = allSrc[iter][i];
                edges[i].dest = allDest[iter][i];
                edges[i].weight = allWeight[iter][i];
            }

            // Measure time for Kruskal's algorithm only
            auto start = high_resolution_clock::now();
            kruskalMST(edges, V, E);
            auto end = high_resolution_clock::now();

            totalTime += duration_cast<nanoseconds>(end - start).count();

            delete[] edges;
        }

        // Clean up pre-generated graphs
        for (int iter = 0; iter < ITERATIONS; iter++) {
            delete[] allSrc[iter];
            delete[] allDest[iter];
            delete[] allWeight[iter];
        }
        delete[] allSrc;
        delete[] allDest;
        delete[] allWeight;
        delete[] allE;

        double avgTimeUs = (totalTime / ITERATIONS) / 1000.0;

        outFile << V << "," << avgTimeUs << endl;

        cout << "Vertices: " << V << "\t\tAvg Time: " << avgTimeUs << " us" << endl;
    }

    outFile.close();

    cout << endl;
    cout << "==================================================" << endl;
    cout << "Results saved to: kruskal_results.txt" << endl;
    cout << "==================================================" << endl;

    return 0;
}
