#include <algorithm>
#include <iomanip>
#include <iostream>
#include <vector>

using namespace std;

void printSet(const vector<int> &set) {
    cout << "{ ";
    for (int value : set) {
        cout << value << ' ';
    }
    cout << '}';
}

void printSubset(const vector<int> &subset) {
    cout << "{ ";
    for (int value : subset) {
        cout << value << ' ';
    }
    cout << "}\n";
}

void printDPTable(const vector<vector<bool>> &dp) {
    int n = static_cast<int>(dp.size()) - 1;
    int target = static_cast<int>(dp[0].size()) - 1;

    cout << setw(8) << "i/S";
    for (int sum = 0; sum <= target; ++sum) {
        cout << setw(4) << sum;
    }
    cout << '\n';

    for (int i = 0; i <= n; ++i) {
        cout << setw(8) << i;
        for (int sum = 0; sum <= target; ++sum) {
            cout << setw(4) << (dp[i][sum] ? "T" : "F");
        }
        cout << '\n';
    }
}

void findAllSubsets(const vector<int> &set,
                    int index,
                    int target,
                    int currentSum,
                    vector<int> &currentSubset,
                    vector<vector<int>> &solutions) {
    if (currentSum == target) {
        solutions.push_back(currentSubset);
        return;
    }

    if (index == static_cast<int>(set.size()) || currentSum > target) {
        return;
    }

    currentSubset.push_back(set[index]);
    findAllSubsets(set, index + 1, target, currentSum + set[index], currentSubset, solutions);

    currentSubset.pop_back();
    findAllSubsets(set, index + 1, target, currentSum, currentSubset, solutions);
}

vector<vector<bool>> buildDPTable(const vector<int> &set, int target) {
    int n = static_cast<int>(set.size());
    vector<vector<bool>> dp(n + 1, vector<bool>(target + 1, false));

    for (int i = 0; i <= n; ++i) {
        dp[i][0] = true;
    }

    for (int i = 1; i <= n; ++i) {
        for (int sum = 1; sum <= target; ++sum) {
            bool excludeElement = dp[i - 1][sum];
            bool includeElement = false;

            if (set[i - 1] <= sum) {
                includeElement = dp[i - 1][sum - set[i - 1]];
            }

            dp[i][sum] = excludeElement || includeElement;
        }
    }

    return dp;
}

void arrangeSolutions(vector<vector<int>> &solutions) {
    for (auto &subset : solutions) {
        sort(subset.begin(), subset.end());
    }

    sort(solutions.begin(), solutions.end(), [](const vector<int> &left, const vector<int> &right) {
        if (left.size() != right.size()) {
            return left.size() < right.size();
        }
        return left < right;
    });

    solutions.erase(unique(solutions.begin(), solutions.end()), solutions.end());
}

void runTestCase(int testNumber, const vector<int> &inputSet, int target) {
    vector<int> set = inputSet;
    vector<int> currentSubset;
    vector<vector<int>> solutions;

    sort(set.begin(), set.end());

    cout << "Test Case " << testNumber << " (Target = " << target << ")\n";
    cout << "Set: ";
    printSet(set);
    cout << "\n\n";

    vector<vector<bool>> dp = buildDPTable(set, target);

    cout << "Final DP Table:\n";
    printDPTable(dp);
    cout << "---------------------------\n";

    findAllSubsets(set, 0, target, 0, currentSubset, solutions);

    if (solutions.empty()) {
        cout << "No subset found\n";
    } else {
        arrangeSolutions(solutions);
        cout << "Total Subsets Found: " << solutions.size() << '\n';
        for (const auto &subset : solutions) {
            printSubset(subset);
        }
    }

    cout << "\nSubset Sum Exists: " << (dp[set.size()][target] ? "Yes" : "No") << '\n';
    cout << "\n---------------------------\n";
}

int main() {
    runTestCase(1, {5, 10, 12, 13, 15, 18}, 10);
    runTestCase(2, {2, 4, 6, 8}, 10);
    runTestCase(3, {3, 7, 9}, 5);
    runTestCase(4, {1, 2, 3, 4, 5}, 5);
    runTestCase(5, {1, 1, 2, 3}, 4);

    cout << "Time Complexity: O(n*target) for DP and O(2^n) for listing all subsets\n";
    cout << "Space Complexity: O(n*target) for DP and O(n) recursion stack\n";

    return 0;
}
