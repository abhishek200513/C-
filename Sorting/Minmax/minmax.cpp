#include <iostream>
#include <fstream>
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <climits>

using namespace std;
using namespace std::chrono;

// Global variables for array size configuration
const int ARRAY_MAX = 1000000;    // 10 lakh (10,00,000)
const int ARRAY_MIN = 50000;     // 50,000
const int INCREMENT = 10000;     // 10,000
const int ITERATIONS = 50;        // Number of runs per size

// Volatile to prevent optimization
volatile int resultMin;
volatile int resultMax;

// Function to find minimum and maximum in a single traversal
void findMinMax(int arr[], int n, int& minVal, int& maxVal) {
    minVal = arr[0];
    maxVal = arr[0];
    
    for (int i = 1; i < n; i++) {
        if (arr[i] < minVal) {
            minVal = arr[i];
        }
        if (arr[i] > maxVal) {
            maxVal = arr[i];
        }
    }
}

int main() {
    // Seed random number generator
    srand(static_cast<unsigned int>(time(0)));
    
    // Open output file
    ofstream outFile("minmax_results.txt");
    
    if (!outFile) {
        cerr << "Error: Could not create output file!" << endl;
        return 1;
    }
    
    // Write header
    outFile << "Size,Time(microseconds)" << endl;
    
    cout << "==================================================" << endl;
    cout << "     MIN-MAX SEARCH TIME COMPLEXITY ANALYSIS      " << endl;
    cout << "==================================================" << endl;
    cout << "Array Min: " << ARRAY_MIN << endl;
    cout << "Array Max: " << ARRAY_MAX << endl;
    cout << "Increment: " << INCREMENT << endl;
    cout << "Iterations: " << ITERATIONS << " (averaged)" << endl;
    cout << "Expected Complexity: O(n)" << endl;
    cout << "==================================================" << endl;
    cout << endl;
    
    // Test for each size from ARRAY_MIN to ARRAY_MAX with INCREMENT
    for (int n = ARRAY_MIN; n <= ARRAY_MAX; n += INCREMENT) {
        
        // Create dynamic array
        int* arr = new int[n];
        
        // Run ITERATIONS and average the time
        double totalTime = 0;
        
        for (int iter = 0; iter < ITERATIONS; iter++) {
            // Fill array with random values for each iteration
            for (int i = 0; i < n; i++) {
                arr[i] = rand();
            }
            
            int minVal, maxVal;
            
            // Measure time for finding min and max
            auto start = high_resolution_clock::now();
            findMinMax(arr, n, minVal, maxVal);
            auto end = high_resolution_clock::now();
            
            // Store results to prevent optimization
            resultMin = minVal;
            resultMax = maxVal;
            
            totalTime += duration_cast<nanoseconds>(end - start).count();
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
    cout << "Results saved to: minmax_results.txt" << endl;
    cout << "==================================================" << endl;
    
    return 0;
}
