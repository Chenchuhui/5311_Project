#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import math
import copy
import csv
import random

# reuse helpers from your previous file
from gen_quicksort_cases import load_array_txt, save_array_txt


# ======================
# Radix sort (your code)
# ======================

def countingSort(arr, exp1):
    n = len(arr)

    # The output array elements that will have sorted arr
    output = [0] * n

    # initialize count array as 0
    count = [0] * 10

    # Store count of occurrences in count[]
    for i in range(n):
        index = arr[i] // exp1
        count[index % 10] += 1

    # Change count[i] so that count[i] now contains actual
    # position of this digit in output array
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build the output array
    i = n - 1
    while i >= 0:
        index = arr[i] // exp1
        digit = index % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1
        i -= 1

    # Copy the output array to arr[]
    for i in range(n):
        arr[i] = output[i]


def radixSort(arr):
    if not arr:
        return

    # Find the maximum number to know number of digits
    max1 = max(arr)

    # Do counting sort for every digit. exp is 10^i
    exp = 1
    while max1 // exp >= 1:
        countingSort(arr, exp)
        exp *= 10


def timed_radixsort(arr):
    """Run radixSort on a copy and return elapsed time in seconds."""
    a = copy.copy(arr)
    start = time.perf_counter()
    radixSort(a)
    end = time.perf_counter()
    return end - start


def main():
    N = 100_000

    print("Loading random array from arr_random_100000.txt ...")
    # This was generated earlier as random ints in [0, 10^6]
    arr_random_full = load_array_txt("arr_random_100000.txt")

    # --------- generate radix-specific best & worst arrays ---------
    # Best-like for radix: numbers with FEWER digits (e.g., 0..999 -> up to 3 digits)
    print("Generating radix best-case array (0..999, few digits) ...")
    arr_radix_best_full = [random.randint(0, 999) for _ in range(N)]

    # Worst-like for radix: numbers with MORE digits (e.g., 0..10^9)
    print("Generating radix worst-case array (0..10^9, many digits) ...")
    arr_radix_worst_full = [random.randint(0, 10**9) for _ in range(N)]

    # Save them
    save_array_txt("arr_radix_best_100000.txt", arr_radix_best_full)
    save_array_txt("arr_radix_worst_100000.txt", arr_radix_worst_full)
    print("Saved:")
    print("  - arr_radix_best_100000.txt")
    print("  - arr_radix_worst_100000.txt")

    # --------- benchmarking ---------
    sizes = [10_000, 20_000, 40_000, 80_000, 100_000]
    rows = []

    print("\nRadix sort timing:")
    print("n\tcase\tT(s)\t\tT/n\t\tT/(n log2 n)")
    print("-" * 80)

    for n in sizes:
        A_rand  = arr_random_full[:n]        # ~ up to 10^6
        A_best  = arr_radix_best_full[:n]    # up to 999
        A_worst = arr_radix_worst_full[:n]   # up to 10^9

        for case_name, arr in [
            ("random",      A_rand),
            ("radix_best",  A_best),
            ("radix_worst", A_worst),
        ]:
            t = timed_radixsort(arr)
            t_over_n     = t / n
            t_over_nlogn = t / (n * math.log2(n))

            print(f"{n}\t{case_name}\t{t:.6f}\t{t_over_n:.3e}\t{t_over_nlogn:.3e}")

            rows.append({
                "n": n,
                "case": case_name,
                "T_sec": t,
                "T_over_n": t_over_n,
                "T_over_nlogn": t_over_nlogn,
            })

        print("-" * 80)

    # ---------- save as CSV ----------
    csv_filename = "radixsort_results.csv"
    with open(csv_filename, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["n", "case", "T_sec", "T_over_n", "T_over_nlogn"]
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"\n[Saved] {csv_filename}")

    # ---------- save as Markdown (ASCII only, no Unicode) ----------
    md_filename = "radixsort_results.md"
    with open(md_filename, "w") as f:
        f.write("| n | case | T (s) | T/n | T/(n log2 n) |\n")
        f.write("|---|------|--------|-----|-------------|\n")
        for r in rows:
            f.write(
                f"| {r['n']} | {r['case']} | "
                f"{r['T_sec']:.6f} | {r['T_over_n']:.3e} | {r['T_over_nlogn']:.3e} |\n"
            )
    print(f"[Saved] {md_filename}")


if __name__ == "__main__":
    main()
