#include <iostream>
#include <fstream>
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <climits>

using namespace std;
using namespace std::chrono;

// Global variables for configuration
const int N_MIN = 5;
const int N_MAX = 200;
const int INCREMENT = 5;
const int ITERATIONS = 5;
const int MAX_DIM = 100;

// MCM Algorithm — computes minimum scalar multiplications
long long matrixChainDP(int p[], int n) {
    // Allocate DP table
    long long** m = new long long*[n + 1];
    for (int i = 0; i <= n; i++) {
        m[i] = new long long[n + 1];
        for (int j = 0; j <= n; j++)
            m[i][j] = 0;
    }

    // Fill table for chain lengths 2 to n
    for (int l = 2; l <= n; l++) {
        for (int i = 1; i <= n - l + 1; i++) {
            int j = i + l - 1;
            m[i][j] = LLONG_MAX;
            for (int k = i; k < j; k++) {
                long long cost = m[i][k] + m[k + 1][j]
                    + (long long)p[i - 1] * p[k] * p[j];
                if (cost < m[i][j])
                    m[i][j] = cost;
            }
        }
    }

    long long result = m[1][n];

    for (int i = 0; i <= n; i++)
        delete[] m[i];
    delete[] m;

    return result;
}

// Generate random dimension array
void generateRandomDimensions(int p[], int n) {
    for (int i = 0; i <= n; i++) {
        p[i] = (rand() % MAX_DIM) + 1;
    }
}

int main() {
    srand(static_cast<unsigned int>(time(0)));

    ofstream outFile("mcm_results.txt");

    if (!outFile) {
        cerr << "Error: Could not create output file!" << endl;
        return 1;
    }

    outFile << "Size,Time(microseconds)" << endl;

    cout << "==================================================" << endl;
    cout << "   MCM ALGORITHM TIME COMPLEXITY ANALYSIS" << endl;
    cout << "==================================================" << endl;
    cout << "Matrices Min: " << N_MIN << endl;
    cout << "Matrices Max: " << N_MAX << endl;
    cout << "Increment:    " << INCREMENT << endl;
    cout << "Iterations:   " << ITERATIONS << " (random dims, averaged)" << endl;
    cout << "Max Dimension: " << MAX_DIM << endl;
    cout << "Expected Complexity: O(n^3)" << endl;
    cout << "==================================================" << endl;
    cout << endl;

    for (int n = N_MIN; n <= N_MAX; n += INCREMENT) {

        double totalTime = 0;

        for (int iter = 0; iter < ITERATIONS; iter++) {
            int* p = new int[n + 1];
            generateRandomDimensions(p, n);

            auto start = high_resolution_clock::now();
            matrixChainDP(p, n);
            auto end = high_resolution_clock::now();

            totalTime += duration_cast<nanoseconds>(end - start).count();

            delete[] p;
        }

        double avgTimeUs = (totalTime / ITERATIONS) / 1000.0;

        outFile << n << "," << avgTimeUs << endl;

        cout << "Matrices: " << n << "\t\tAvg Time: " << avgTimeUs << " us" << endl;
    }

    outFile.close();

    cout << endl;
    cout << "==================================================" << endl;
    cout << "Results saved to: mcm_results.txt" << endl;
    cout << "==================================================" << endl;

    return 0;
}
