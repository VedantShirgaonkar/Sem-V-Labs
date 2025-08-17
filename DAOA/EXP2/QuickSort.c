#include <stdio.h>
#include <stdlib.h>


void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}


int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low - 1;

    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return i + 1;
}


void quickSort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);  
        quickSort(arr, pi + 1, high); 
    }
}


void displayArray(int arr[], int n) {
    if (arr == NULL || n == 0) {
        printf("Array not initialized!\n");
        return;
    }
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    int *arr = NULL;
    int n = 0, choice;

    do {
        printf("\n--- Quick Sort Menu ---\n");
        printf("1. Enter array\n");
        printf("2. Sort array using Quick Sort\n");
        printf("3. Display array\n");
        printf("4. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter number of elements: ");
                scanf("%d", &n);
                arr = (int *)malloc(n * sizeof(int));
                printf("Enter %d elements:\n", n);
                for (int i = 0; i < n; i++) {
                    scanf("%d", &arr[i]);
                }
                break;

            case 2:
                if (arr == NULL || n == 0) {
                    printf("Please enter the array first!\n");
                } else {
                    quickSort(arr, 0, n - 1);
                    printf("Array sorted successfully!\n");
                }
                break;

            case 3:
                displayArray(arr, n);
                break;

            case 4:
                printf("Exiting program...\n");
                break;

            default:
                printf("Invalid choice! Please try again.\n");
        }
    } while (choice != 4);

    free(arr);
    return 0;
}