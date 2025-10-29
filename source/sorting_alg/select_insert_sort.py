import numpy as np

# array of 10 randim integers between 0 and 100
arr = np.random.randint(0, 100, size=10)

def select_sort(arr):
    # manual implementation of selection sort
    for i in range(len(arr)):      
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

def insertion_sort(arr):
    # manual implementation of insertion sort
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >=0 and key < arr[j] :
                arr[j + 1] = arr[j]
                j -= 1
        arr[j + 1] = key
        
select_sort(arr)
print("Selection Sort Result:", arr)