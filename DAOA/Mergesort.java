import java.util.Scanner;

public class Mergesort {

    public static void combine(int[] A, int low, int mid, int high) {
        int[] temp = new int[A.length];
        int k = low;
        int i = low;
        int j = mid + 1;

        while (i <= mid && j <= high) {
            if (A[i] <= A[j]) {
                temp[k] = A[i];
                i++;
            } else {
                temp[k] = A[j];
                j++;
            }
            k++;
        }

        while (i <= mid) {
            temp[k] = A[i];
            i++;
            k++;
        }

        while (j <= high) {
            temp[k] = A[j];
            j++;
            k++;
        }

        for (int index = low; index <= high; index++) {
            A[index] = temp[index];
        }
    }

    public static void mergeSort(int[] A, int low, int high) {
        if (low < high) {
            int mid = (low + high) / 2;
            mergeSort(A, low, mid);
            mergeSort(A, mid + 1, high);
            combine(A, low, mid, high);
        }
    }

    public static void displayArray(int[] A) {
        for (int num : A) {
            System.out.print(num + " ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int[] arr = new int[0];
        int choice;

        do {
            System.out.println("\n--- MENU ---");
            System.out.println("1. Enter array elements");
            System.out.println("2. Display array");
            System.out.println("3. Sort using Merge Sort");
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
                    if (arr.length == 0) {
                        System.out.println("Array is empty!");
                    } else {
                        System.out.println("Array elements:");
                        displayArray(arr);
                    }
                    break;

                case 3:
                    if (arr.length == 0) {
                        System.out.println("Array is empty! Please enter elements first.");
                    } else {
                        mergeSort(arr, 0, arr.length - 1);
                        System.out.println("Array sorted successfully!");
                    }
                    break;

                case 4:
                    System.out.println("Exiting program...");
                    break;

                default:
                    System.out.println("Invalid choice! Try again.");
            }
        } while (choice != 4);

        sc.close();
    }
}