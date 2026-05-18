#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

// LCS using Dynamic Programming with detailed output
void lcs(const string& X, const string& Y, int caseNum) {
    int m = X.length();
    int n = Y.length();

    // Allocate DP table (m+1) x (n+1)
    int** dp = new int*[m + 1];
    for (int i = 0; i <= m; i++) {
        dp[i] = new int[n + 1];
        for (int j = 0; j <= n; j++)
            dp[i][j] = 0;
    }

    // Print input strings
    cout << "\n  String X: \"" << X << "\"  (length = " << m << ")" << endl;
    cout << "  String Y: \"" << Y << "\"  (length = " << n << ")" << endl;

    // Base case
    cout << "\n  Base Case: dp[i][0] = 0, dp[0][j] = 0 for all i, j." << endl;

    // Fill DP table
    cout << "\n  --------------------------------------------------------" << endl;
    cout << "  FILLING DP TABLE:" << endl;
    cout << "  --------------------------------------------------------" << endl;

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (X[i - 1] == Y[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
                cout << "  dp[" << i << "][" << j << "]: X[" << i
                     << "]=" << X[i - 1] << " == Y[" << j << "]=" << Y[j - 1]
                     << "  =>  dp[" << i - 1 << "][" << j - 1 << "] + 1 = "
                     << dp[i - 1][j - 1] << " + 1 = " << dp[i][j]
                     << "  <-- MATCH" << endl;
            } else {
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
                cout << "  dp[" << i << "][" << j << "]: X[" << i
                     << "]=" << X[i - 1] << " != Y[" << j << "]=" << Y[j - 1]
                     << "  =>  max(dp[" << i - 1 << "][" << j << "], dp["
                     << i << "][" << j - 1 << "]) = max(" << dp[i - 1][j]
                     << ", " << dp[i][j - 1] << ") = " << dp[i][j] << endl;
            }
        }
        cout << endl;
    }

    // Print DP table
    cout << "  DP Table:" << endl;
    cout << setw(8) << " ";
    cout << setw(6) << "0";
    for (int j = 1; j <= n; j++)
        cout << setw(6) << Y[j - 1];
    cout << endl;

    for (int i = 0; i <= m; i++) {
        if (i == 0)
            cout << setw(6) << "0" << " |";
        else
            cout << setw(5) << X[i - 1] << " " << i << "|";

        for (int j = 0; j <= n; j++)
            cout << setw(6) << dp[i][j];
        cout << endl;
    }

    // Backtrack to find the LCS string
    cout << "\n  --------------------------------------------------------" << endl;
    cout << "  BACKTRACKING TO FIND LCS:" << endl;
    cout << "  --------------------------------------------------------" << endl;

    string lcsStr = "";
    int i = m, j = n;

    while (i > 0 && j > 0) {
        if (X[i - 1] == Y[j - 1]) {
            cout << "  (" << i << "," << j << "): X[" << i << "]=" << X[i - 1]
                 << " == Y[" << j << "]=" << Y[j - 1]
                 << "  =>  Include '" << X[i - 1] << "', move diagonal" << endl;
            lcsStr = X[i - 1] + lcsStr;
            i--;
            j--;
        } else if (dp[i - 1][j] > dp[i][j - 1]) {
            cout << "  (" << i << "," << j << "): dp[" << i - 1 << "][" << j
                 << "]=" << dp[i - 1][j] << " > dp[" << i << "][" << j - 1
                 << "]=" << dp[i][j - 1] << "  =>  Move up" << endl;
            i--;
        } else {
            cout << "  (" << i << "," << j << "): dp[" << i - 1 << "][" << j
                 << "]=" << dp[i - 1][j] << " <= dp[" << i << "][" << j - 1
                 << "]=" << dp[i][j - 1] << "  =>  Move left" << endl;
            j--;
        }
    }

    // Output
    cout << "\n  ========================================================" << endl;
    cout << "  OUTPUT:" << endl;
    cout << "  ========================================================" << endl;
    cout << "  Length of LCS : " << dp[m][n] << endl;
    cout << "  LCS String    : \"" << lcsStr << "\"" << endl;
    cout << "  ========================================================" << endl;

    // Cleanup
    for (int i = 0; i <= m; i++)
        delete[] dp[i];
    delete[] dp;
}

// Run a single test case
void runTestCase(int caseNum, const string& label,
                 const string& X, const string& Y) {
    cout << "\n============================================================" << endl;
    cout << "Test Case " << caseNum << " (" << label << ")" << endl;
    cout << "============================================================" << endl;

    cout << "Input:" << endl;
    cout << "  X = \"" << X << "\"" << endl;
    cout << "  Y = \"" << Y << "\"" << endl;

    lcs(X, Y, caseNum);
    cout << endl;
}

int main() {

    cout << "============================================================" << endl;
    cout << "              Experiment 15" << endl;
    cout << "    Longest Common Subsequence (LCS)" << endl;
    cout << "        using Dynamic Programming" << endl;
    cout << "============================================================" << endl;

    // ---- Test Case 1 (Normal Case) ----
    runTestCase(1, "Normal Case", "ABCBDAB", "BDCAB");

    // ---- Test Case 2 (No Common Subsequence) ----
    runTestCase(2, "No Common Subsequence", "ABC", "XYZ");

    // ---- Test Case 3 (Identical Strings) ----
    runTestCase(3, "Identical Strings", "AGGTAB", "AGGTAB");

    // ---- Test Case 4 (One String is Subsequence) ----
    runTestCase(4, "One String is Subsequence", "ABCDEF", "ACE");

    // ---- Test Case 5 (Larger Case) ----
    runTestCase(5, "Larger Case", "STONE", "LONGEST");

    cout << "\n============================================================" << endl;
    cout << "Result:" << endl;
    cout << "All predefined test cases were executed with full" << endl;
    cout << "step-by-step DP table filling and backtracking." << endl;
    cout << "============================================================" << endl;
    cout << endl;
    cout << "Conclusion:" << endl;
    cout << "The LCS algorithm successfully found the longest common" << endl;
    cout << "subsequence for all test cases. By filling the DP table" << endl;
    cout << "bottom-up and backtracking through it, the algorithm" << endl;
    cout << "determined both the length and the actual subsequence" << endl;
    cout << "in O(m*n) time and space." << endl;

    return 0;
}
