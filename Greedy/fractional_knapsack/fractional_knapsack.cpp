#include <iostream>
#include <algorithm>
#include <iomanip>

using namespace std;

// Structure to represent an item
struct Item {
    int id;
    int weight;
    int profit;
    double ratio;  // profit-to-weight ratio
};

// ---------- Comparators for 3 Greedy Strategies ----------

// Strategy 1: Sort by weight (ascending) — least weight first
bool compareByWeight(Item a, Item b) {
    return a.weight < b.weight;
}

// Strategy 2: Sort by profit (descending) — max profit first
bool compareByProfit(Item a, Item b) {
    return a.profit > b.profit;
}

// Strategy 3: Sort by ratio (descending) — best ratio first
bool compareByRatio(Item a, Item b) {
    return a.ratio > b.ratio;
}

// Fractional Knapsack solver (generic — works with any sorting)
double fractionalKnapsack(Item items[], int n, int capacity, const string &strategyName) {

    cout << "\n====================================================" << endl;
    cout << "  Strategy: " << strategyName << endl;
    cout << "====================================================" << endl;
    cout << left << setw(6) << "Item"
         << setw(10) << "Weight"
         << setw(10) << "Profit"
         << setw(12) << "Ratio"
         << setw(18) << "Taken" << endl;
    cout << "----------------------------------------------------" << endl;

    double totalProfit = 0.0;
    int remainingCapacity = capacity;

    for (int i = 0; i < n; i++) {
        if (remainingCapacity == 0) break;

        if (items[i].weight <= remainingCapacity) {
            // Take the whole item
            totalProfit += items[i].profit;
            remainingCapacity -= items[i].weight;

            cout << left << setw(6) << items[i].id
                 << setw(10) << items[i].weight
                 << setw(10) << items[i].profit
                 << setw(12) << fixed << setprecision(2) << items[i].ratio
                 << "1.00 (Full)" << endl;
        } else {
            // Take fraction of the item
            double fraction = (double)remainingCapacity / items[i].weight;
            totalProfit += items[i].profit * fraction;

            cout << left << setw(6) << items[i].id
                 << setw(10) << items[i].weight
                 << setw(10) << items[i].profit
                 << setw(12) << fixed << setprecision(2) << items[i].ratio
                 << fixed << setprecision(2) << fraction << " (Fraction)" << endl;

            remainingCapacity = 0;
        }
    }

    cout << "----------------------------------------------------" << endl;
    cout << "  Total Profit = " << fixed << setprecision(2) << totalProfit << endl;
    cout << "====================================================" << endl;

    return totalProfit;
}

int main() {
    int n, capacity;

    cout << "====================================================" << endl;
    cout << "   FRACTIONAL KNAPSACK — 3 GREEDY STRATEGIES        " << endl;
    cout << "====================================================" << endl;

    cout << "\nEnter the number of items: ";
    cin >> n;

    // Use dynamic arrays to store original and copies
    Item original[n];

    cout << "\nEnter weight and profit for each item:" << endl;
    for (int i = 0; i < n; i++) {
        original[i].id = i + 1;
        cout << "  Item " << i + 1 << " -> Weight: ";
        cin >> original[i].weight;
        cout << "            Profit: ";
        cin >> original[i].profit;
        original[i].ratio = (double)original[i].profit / original[i].weight;
    }

    cout << "\nEnter the knapsack capacity: ";
    cin >> capacity;

    // Display all items
    cout << "\n====================================================" << endl;
    cout << "               ITEM TABLE                           " << endl;
    cout << "====================================================" << endl;
    cout << left << setw(6) << "Item"
         << setw(10) << "Weight"
         << setw(10) << "Profit"
         << setw(12) << "P/W Ratio" << endl;
    cout << "----------------------------------------------------" << endl;
    for (int i = 0; i < n; i++) {
        cout << left << setw(6) << original[i].id
             << setw(10) << original[i].weight
             << setw(10) << original[i].profit
             << fixed << setprecision(2) << original[i].ratio << endl;
    }
    cout << "  Knapsack Capacity = " << capacity << endl;
    cout << "====================================================" << endl;

    // ========== STRATEGY 1: Least Weight First ==========
    Item copy1[n];
    for (int i = 0; i < n; i++) copy1[i] = original[i];
    sort(copy1, copy1 + n, compareByWeight);
    double profit1 = fractionalKnapsack(copy1, n, capacity, "LEAST WEIGHT FIRST");

    // ========== STRATEGY 2: Maximum Profit First ==========
    Item copy2[n];
    for (int i = 0; i < n; i++) copy2[i] = original[i];
    sort(copy2, copy2 + n, compareByProfit);
    double profit2 = fractionalKnapsack(copy2, n, capacity, "MAXIMUM PROFIT FIRST");

    // ========== STRATEGY 3: Best Ratio First ==========
    Item copy3[n];
    for (int i = 0; i < n; i++) copy3[i] = original[i];
    sort(copy3, copy3 + n, compareByRatio);
    double profit3 = fractionalKnapsack(copy3, n, capacity, "BEST PROFIT/WEIGHT RATIO FIRST");

    // ========== COMPARISON ==========
    cout << "\n====================================================" << endl;
    cout << "            COMPARISON OF STRATEGIES                " << endl;
    cout << "====================================================" << endl;
    cout << left << setw(38) << "  Strategy"
         << "Profit" << endl;
    cout << "----------------------------------------------------" << endl;
    cout << left << setw(38) << "  1. Least Weight First"
         << fixed << setprecision(2) << profit1 << endl;
    cout << left << setw(38) << "  2. Maximum Profit First"
         << fixed << setprecision(2) << profit2 << endl;
    cout << left << setw(38) << "  3. Best Ratio First (Optimal)"
         << fixed << setprecision(2) << profit3 << endl;
    cout << "----------------------------------------------------" << endl;

    // Find the best strategy
    double best = max({profit1, profit2, profit3});
    cout << "\n  >> Best Strategy: ";
    if (best == profit3) cout << "BEST RATIO FIRST";
    else if (best == profit2) cout << "MAXIMUM PROFIT FIRST";
    else cout << "LEAST WEIGHT FIRST";
    cout << " with profit = " << fixed << setprecision(2) << best << endl;

    cout << "====================================================" << endl;

    return 0;
}
