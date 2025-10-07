#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAX 30

int board[MAX];  // board[i] stores column position of queen in row i

// Function to check if placing queen is safe
int place(int row, int column) {
    for (int i = 1; i < row; i++) {
        if (board[i] == column || abs(board[i] - column) == abs(i - row))
            return 0;  // conflict found
    }
    return 1;  // safe position
}

void print_board(int n) {
    printf("\nSolution:\n");
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            if (board[i] == j)
                printf(" Q ");
            else
                printf(" . ");
        }
        printf("\n");
    }
}

//Solve nqueen using backtracking and recursion
void queen(int row, int n) {
    for (int column = 1; column <= n; column++) {
        if (place(row, column)) {
            board[row] = column;  // place queen

            if (row == n)
                print_board(n);  // solution found
            else
                queen(row + 1, n);  // try next queen
        }
    }
}

int main() {
    int n;
    printf("Enter number of Queens: ");
    scanf("%d", &n);

    if (n < 1) {
        printf("Invalid number of queens!\n");
        return 0;
    }

    queen(1, n);
    return 0;
}