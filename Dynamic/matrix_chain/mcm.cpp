#include <iostream>
#include <iomanip>
#include <climits>
#include <string>
#include <vector>

using namespace std;

const int INF = INT_MAX;

// Print a square-style DP table (m or s)
void printTable(int** table, int n, const string& label, bool isParenTable = false) {
    cout << "\n  " << label << ":" << endl;
    cout << setw(8) << " ";
    for (int j = 1; j <= n; j++)
        cout << setw(8) << j;
    cout << endl;

    for (int i = 1; i <= n; i++) {
        cout << setw(6) << i << " |";
        for (int j = 1; j <= n; j++) {
            if (i > j)
                cout << setw(8) << "-";
            else if (i == j)
                cout << setw(8) << 0;
            else {
                if (table[i][j] == INF)
                    cout << setw(8) << "INF";
                else
                    cout << setw(8) << table[i][j];
            }
        }
        cout << endl;
    }
}

// Recursively build the optimal parenthesization string
string buildParenString(int** s, int i, int j) {
    if (i == j)
        return "A" + to_string(i);
    return "(" + buildParenString(s, i, s[i][j]) + " x " +
           buildParenString(s, s[i][j] + 1, j) + ")";
}

// Matrix Chain Multiplication — DP with detailed output
void matrixChainMultiplication(int p[], int n, int caseNum) {
    // n = number of matrices, dimensions are p[0..n]
    // Matrix Ai has dimensions p[i-1] x p[i]

    // Allocate DP tables
    int** m = new int*[n + 1];  // m[i][j] = min multiplications for Ai..Aj
    int** s = new int*[n + 1];  // s[i][j] = split point for optimal parenthesization

    for (int i = 0; i <= n; i++) {
        m[i] = new int[n + 1];
        s[i] = new int[n + 1];
        for (int j = 0; j <= n; j++) {
            m[i][j] = (i == j) ? 0 : INF;
            s[i][j] = 0;
        }
    }

    // Print dimensions
    cout << "\n  Matrix Dimensions:" << endl;
    for (int i = 1; i <= n; i++) {
        cout << "    A" << i << " : " << p[i - 1] << " x " << p[i] << endl;
    }

    // Fill DP table — chain length l from 2 to n
    for (int l = 2; l <= n; l++) {
        cout << "\n  --------------------------------------------------------" << endl;
        cout << "  Chain Length l = " << l << ":" << endl;
        cout << "  --------------------------------------------------------" << endl;

        for (int i = 1; i <= n - l + 1; i++) {
            int j = i + l - 1;

            cout << "    m[" << i << "][" << j << "]: Evaluating splits k = "
                 << i << " to " << j - 1 << endl;

            // Try all split points k
            for (int k = i; k < j; k++) {
                int cost = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j];

                cout << "      k=" << k
                     << " : m[" << i << "][" << k << "] + m[" << k + 1 << "][" << j
                     << "] + p[" << i - 1 << "]*p[" << k << "]*p[" << j << "]"
                     << " = " << m[i][k] << " + " << m[k + 1][j]
                     << " + " << p[i - 1] << "*" << p[k] << "*" << p[j]
                     << " = " << cost;

                if (cost < m[i][j]) {
                    m[i][j] = cost;
                    s[i][j] = k;
                    cout << "  <-- new minimum" << endl;
                } else {
                    cout << "  (not minimum)" << endl;
                }
            }

            cout << "      => m[" << i << "][" << j << "] = " << m[i][j]
                 << ", split at k = " << s[i][j] << endl;
        }
    }

    // Print final tables
    printTable(m, n, "Cost Table m[i][j]");
    printTable(s, n, "Split Table s[i][j]", true);

    // Output
    cout << "\n  ========================================================" << endl;
    cout << "  OUTPUT:" << endl;
    cout << "  ========================================================" << endl;
    cout << "  Minimum number of scalar multiplications: " << m[1][n] << endl;
    cout << "  Optimal Parenthesization: " << buildParenString(s, 1, n) << endl;
    cout << "  ========================================================" << endl;

    // Cleanup
    for (int i = 0; i <= n; i++) {
        delete[] m[i];
        delete[] s[i];
    }
    delete[] m;
    delete[] s;
}

// Run a single test case
void runTestCase(int caseNum, const string& label, int p[], int n) {
    cout << "\n============================================================" << endl;
    cout << "Test Case " << caseNum << " (" << label << ")" << endl;
    cout << "============================================================" << endl;

    // Print input
    cout << "Input:" << endl;
    cout << "  Number of matrices: " << n << endl;
    cout << "  Dimension array p[] = { ";
    for (int i = 0; i <= n; i++) {
        cout << p[i];
        if (i < n) cout << ", ";
    }
    cout << " }" << endl;

    matrixChainMultiplication(p, n, caseNum);
    cout << endl;
}

int main() {

    cout << "============================================================" << endl;
    cout << "              Experiment 14" << endl;
    cout << "      Matrix Chain Multiplication (MCM)" << endl;
    cout << "        using Dynamic Programming" << endl;
    cout << "============================================================" << endl;

    // ---- Test Case 1 (Normal Case — 4 Matrices) ----
    {
        int p[] = {10, 30, 5, 60};
        int n = 3;
        runTestCase(1, "Normal Case — 3 Matrices", p, n);
    }

    // ---- Test Case 2 (Standard Case — 4 Matrices) ----
    {
        int p[] = {40, 20, 30, 10, 30};
        int n = 4;
        runTestCase(2, "Standard Case — 4 Matrices", p, n);
    }

    // ---- Test Case 3 (Edge Case — 2 Matrices) ----
    {
        int p[] = {10, 20, 30};
        int n = 2;
        runTestCase(3, "Edge Case — 2 Matrices", p, n);
    }

    // ---- Test Case 4 (Larger Case — 6 Matrices) ----
    {
        int p[] = {30, 35, 15, 5, 10, 20, 25};
        int n = 6;
        runTestCase(4, "Larger Case — 6 Matrices", p, n);
    }

    // ---- Test Case 5 (Uniform Dimensions) ----
    {
        int p[] = {5, 5, 5, 5, 5};
        int n = 4;
        runTestCase(5, "Uniform Dimensions — 4 Matrices", p, n);
    }

    cout << "\n============================================================" << endl;
    cout << "Result:" << endl;
    cout << "All predefined test cases were executed with full" << endl;
    cout << "step-by-step DP table filling and optimal parenthesization." << endl;
    cout << "============================================================" << endl;
    cout << endl;
    cout << "Conclusion:" << endl;
    cout << "The Matrix Chain Multiplication algorithm successfully found" << endl;
    cout << "the optimal parenthesization to minimize scalar multiplications" << endl;
    cout << "for all test cases. By evaluating every possible split point" << endl;
    cout << "for increasing chain lengths, the DP approach guaranteed the" << endl;
    cout << "globally optimal solution in O(n^3) time." << endl;

    return 0;
}
