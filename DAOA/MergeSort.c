#include <stdio.h>
#include <stdlib.h>

// Function to merge two halves
void combine(int A[], int low, int mid, int high) {
    int temp[high - low + 1];
    int i = low;
    int j = mid + 1;
    int k = 0;

    while (i <= mid && j <= high) {
        if (A[i] <= A[j]) {
            temp[k++] = A[i++];
        } else {
            temp[k++] = A[j++];
        }
    }

    while (i <= mid) {
        temp[k++] = A[i++];
    }

    while (j <= high) {
        temp[k++] = A[j++];
    }

    for (int index = 0; index < k; index++) {
        A[low + index] = temp[index];
    }
}


void mergeSort(int A[], int low, int high) {
    if (low < high) {
        int mid = (low + high) / 2;
        mergeSort(A, low, mid);
        mergeSort(A, mid + 1, high);
        combine(A, low, mid, high);
    }
}


void displayArray(int A[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", A[i]);
    }
    printf("\n");
}

int main() {
    int *arr = NULL;
    int n = 0, choice;

    do {
        printf("\n--- MENU ---\n");
        printf("1. Enter array elements\n");
        printf("2. Display array\n");
        printf("3. Sort using Merge Sort\n");
        printf("4. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter number of elements: ");
                scanf("%d", &n);
                arr = (int *)malloc(n * sizeof(int));
                if (arr == NULL) {
                    printf("Memory allocation failed!\n");
                    exit(1);
                }
                printf("Enter %d elements:\n", n);
                for (int i = 0; i < n; i++) {
                    scanf("%d", &arr[i]);
                }
                break;

            case 2:
                if (n == 0) {
                    printf("Array is empty!\n");
                } else {
                    printf("Array elements:\n");
                    displayArray(arr, n);
                }
                break;

            case 3:
                if (n == 0) {
                    printf("Array is empty! Please enter elements first.\n");
                } else {
                    mergeSort(arr, 0, n - 1);
                    printf("Array sorted successfully!\n");
                }
                break;

            case 4:
                printf("Exiting program...\n");
                break;

            default:
                printf("Invalid choice! Try again.\n");
        }
    } while (choice != 4);

    free(arr);
    return 0;
}