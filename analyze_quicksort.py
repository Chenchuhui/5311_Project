#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import math
import sys
import copy

# ==========================
# Import from your generator
# ==========================
# If your previous file was named gen_quicksort_cases.py,
# make sure it's in the same folder and has load_array_txt and quickSort defined.

from gen_quicksort_cases import load_array_txt, quickSort

# Make sure recursion won't crash in worst case (still may be slow!)
sys.setrecursionlimit(200000)


def timed_quicksort(arr):
    """Run quickSort on a *copy* of arr and return elapsed time in seconds."""
    a = copy.copy(arr)
    start = time.perf_counter()
    quickSort(a, 0, len(a) - 1)
    end = time.perf_counter()
    return end - start


def main():
    # -------- 1. Load full arrays (100000 each) --------
    print("Loading arrays from txt files...")
    arr_random_full = load_array_txt("arr_random_100000.txt")
    arr_best_full   = load_array_txt("arr_best_100000.txt")
    arr_worst_full  = load_array_txt("arr_worst_100000.txt")

    # -------- 2. Choose test sizes --------
    # you can adjust this if your computer is too slow
    sizes = [10_000, 20_000, 40_000, 80_000]

    print("n\tcase\tT(s)\t\tT/(n log2 n)\t\tT/n^2")
    print("-" * 80)

    for n in sizes:
        # Take the first n elements from the 100000 arrays
        A_rand  = arr_random_full[:n]
        A_best  = arr_best_full[:n]
        A_worst = arr_worst_full[:n]

        # Random / average case
        t_rand = timed_quicksort(A_rand)
        print(f"{n}\trandom\t{t_rand:.6f}\t{t_rand/(n*math.log2(n)):.3e}\t{t_rand/(n**2):.3e}")

        # Best-like case
        t_best = timed_quicksort(A_best)
        print(f"{n}\tbest  \t{t_best:.6f}\t{t_best/(n*math.log2(n)):.3e}\t{t_best/(n**2):.3e}")

        # Worst case (may be slow!)
        t_worst = timed_quicksort(A_worst)
        print(f"{n}\tworst \t{t_worst:.6f}\t{t_worst/(n*math.log2(n)):.3e}\t{t_worst/(n**2):.3e}")

        print("-" * 80)


    # -------- 3. Optional: compare to Python's built-in sort on 100000 --------
    print("\nCompare with Python built-in sort on n = 100000:")
    n = 100_000
    for name, arr in [
        ("random", arr_random_full),
        ("best  ", arr_best_full),
        ("worst ", arr_worst_full),
    ]:
        b = copy.copy(arr)
        start = time.perf_counter()
        b.sort()
        end = time.perf_counter()
        print(f"builtin.sort, {name}, n={n}: {end - start:.6f} s")


if __name__ == "__main__":
    main()
