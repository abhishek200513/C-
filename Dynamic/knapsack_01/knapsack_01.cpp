#include <iostream>
#include <iomanip>

using namespace std;

// 0/1 Knapsack using Dynamic Programming (Bottom-Up Tabulation)
// Returns the maximum profit achievable within the given capacity
int knapsack01(int weights[], int profits[], int n, int capacity, int** dp) {

    // Build the DP table bottom-up
    // dp[i][w] = max profit using items 1..i with capacity w
    for (int i = 0; i <= n; i++) {
        for (int w = 0; w <= capacity; w++) {
            if (i == 0 || w == 0) {
                dp[i][w] = 0;  // Base case: no items or no capacity
            }
            else if (weights[i - 1] <= w) {
                // Item i can fit — choose max of including or excluding it
                int include = profits[i - 1] + dp[i - 1][w - weights[i - 1]];
                int exclude = dp[i - 1][w];
                dp[i][w] = max(include, exclude);
            }
            else {
                // Item i is too heavy — skip it
                dp[i][w] = dp[i - 1][w];
            }
        }
    }

    return dp[n][capacity];
}

// Trace back through the DP table to find which items were selected
void traceSelectedItems(int** dp, int weights[], int profits[], int n, int capacity) {

    cout << "\n  Selected Items:" << endl;
    cout << "  " << left << setw(8) << "Item"
         << setw(10) << "Weight"
         << setw(10) << "Profit" << endl;
    cout << "  ----------------------------------" << endl;

    int totalWeight = 0;
    int w = capacity;

    for (int i = n; i > 0; i--) {
        // If value came from above, item i was NOT included
        // If it differs, item i WAS included
        if (dp[i][w] != dp[i - 1][w]) {
            cout << "  " << left << setw(8) << i
                 << setw(10) << weights[i - 1]
                 << setw(10) << profits[i - 1] << endl;
            totalWeight += weights[i - 1];
            w -= weights[i - 1];
        }
    }

    cout << "  ----------------------------------" << endl;
    cout << "  Total Weight Used = " << totalWeight << " / " << capacity << endl;
}

// Print the full DP table for visualization
void printDPTable(int** dp, int n, int capacity, int weights[]) {

    cout << "\n=====================================================" << endl;
    cout << "                   DP TABLE                          " << endl;
    cout << "=====================================================" << endl;

    // Header row: capacities
    cout << setw(8) << "i\\w |";
    for (int w = 0; w <= capacity; w++) {
        cout << setw(5) << w;
    }
    cout << endl;

    cout << "  ------+";
    for (int w = 0; w <= capacity; w++) {
        cout << "-----";
    }
    cout << endl;

    // Print each row
    for (int i = 0; i <= n; i++) {
        if (i == 0)
            cout << "  " << setw(4) << left << 0 << "  |";
        else
            cout << "  " << setw(4) << left << i << "  |";

        for (int w = 0; w <= capacity; w++) {
            cout << right << setw(5) << dp[i][w];
        }
        cout << endl;
    }

    cout << "=====================================================" << endl;
}

int main() {
    int n, capacity;

    cout << "=====================================================" << endl;
    cout << "   0/1 KNAPSACK — DYNAMIC PROGRAMMING (TABULATION)   " << endl;
    cout << "=====================================================" << endl;

    cout << "\nEnter the number of items: ";
    cin >> n;

    int weights[n], profits[n];

    cout << "\nEnter weight and profit for each item:" << endl;
    for (int i = 0; i < n; i++) {
        cout << "  Item " << i + 1 << " -> Weight: ";
        cin >> weights[i];
        cout << "            Profit: ";
        cin >> profits[i];
    }

    cout << "\nEnter the knapsack capacity: ";
    cin >> capacity;

    // Display all items
    cout << "\n=====================================================" << endl;
    cout << "                    ITEM TABLE                        " << endl;
    cout << "=====================================================" << endl;
    cout << left << setw(8) << "  Item"
         << setw(10) << "Weight"
         << setw(10) << "Profit" << endl;
    cout << "-----------------------------------------------------" << endl;
    for (int i = 0; i < n; i++) {
        cout << left << setw(8) << ("  " + to_string(i + 1))
             << setw(10) << weights[i]
             << setw(10) << profits[i] << endl;
    }
    cout << "  Knapsack Capacity = " << capacity << endl;
    cout << "=====================================================" << endl;

    // Allocate DP table
    int** dp = new int*[n + 1];
    for (int i = 0; i <= n; i++) {
        dp[i] = new int[capacity + 1];
    }

    // Solve
    int maxProfit = knapsack01(weights, profits, n, capacity, dp);

    // Print DP table (only if capacity is small enough to display nicely)
    if (capacity <= 20) {
        printDPTable(dp, n, capacity, weights);
    } else {
        cout << "\n  (DP table display skipped — capacity > 20)" << endl;
    }

    // Results
    cout << "\n=====================================================" << endl;
    cout << "                     RESULT                           " << endl;
    cout << "=====================================================" << endl;
    cout << "  Maximum Profit = " << maxProfit << endl;

    traceSelectedItems(dp, weights, profits, n, capacity);

    cout << "=====================================================" << endl;

    // Free memory
    for (int i = 0; i <= n; i++) {
        delete[] dp[i];
    }
    delete[] dp;

    return 0;
}
