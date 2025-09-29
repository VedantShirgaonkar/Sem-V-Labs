#include <stdio.h>
#include <stdlib.h>

int formingMagicSquare(int s[3][3]) {
    // All 8 possible 3x3 magic squares
    int magic[8][3][3] = {
        {{8,1,6},{3,5,7},{4,9,2}},
        {{6,1,8},{7,5,3},{2,9,4}},
        {{4,9,2},{3,5,7},{8,1,6}},
        {{2,9,4},{7,5,3},{6,1,8}},
        {{8,3,4},{1,5,9},{6,7,2}},
        {{4,3,8},{9,5,1},{2,7,6}},
        {{6,7,2},{1,5,9},{8,3,4}},
        {{2,7,6},{9,5,1},{4,3,8}}
    };

    int minCost = 100000; // Large number
    for(int k=0; k<8; k++) {
        int cost = 0;
        for(int i=0; i<3; i++) {
            for(int j=0; j<3; j++) {
                cost += abs(s[i][j] - magic[k][i][j]);
            }
        }
        if(cost < minCost) {
            minCost = cost;
        }
    }
    return minCost;
}

int main() {
    int s[3][3];
    for(int i=0; i<3; i++) {
        for(int j=0; j<3; j++) {
            scanf("%d", &s[i][j]);
        }
    }

    int result = formingMagicSquare(s);
    printf("%d\n", result);

    return 0;
}