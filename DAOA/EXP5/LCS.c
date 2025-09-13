#include <stdio.h>
#include <string.h>

#define MAX 50

void printLCS(char b[MAX][MAX], char X[], int i, int j) {
    if (i == 0 || j == 0) return;
    if (b[i][j] == 'D') {
        printLCS(b, X, i - 1, j - 1);
        printf("%c", X[i - 1]);
    } else if (b[i][j] == 'U') {
        printLCS(b, X, i - 1, j);
    } else {
        printLCS(b, X, i, j - 1);
    }
}

int main() {
    char X[MAX], Y[MAX], b[MAX][MAX];
    int c[MAX][MAX];
    int m, n, i, j;

    printf("Enter first sequence: ");
    scanf("%s", X);
    printf("Enter second sequence: ");
    scanf("%s", Y);

    m = strlen(X);
    n = strlen(Y);

    for (i = 0; i <= m; i++) c[i][0] = 0;
    for (j = 0; j <= n; j++) c[0][j] = 0;

    for (i = 1; i <= m; i++) {
        for (j = 1; j <= n; j++) {
            if (X[i - 1] == Y[j - 1]) {
                c[i][j] = c[i - 1][j - 1] + 1;
                b[i][j] = 'D'; 
            } else if (c[i - 1][j] >= c[i][j - 1]) {
                c[i][j] = c[i - 1][j];
                b[i][j] = 'U';
            } else {
                c[i][j] = c[i][j - 1];
                b[i][j] = 'L';
            }
        }
    }

    printf("LCS: ");
    printLCS(b, X, m, n);
    printf("\nLength of LCS: %d\n", c[m][n]);

    return 0;
}