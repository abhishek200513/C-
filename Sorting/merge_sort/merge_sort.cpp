#include <iostream>
#include <fstream>
#include <chrono>
#include <cstdlib>
#include <ctime>

using namespace std;
using namespace std::chrono;

// Global variables for configuration
const int ARRAY_MAX = 200000;      // 500,000
const int ARRAY_MIN = 50000;       // 50,000
const int INCREMENT = 10000;       // 10,000
const int ITERATIONS = 100;        // Number of runs per size (averaged)

// Merge two sorted halves into a single sorted array
void merge(int arr[], int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;

    // Create temporary arrays
    int* L = new int[n1];
    int* R = new int[n2];

    // Copy data to temporary arrays
    for (int i = 0; i < n1; i++)
        L[i] = arr[left + i];
    for (int j = 0; j < n2; j++)
        R[j] = arr[mid + 1 + j];

    // Merge the temporary arrays back into arr[left..right]
    int i = 0, j = 0, k = left;

    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    // Copy remaining elements of L[], if any
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    // Copy remaining elements of R[], if any
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }

    // Free temporary arrays
    delete[] L;
    delete[] R;
}

// Merge Sort Function (Recursive)
void mergeSort(int arr[], int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;

        mergeSort(arr, left, mid);       // Sort left half
        mergeSort(arr, mid + 1, right);  // Sort right half
        merge(arr, left, mid, right);    // Merge sorted halves
    }
}

int main() {
    // Seed random number generator
    srand(static_cast<unsigned int>(time(0)));

    // Open output file
    ofstream outFile("mergesort_results.txt");

    if (!outFile) {
        cerr << "Error: Could not create output file!" << endl;
        return 1;
    }

    // Write header
    outFile << "Size,Time(microseconds)" << endl;

    cout << "==================================================" << endl;
    cout << "     MERGE SORT TIME COMPLEXITY ANALYSIS          " << endl;
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

            // Measure time for merge sort
            auto start = high_resolution_clock::now();
            mergeSort(arr, 0, n - 1);
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
    cout << "Results saved to: mergesort_results.txt" << endl;
    cout << "==================================================" << endl;

    return 0;
}
