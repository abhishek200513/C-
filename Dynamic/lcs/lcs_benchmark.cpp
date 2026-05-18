#include <iostream>
#include <fstream>
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <algorithm>
#include <string>

using namespace std;
using namespace std::chrono;

// Global configuration
const int N_MIN = 50;
const int N_MAX = 1500;
const int INCREMENT = 50;
const int ITERATIONS = 5;

// LCS Algorithm — computes length only (for benchmarking)
int lcsDP(const string& X, const string& Y) {
    int m = X.length();
    int n = Y.length();

    // Use two rows to save space (only need previous row)
    int* prev = new int[n + 1]();
    int* curr = new int[n + 1]();

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (X[i - 1] == Y[j - 1])
                curr[j] = prev[j - 1] + 1;
            else
                curr[j] = max(prev[j], curr[j - 1]);
        }
        // Swap rows
        int* temp = prev;
        prev = curr;
        curr = temp;
        // Reset curr
        for (int j = 0; j <= n; j++) curr[j] = 0;
    }

    int result = prev[n];
    delete[] prev;
    delete[] curr;
    return result;
}

// Generate a random string of given length
string generateRandomString(int len) {
    string s(len, ' ');
    const char charset[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    for (int i = 0; i < len; i++) {
        s[i] = charset[rand() % 26];
    }
    return s;
}

int main() {
    srand(static_cast<unsigned int>(time(0)));

    ofstream outFile("lcs_results.txt");

    if (!outFile) {
        cerr << "Error: Could not create output file!" << endl;
        return 1;
    }

    outFile << "Size,Time(microseconds)" << endl;

    cout << "==================================================" << endl;
    cout << "    LCS ALGORITHM TIME COMPLEXITY ANALYSIS" << endl;
    cout << "==================================================" << endl;
    cout << "String Length Min: " << N_MIN << endl;
    cout << "String Length Max: " << N_MAX << endl;
    cout << "Increment:        " << INCREMENT << endl;
    cout << "Iterations:       " << ITERATIONS << " (random strings, averaged)" << endl;
    cout << "Expected Complexity: O(m*n) = O(n^2) for equal lengths" << endl;
    cout << "==================================================" << endl;
    cout << endl;

    for (int n = N_MIN; n <= N_MAX; n += INCREMENT) {

        double totalTime = 0;

        for (int iter = 0; iter < ITERATIONS; iter++) {
            string X = generateRandomString(n);
            string Y = generateRandomString(n);

            auto start = high_resolution_clock::now();
            lcsDP(X, Y);
            auto end = high_resolution_clock::now();

            totalTime += duration_cast<nanoseconds>(end - start).count();
        }

        double avgTimeUs = (totalTime / ITERATIONS) / 1000.0;

        outFile << n << "," << avgTimeUs << endl;

        cout << "Length: " << n << "\t\tAvg Time: " << avgTimeUs << " us" << endl;
    }

    outFile.close();

    cout << endl;
    cout << "==================================================" << endl;
    cout << "Results saved to: lcs_results.txt" << endl;
    cout << "==================================================" << endl;

    return 0;
}
