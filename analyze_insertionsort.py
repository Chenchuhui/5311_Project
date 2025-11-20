#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import math
import copy
import csv

from gen_quicksort_cases import load_array_txt, save_array_txt


# =========================
# Insertion sort (your code)
# =========================

def insertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # Move elements of arr[0..i-1] that are greater than key
        # to one position ahead of their current position
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def timed_insertionsort(arr):
    """Run insertionSort on a *copy* and return elapsed time in seconds."""
    a = copy.copy(arr)
    start = time.perf_counter()
    insertionSort(a)
    end = time.perf_counter()
    return end - start


def main():
    N = 100_000

    print("Loading random array from arr_random_100000.txt ...")
    arr_random_full = load_array_txt("arr_random_100000.txt")

    # --------- generate insertion-specific best & worst arrays ---------
    # Best case for insertion sort: already sorted ascending
    print("Generating insertion best-case array (ascending) ...")
    arr_ins_best_full = list(range(N))           # 0, 1, ..., N-1

    # Worst case for insertion sort: sorted descending
    print("Generating insertion worst-case array (descending) ...")
    arr_ins_worst_full = list(range(N, 0, -1))   # N, ..., 1

    # Save them so you can reuse for other algorithms too
    save_array_txt("arr_insert_best_100000.txt", arr_ins_best_full)
    save_array_txt("arr_insert_worst_100000.txt", arr_ins_worst_full)
    print("Saved:")
    print("  - arr_insert_best_100000.txt")
    print("  - arr_insert_worst_100000.txt")

    # --------- benchmarking ---------
    # For insertion sort, n^2 grows very fast, so use smaller sizes
    sizes = [1_000, 2_000, 4_000, 8_000, 16_000, 32_000]
    rows = []

    print("\nInsertion sort timing:")
    print("n\tcase\tT(s)\t\tT/n\t\tT/n^2")
    print("-" * 80)

    for n in sizes:
        A_rand  = arr_random_full[:n]
        A_best  = arr_ins_best_full[:n]
        A_worst = arr_ins_worst_full[:n]

        for case_name, arr in [
            ("random",       A_rand),
            ("insert_best",  A_best),
            ("insert_worst", A_worst),
        ]:
            t = timed_insertionsort(arr)
            t_over_n  = t / n
            t_over_n2 = t / (n ** 2)

            print(f"{n}\t{case_name}\t{t:.6f}\t{t_over_n:.3e}\t{t_over_n2:.3e}")

            rows.append({
                "n": n,
                "case": case_name,
                "T_sec": t,
                "T_over_n": t_over_n,
                "T_over_n2": t_over_n2,
            })

        print("-" * 80)

    # ---------- save as CSV ----------
    csv_filename = "insertionsort_results.csv"
    with open(csv_filename, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["n", "case", "T_sec", "T_over_n", "T_over_n2"]
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"\n[Saved] {csv_filename}")

    # ---------- save as Markdown ----------
    md_filename = "insertionsort_results.md"
    with open(md_filename, "w") as f:
        f.write("| n | case | T (s) | T/n | T/n² |\n")
        f.write("|---|------|--------|-----|------|\n")
        for r in rows:
            f.write(
                f"| {r['n']} | {r['case']} | "
                f"{r['T_sec']:.6f} | {r['T_over_n']:.3e} | {r['T_over_n2']:.3e} |\n"
            )
    print(f"[Saved] {md_filename}")


if __name__ == "__main__":
    main()
