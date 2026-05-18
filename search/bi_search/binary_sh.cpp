#include <iostream>
#include <fstream>
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <algorithm>

using namespace std;
using namespace std::chrono;

// Global variables for array size configuration
const int ARRAY_MAX = 800000;   // 
const int ARRAY_MIN = 8000;      // 50,000
const int INCREMENT = 5000;      // 10,000
const int ITERATIONS = 100000;     // Many iterations because binary search is FAST!

// Volatile to prevent optimization
volatile int searchResult;

// Binary Search Function
int binarySearch(int arr[], int n, int key) {
    int left = 0;
    int right = n - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        
        if (arr[mid] == key) {
            return mid;  // Element found
        }
        else if (arr[mid] < key) {
            left = mid + 1;  // Search in right half
        }
        else {
            right = mid - 1;  // Search in left half
        }
    }
    return -1;  // Element not found
}

int main() {
    // Seed random number generator
    srand(static_cast<unsigned int>(time(0)));
    
    // Open output file
    ofstream outFile("binary_search_results.txt");
    
    if (!outFile) {
        cerr << "Error: Could not create output file!" << endl;
        return 1;
    }
    
    // Write header
    outFile << "Size,Time(nanoseconds)" << endl;
    
    cout << "==================================================" << endl;
    cout << "     BINARY SEARCH TIME COMPLEXITY ANALYSIS       " << endl;
    cout << "==================================================" << endl;
    cout << "Array Min: " << ARRAY_MIN << endl;
    cout << "Array Max: " << ARRAY_MAX << endl;
    cout << "Increment: " << INCREMENT << endl;
    cout << "Iterations: " << ITERATIONS << " (random keys, averaged)" << endl;
    cout << "Expected Complexity: O(log n)" << endl;
    cout << "==================================================" << endl;
    cout << endl;
    
    // Test for each size from ARRAY_MIN to ARRAY_MAX with INCREMENT
    for (int n = ARRAY_MIN; n <= ARRAY_MAX; n += INCREMENT) {
        
        // Create dynamic array
        int* arr = new int[n];
        
        // Fill array with sorted values (required for binary search)
        for (int i = 0; i < n; i++) {
            arr[i] = i;  // Sorted array: 0, 1, 2, ..., n-1
        }
        
        // Run ITERATIONS searches and measure total time
        auto start = high_resolution_clock::now();
        
        for (int iter = 0; iter < ITERATIONS; iter++) {
            // Pick a random key from the array
            int randomIndex = rand() % n;
            int key = arr[randomIndex];
            
            searchResult = binarySearch(arr, n, key);
        }
        
        auto end = high_resolution_clock::now();
        
        // Calculate average time in nanoseconds
        double totalTimeNs = duration_cast<nanoseconds>(end - start).count();
        double avgTimeNs = totalTimeNs / ITERATIONS;
        
        // Write to file
        outFile << n << "," << avgTimeNs << endl;
        
        // Display progress
        cout << "Array Size: " << n << "\t\tAvg Time: " << avgTimeNs << " ns" << endl;
        
        // Free memory
        delete[] arr;
    }
    
    outFile.close();
    
    cout << endl;
    cout << "==================================================" << endl;
    cout << "Results saved to: binary_search_results.txt" << endl;
    cout << "==================================================" << endl;
    
    return 0;
}
