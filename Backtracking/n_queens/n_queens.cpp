#include <iostream>
#include <iomanip>
#include <vector>

using namespace std;

int solutionCount = 0;

// Print the board with queens placed
void printBoard(int board[], int n, int solNum) {

    cout << "\n  Solution " << solNum << ":" << endl;
    cout << "  ";
    for (int j = 0; j < n; j++)
        cout << "----";
    cout << "-" << endl;

    for (int i = 0; i < n; i++) {
        cout << "  |";
        for (int j = 0; j < n; j++) {
            if (board[i] == j)
                cout << " Q |";
            else
                cout << "   |";
        }
        cout << endl;

        cout << "  ";
        for (int j = 0; j < n; j++)
            cout << "----";
        cout << "-" << endl;
    }

    // Column positions
    cout << "  Placement: [";
    for (int i = 0; i < n; i++) {
        cout << "Q" << i + 1 << "=Col" << board[i] + 1;
        if (i < n - 1) cout << ", ";
    }
    cout << "]" << endl;
}

// Check if placing a queen at (row, col) is safe
// by checking against all previously placed queens (rows 0..row-1)
bool isSafe(int board[], int row, int col) {

    for (int i = 0; i < row; i++) {
        // Same column check
        if (board[i] == col)
            return false;

        // Diagonal check: |row_diff| == |col_diff|
        if (abs(i - row) == abs(board[i] - col))
            return false;
    }

    return true;
}

// Solve N-Queens using backtracking
// board[i] = column where queen is placed in row i
void solveNQueens(int board[], int row, int n, bool printAll) {

    if (row == n) {
        // All queens placed successfully
        solutionCount++;
        if (printAll || solutionCount <= 2) {
            printBoard(board, n, solutionCount);
        }
        return;
    }

    for (int col = 0; col < n; col++) {
        if (isSafe(board, row, col)) {
            board[row] = col;               // Place queen
            solveNQueens(board, row + 1, n, printAll);  // Recurse for next row
            board[row] = -1;                // Backtrack
        }
    }
}

int main() {
    int n;
    int choice;

    cout << "=====================================================" << endl;
    cout << "     N-QUEENS PROBLEM — BACKTRACKING APPROACH         " << endl;
    cout << "=====================================================" << endl;

    cout << "\nEnter the value of N: ";
    cin >> n;

    if (n <= 0) {
        cout << "\n  Invalid input! N must be a positive integer." << endl;
        return 1;
    }

    if (n == 1) {
        cout << "\n  Trivial case: Place 1 queen on a 1x1 board." << endl;
        cout << "  Solution 1:" << endl;
        cout << "  -----" << endl;
        cout << "  | Q |" << endl;
        cout << "  -----" << endl;
        cout << "\n  Total solutions: 1" << endl;
        return 0;
    }

    if (n == 2 || n == 3) {
        cout << "\n  No solution exists for N = " << n << "." << endl;
        cout << "  (It is impossible to place " << n << " non-attacking queens on a "
             << n << "x" << n << " board.)" << endl;
        return 0;
    }

    cout << "\nPrint all solutions or just first two?" << endl;
    cout << "  1. Print ALL solutions" << endl;
    cout << "  2. Print first 2 only (show total count)" << endl;
    cout << "  Choice: ";
    cin >> choice;

    bool printAll = (choice == 1);

    cout << "\n=====================================================" << endl;
    cout << "  Solving " << n << "-Queens Problem..." << endl;
    cout << "=====================================================" << endl;

    int board[n];
    for (int i = 0; i < n; i++)
        board[i] = -1;

    solutionCount = 0;
    solveNQueens(board, 0, n, printAll);

    if (!printAll && solutionCount > 2) {
        cout << "\n  ... (" << solutionCount - 2 << " more solutions not displayed)" << endl;
    }

    cout << "\n=====================================================" << endl;
    cout << "                     RESULT                           " << endl;
    cout << "=====================================================" << endl;
    cout << "  N = " << n << endl;
    cout << "  Total Solutions = " << solutionCount << endl;
    cout << "=====================================================" << endl;

    return 0;
}
