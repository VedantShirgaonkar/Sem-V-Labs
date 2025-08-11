import java.util.Scanner;

public class QuickSort {

    // Quick Sort implementation
    public static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);  // sort left part
            quickSort(arr, pi + 1, high); // sort right part
        }
    }

    public static int partition(int[] arr, int low, int high) {
        int pivot = arr[high]; // pivot element
        int i = low - 1; // index of smaller element

        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                // swap arr[i] and arr[j]
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }

        // swap arr[i+1] and arr[high] (pivot)
        int temp = arr[i + 1];
        arr[i + 1] = arr[high];
        arr[high] = temp;

        return i + 1;
    }

    public static void displayArray(int[] arr) {
        if (arr == null) {
            System.out.println("Array not initialized!");
            return;
        }
        for (int value : arr) {
            System.out.print(value + " ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int[] arr = null;
        int choice;

        do {
            System.out.println("\n--- Quick Sort Menu ---");
            System.out.println("1. Enter array");
            System.out.println("2. Sort array using Quick Sort");
            System.out.println("3. Display array");
            System.out.println("4. Exit");
            System.out.print("Enter your choice: ");
            choice = sc.nextInt();

            switch (choice) {
                case 1:
                    System.out.print("Enter number of elements: ");
                    int n = sc.nextInt();
                    arr = new int[n];
                    System.out.println("Enter " + n + " elements:");
                    for (int i = 0; i < n; i++) {
                        arr[i] = sc.nextInt();
                    }
                    break;

                case 2:
                    if (arr == null) {
                        System.out.println("Please enter the array first!");
                    } else {
                        quickSort(arr, 0, arr.length - 1);
                        System.out.println("Array sorted successfully!");
                    }
                    break;

                case 3:
                    displayArray(arr);
                    break;

                case 4:
                    System.out.println("Exiting program...");
                    break;

                default:
                    System.out.println("Invalid choice! Please try again.");
            }

        } while (choice != 4);

        sc.close();
    }
}
