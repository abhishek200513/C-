#include <iostream>
#include <vector>
#include <numeric>

using namespace std;

// Backtracking function to find all subsets that sum to targetSum
void sumOfSubsets(const vector<int>& w, int targetSum, vector<int>& subset, int sumSoFar, int totalRemaining, int index) {
    // If we have reached the exact target sum, we print the subset
    if (sumSoFar == targetSum) {
        cout << "{ ";
        for (int val : subset) {
            cout << val << " ";
        }
        cout << "}\n";
        return;
    }

    // If we considered all elements, stop
    if (index >= w.size()) {
        return;
    }

    // Pruning: if even including all remaining elements we can't reach the target,
    // or if we already exceeded it, stop exploring this branch
    if (sumSoFar + totalRemaining < targetSum || sumSoFar > targetSum) {
        return;
    }

    // Branch 1: Include the current element
    if (sumSoFar + w[index] <= targetSum) {
        subset.push_back(w[index]);
        sumOfSubsets(w, targetSum, subset, sumSoFar + w[index], totalRemaining - w[index], index + 1);
        subset.pop_back(); // backtrack
    }

    // Branch 2: Exclude the current element
    if (sumSoFar + totalRemaining - w[index] >= targetSum) {
        sumOfSubsets(w, targetSum, subset, sumSoFar, totalRemaining - w[index], index + 1);
    }
}

int main() {
    cout << "============================================================" << endl;
    cout << "              Sum of Subsets Problem" << endl;
    cout << "               (Backtracking Approach)" << endl;
    cout << "============================================================" << endl;

    int n;
    cout << "Enter the number of elements: ";
    cin >> n;

    vector<int> weights(n);
    int totalSum = 0;
    cout << "Enter the elements (in ascending order ideally): ";
    for (int i = 0; i < n; ++i) {
        cin >> weights[i];
        totalSum += weights[i];
    }

    int targetSum;
    cout << "Enter the target sum: ";
    cin >> targetSum;

    cout << "\nSubsets that sum to " << targetSum << " are:" << endl;
    
    // Check if a solution is even possible
    if (totalSum < targetSum || weights[0] > targetSum) {
        cout << "No subsets possible." << endl;
    } else {
        vector<int> subset;
        sumOfSubsets(weights, targetSum, subset, 0, totalSum, 0);
    }

    return 0;
}
