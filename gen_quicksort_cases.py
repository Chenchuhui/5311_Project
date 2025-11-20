#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import sys
from typing import List

# ==============================
# Quicksort (your implementation)
# ==============================

def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            swap(arr, i, j)
    swap(arr, i + 1, high)
    return i + 1

def quickSort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quickSort(arr, low, pi - 1)
        quickSort(arr, pi + 1, high)

# ==========================================
# Generators for random / best / worst cases
# ==========================================

def make_random_case(n: int, low: int = 0, high: int = 10**6) -> List[int]:
    """Random integers in [low, high]."""
    return [random.randint(low, high) for _ in range(n)]

def make_worst_case(n: int) -> List[int]:
    """
    Worst case for this quicksort (pivot = last element, < comparison):
    A sorted array (ascending) will make partitions extremely unbalanced.
    """
    return list(range(n))  # 0,1,2,...,n-1

def make_best_case_array(n: int) -> List[int]:
    """
    Construct a 'best-like' case for this quicksort:
    For each subarray [low, high], we try to put a median element at index 'high',
    so that partition() gets a good pivot and splits the array more evenly.
    """
    arr = list(range(n))  # start sorted

    def helper(low, high):
        if low >= high:
            return
        mid = (low + high) // 2   # choose median index
        # move median to the pivot position (high)
        arr[mid], arr[high] = arr[high], arr[mid]
        # left part: [low, mid-1]
        helper(low, mid - 1)
        # right part: [mid+1, high-1] (high already used)
        helper(mid + 1, high - 1)

    helper(0, n - 1)
    return arr

# =====================
# Save / load utilities
# =====================

def save_array_txt(filename: str, arr: List[int]) -> None:
    """
    Save array to a text file, one integer per line.
    This makes it easy to load from other languages as well.
    """
    with open(filename, "w") as f:
        for x in arr:
            f.write(f"{x}\n")

def load_array_txt(filename: str) -> List[int]:
    """
    Example loader (not strictly needed now, but handy later).
    """
    with open(filename, "r") as f:
        return [int(line.strip()) for line in f if line.strip()]

# =====================
# Main: generate & save
# =====================

if __name__ == "__main__":
    # so that worst-case quicksort won't crash if you test it
    sys.setrecursionlimit(200000)

    N = 100_000

    print(f"Generating arrays of size {N} ...")

    random_case = make_random_case(N)
    best_case   = make_best_case_array(N)
    worst_case  = make_worst_case(N)

    print("Saving arrays to text files ...")
    save_array_txt("arr_random_100000.txt", random_case)
    save_array_txt("arr_best_100000.txt", best_case)
    save_array_txt("arr_worst_100000.txt", worst_case)

    print("Done.")
    print("Files generated:")
    print("  - arr_random_100000.txt  (random data)")
    print("  - arr_best_100000.txt    (best-like case for this quicksort)")
    print("  - arr_worst_100000.txt   (sorted ascending: worst case for this quicksort)")

    # --- (Optional) quick test on small n to check correctness ---
    # You can comment this block out if you don't need it.

    test_arr = [10, 7, 8, 9, 1, 5]
    quickSort(test_arr, 0, len(test_arr) - 1)
    print("Small test sorted:", test_arr)
