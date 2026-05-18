#include <iostream>
#include <fstream>
#include <chrono>
#include <cstdlib>
#include <ctime>

using namespace std;
using namespace std::chrono;

// Global variables for configuration
const int ARRAY_MAX = 5000000;    // 10 lakh (10,00,000)
const int ARRAY_MIN = 50000;      // 50,000
const int INCREMENT = 10000;      // 10,000
const int ITERATIONS = 10000; 
// Number of runs per size (averaged)

// Partition function (Lomuto partition scheme)
int partition(int arr[], int low, int high) {
    int pivot = arr[high];  // Pivot is last element
    int i = low - 1;
    
    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}

// Quick Sort Function (Recursive)
void quickSort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        
        quickSort(arr, low, pi - 1);   // Sort left part
        quickSort(arr, pi + 1, high);   // Sort right part
    }
}

int main() {
    // Seed random number generator
    srand(static_cast<unsigned int>(time(0)));
    
    // Open output file
    ofstream outFile("quicksort_results.txt");
    
    if (!outFile) {
        cerr << "Error: Could not create output file!" << endl;
        return 1;
    }
    
    // Write header
    outFile << "Size,Time(microseconds)" << endl;
    
    cout << "==================================================" << endl;
    cout << "     QUICK SORT TIME COMPLEXITY ANALYSIS          " << endl;
    cout << "==================================================" << endl;
    cout << "Array Min: " << ARRAY_MIN << endl;
    cout << "Array Max: " << ARRAY_MAX << endl;
    cout << "Increment: " << INCREMENT << endl;
    cout << "Iterations: " << ITERATIONS << " (random arrays, averaged)" << endl;
    cout << "Expected Complexity: O(n log n)" << endl;
    cout << "==================================================" << endl;
    cout << endl;
    
    // Test for each size from ARRAY_MIN to ARRAY_MAX with INCREMENT
    for (int n = ARRAY_MIN; n <= ARRAY_MAX; n += INCREMENT) {
        
        double totalTime = 0;
        
        for (int iter = 0; iter < ITERATIONS; iter++) {
            // Create and fill array with random values for each iteration
            int* arr = new int[n];
            for (int i = 0; i < n; i++) {
                arr[i] = rand();
            }
            
            // Measure time for quick sort
            auto start = high_resolution_clock::now();
            quickSort(arr, 0, n - 1);
            auto end = high_resolution_clock::now();
            
            totalTime += duration_cast<nanoseconds>(end - start).count();
            
            // Free memory
            delete[] arr;
        }
        
        // Calculate average time in microseconds
        double avgTimeUs = (totalTime / ITERATIONS) / 1000.0;
        
        // Write to file
        outFile << n << "," << avgTimeUs << endl;
        
        // Display progress
        cout << "Array Size: " << n << "\t\tAvg Time: " << avgTimeUs << " us" << endl;
    }
    
    outFile.close();
    
    cout << endl;
    cout << "==================================================" << endl;
    cout << "Results saved to: quicksort_results.txt" << endl;
    cout << "==================================================" << endl;
    
    return 0;
}
