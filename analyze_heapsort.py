#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import math
import copy
import csv

# We reuse the loader/saver you already wrote
from gen_quicksort_cases import load_array_txt, save_array_txt


# ======================
# Heap sort (your code)
# ======================

def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[l] > arr[largest]:
        largest = l

    if r < n and arr[r] > arr[largest]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heapSort(arr):
    n = len(arr)

    # Build heap (max-heap)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # One by one extract an element from heap
    for i in range(n - 1, 0, -1):
        # Move current root to end
        arr[0], arr[i] = arr[i], arr[0]
        # Restore heap on reduced array
        heapify(arr, i, 0)


def timed_heapsort(arr):
    """Run heapSort on a *copy* and return elapsed time (seconds)."""
    a = copy.copy(arr)
    start = time.perf_counter()
    heapSort(a)
    end = time.perf_counter()
    return end - start


def main():
    N = 100_000

    print("Loading random array from arr_random_100000.txt ...")
    arr_random_full = load_array_txt("arr_random_100000.txt")

    # --------- generate heap-specific best & worst arrays ---------
    # Best-like for heap: already a max-heap -> descending
    print("Generating heap best-case array (descending) ...")
    arr_heap_best_full = list(range(N, 0, -1))  # N, N-1, ..., 1

    # Worst-like for heap: ascending
    print("Generating heap worst-case array (ascending) ...")
    arr_heap_worst_full = list(range(N))        # 0, 1, ..., N-1

    # Save them so you can test other algorithms on same data
    save_array_txt("arr_heap_best_100000.txt", arr_heap_best_full)
    save_array_txt("arr_heap_worst_100000.txt", arr_heap_worst_full)
    print("Saved:")
    print("  - arr_heap_best_100000.txt")
    print("  - arr_heap_worst_100000.txt")

    # --------- benchmarking ---------
    sizes = [10_000, 20_000, 40_000, 80_000, 100_000]
    rows = []

    print("\nHeap sort timing:")
    print("n\tcase\tT(s)\t\tT/(n log2 n)\t\tT/n^2")
    print("-" * 80)

    for n in sizes:
        A_rand  = arr_random_full[:n]
        A_best  = arr_heap_best_full[:n]
        A_worst = arr_heap_worst_full[:n]

        for case_name, arr in [
            ("random", A_rand),
            ("heap_best",  A_best),
            ("heap_worst", A_worst),
        ]:
            t = timed_heapsort(arr)
            t_over_nlogn = t / (n * math.log2(n))
            t_over_n2    = t / (n ** 2)

            print(f"{n}\t{case_name}\t{t:.6f}\t{t_over_nlogn:.3e}\t{t_over_n2:.3e}")

            rows.append({
                "n": n,
                "case": case_name,
                "T_sec": t,
                "T_over_nlogn": t_over_nlogn,
                "T_over_n2": t_over_n2,
            })

        print("-" * 80)

    # ---------- save as CSV ----------
    csv_filename = "heapsort_results.csv"
    with open(csv_filename, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["n", "case", "T_sec", "T_over_nlogn", "T_over_n2"]
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"\n[Saved] {csv_filename}")

    # ---------- save as Markdown ----------
    md_filename = "heapsort_results.md"
    with open(md_filename, "w") as f:
        f.write("| n | case | T (s) | T/(n log₂ n) | T/n² |\n")
        f.write("|---|------|--------|--------------|------|\n")
        for r in rows:
            f.write(
                f"| {r['n']} | {r['case']} | "
                f"{r['T_sec']:.6f} | {r['T_over_nlogn']:.3e} | {r['T_over_n2']:.3e} |\n"
            )
    print(f"[Saved] {md_filename}")


if __name__ == "__main__":
    main()
