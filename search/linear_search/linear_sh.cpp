#include <iostream>
#include <fstream>
#include <chrono>
#include <cstdlib>
#include <ctime>

using namespace std;
using namespace std::chrono;

// Global variables for array size configuration
const int ARRAY_MAX = 1000000; 
const int ARRAY_MIN = 50000;      // 50,000
const int INCREMENT = 10000;      // 10,000
const int ITERATIONS = 1000;        // Number of searches per size

// Volatile to prevent optimization
volatile int searchResult;

// Linear Search Function
int linearSearch(int arr[], int n, int key) {
    for (int i = 0; i < n; i++) {
        if (arr[i] == key) {
            return i;
        }
    }
    return -1;
}

int main() {
    // Seed random number generator
    srand(static_cast<unsigned int>(time(0)));
    
    // Open output file
    ofstream outFile("linear_search_results.txt");
    
    if (!outFile) {
        cerr << "Error: Could not create output file!" << endl;
        return 1;
    }
    
    // Write header
    outFile << "Size,Time(microseconds)" << endl;
    
    cout << "==================================================" << endl;
    cout << "     LINEAR SEARCH TIME COMPLEXITY ANALYSIS       " << endl;
    cout << "==================================================" << endl;
    cout << "Array Min: " << ARRAY_MIN << endl;
    cout << "Array Max: " << ARRAY_MAX << endl;
    cout << "Increment: " << INCREMENT << endl;
    cout << "Iterations: " << ITERATIONS << " (average case n/2, averaged)" << endl;
    cout << "==================================================" << endl;
    cout << endl;
    
    // Test for each size from ARRAY_MIN to ARRAY_MAX with INCREMENT
    for (int n = ARRAY_MIN; n <= ARRAY_MAX; n += INCREMENT) {
        
        // Create dynamic array
        int* arr = new int[n];
        
        // Fill array with random values
        for (int i = 0; i < n; i++) {
            arr[i] = rand();
        }
        
        // Run ITERATIONS searches and average the time
        double totalTime = 0;
        
        for (int iter = 0; iter < ITERATIONS; iter++) {
            // Place a unique marker at the MIDDLE of the array
            // This gives exactly average case O(n/2) behavior
            int targetPos = n / 2;
            arr[targetPos] = -999999 - iter;  // Unique value for each iteration
            int key = arr[targetPos];
            
            // Measure time for this search
            auto start = high_resolution_clock::now();
            searchResult = linearSearch(arr, n, key);
            auto end = high_resolution_clock::now();
            
            totalTime += duration_cast<nanoseconds>(end - start).count();
            
            // Reset the position to a random value
            arr[targetPos] = rand();
        }
        
        // Calculate average time in microseconds
        double avgTimeUs = (totalTime / ITERATIONS) / 1000.0;
        
        // Write to file
        outFile << n << "," << avgTimeUs << endl;
        
        // Display progress
        cout << "Array Size: " << n << "\t\tAvg Time: " << avgTimeUs << " us" << endl;
        
        // Free memory
        delete[] arr;
    }
    
    outFile.close();
    
    cout << endl;
    cout << "==================================================" << endl;
    cout << "Results saved to: linear_search_results.txt" << endl;
    cout << "==================================================" << endl;
    
    return 0;
}
