#include <iostream>
#include <fstream>
#include <chrono>
#include <cstdlib>
#include <ctime>

using namespace std;
using namespace std::chrono;

// Configuration
const int ARRAY_SIZE = 400000;   // Fixed array size
const int N_MIN = 2;             // Minimum N (binary search)
const int N_MAX = 40;            // Maximum N
const int ITERATIONS = 100000;   // Number of searches per N value

// Volatile to prevent optimization
volatile int searchResult;

// N-ary Search Function (Recursive)
// Splits the sorted array into N parts at each step
int narySearch(int arr[], int left, int right, int key, int n) {
    // Base case: invalid range
    if (left > right) {
        return -1;
    }
    
    int range = right - left;
    
    // Base case: range is small, do linear scan
    if (range < n) {
        for (int i = left; i <= right; i++) {
            if (arr[i] == key) {
                return i;
            }
        }
        return -1;
    }
    
    // Check each of the N-1 midpoints
    for (int i = 1; i < n; i++) {
        int mid = left + (range * i) / n;
        
        if (arr[mid] == key) {
            return mid;  // Element found at a midpoint
        }
        
        if (arr[mid] > key) {
            // Key lies in the segment before this midpoint
            int prevMid = (i == 1) ? left : left + (range * (i - 1)) / n + 1;
            return narySearch(arr, prevMid, mid - 1, key, n);  // Recurse
        }
    }
    
    // Key is greater than all midpoints, search in the last segment
    int lastMid = left + (range * (n - 1)) / n;
    return narySearch(arr, lastMid + 1, right, key, n);  // Recurse
}

int main() {
    // Seed random number generator
    srand(static_cast<unsigned int>(time(0)));
    
    // Open output file
    ofstream outFile("nary_search_results.txt");
    
    if (!outFile) {
        cerr << "Error: Could not create output file!" << endl;
        return 1;
    }
    
    // Write header
    outFile << "N,Time(nanoseconds)" << endl;
    
    cout << "==================================================" << endl;
    cout << "     N-ARY SEARCH - TIME vs N ANALYSIS            " << endl;
    cout << "==================================================" << endl;
    cout << "Fixed Array Size: " << ARRAY_SIZE << endl;
    cout << "N Range: " << N_MIN << " to " << N_MAX << endl;
    cout << "Iterations: " << ITERATIONS << " (random keys, averaged)" << endl;
    cout << "==================================================" << endl;
    cout << endl;
    
    // Create and fill array once (sorted)
    int* arr = new int[ARRAY_SIZE];
    for (int i = 0; i < ARRAY_SIZE; i++) {
        arr[i] = i;  // Sorted array: 0, 1, 2, ..., ARRAY_SIZE-1
    }
    
    // Test for each value of N
    for (int n = N_MIN; n <= N_MAX; n++) {
        
        // Run ITERATIONS searches and measure total time
        auto start = high_resolution_clock::now();
        
        for (int iter = 0; iter < ITERATIONS; iter++) {
            // Pick a random key from the array
            int randomIndex = rand() % ARRAY_SIZE;
            int key = arr[randomIndex];
            
            searchResult = narySearch(arr, 0, ARRAY_SIZE - 1, key, n);
        }
        
        auto end = high_resolution_clock::now();
        
        // Calculate average time in nanoseconds
        double totalTimeNs = duration_cast<nanoseconds>(end - start).count();
        double avgTimeNs = totalTimeNs / ITERATIONS;
        
        // Write to file
        outFile << n << "," << avgTimeNs << endl;
        
        // Display progress
        cout << "N = " << n << "\t\tAvg Time: " << avgTimeNs << " ns" << endl;
    }
    
    // Free memory
    delete[] arr;
    outFile.close();
    
    cout << endl;
    cout << "==================================================" << endl;
    cout << "Results saved to: nary_search_results.txt" << endl;
    cout << "==================================================" << endl;
    
    return 0;
}
