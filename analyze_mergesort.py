#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import math
import copy
import csv

from gen_quicksort_cases import load_array_txt, save_array_txt


def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m

    L = [0] * n1
    R = [0] * n2

    for i in range(n1):
        L[i] = arr[l + i]
    for j in range(n2):
        R[j] = arr[m + 1 + j]

    i = j = 0
    k = l

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


def mergeSort(arr, l, r):
    if l < r:
        m = l + (r - l) // 2
        mergeSort(arr, l, m)
        mergeSort(arr, m + 1, r)
        merge(arr, l, m, r)


def timed_mergesort(arr):
    """Run mergeSort on a *copy* and return elapsed time in seconds."""
    a = copy.copy(arr)
    start = time.perf_counter()
    mergeSort(a, 0, len(a) - 1)
    end = time.perf_counter()
    return end - start


def main():
    N = 100_000

    print("Loading random array from arr_random_100000.txt ...")
    arr_random_full = load_array_txt("arr_random_100000.txt")

    print("Generating merge best-case array (ascending) ...")
    arr_merge_best_full = list(range(N))           # 0, 1, ..., N-1

    print("Generating merge worst-case array (descending) ...")
    arr_merge_worst_full = list(range(N, 0, -1))   # N, ..., 1

    save_array_txt("arr_merge_best_100000.txt", arr_merge_best_full)
    save_array_txt("arr_merge_worst_100000.txt", arr_merge_worst_full)
    print("Saved:")
    print("  - arr_merge_best_100000.txt")
    print("  - arr_merge_worst_100000.txt")

    sizes = [10_000, 20_000, 40_000, 80_000, 100_000]
    rows = []

    print("\nMerge sort timing:")
    print("n\tcase\tT(s)\t\tT/(n log2 n)\t\tT/n^2")
    print("-" * 80)

    for n in sizes:
        A_rand  = arr_random_full[:n]
        A_best  = arr_merge_best_full[:n]
        A_worst = arr_merge_worst_full[:n]

        for case_name, arr in [
            ("random",      A_rand),
            ("merge_best",  A_best),
            ("merge_worst", A_worst),
        ]:
            t = timed_mergesort(arr)
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

    csv_filename = "mergesort_results.csv"
    with open(csv_filename, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["n", "case", "T_sec", "T_over_nlogn", "T_over_n2"]
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"\n[Saved] {csv_filename}")

    md_filename = "mergesort_results.md"
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
