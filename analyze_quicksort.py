#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import math
import sys
import copy
import csv

from gen_quicksort_cases import load_array_txt, quickSort

sys.setrecursionlimit(200000)


def timed_quicksort(arr):
    """Run quickSort on a *copy* of arr and return elapsed time in seconds."""
    a = copy.copy(arr)
    start = time.perf_counter()
    quickSort(a, 0, len(a) - 1)
    end = time.perf_counter()
    return end - start


def main():
    print("Loading arrays from txt files...")
    arr_random_full = load_array_txt("arr_random_100000.txt")
    arr_best_full   = load_array_txt("arr_quicksort_best_100000.txt")
    arr_worst_full  = load_array_txt("arr_quicksort_worst_100000.txt")

    sizes = [10_000, 20_000, 40_000, 80_000 , 100_000]

    # collect all rows here
    rows = []

    print("n\tcase\tT(s)\t\tT/(n log2 n)\t\tT/n^2")
    print("-" * 80)

    for n in sizes:
        A_rand  = arr_random_full[:n]
        A_best  = arr_best_full[:n]
        A_worst = arr_worst_full[:n]

        for case_name, arr in [
            ("random", A_rand),
            ("best",   A_best),
            ("worst",  A_worst),
        ]:
            t = timed_quicksort(arr)
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
    csv_filename = "quicksort_results.csv"
    with open(csv_filename, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["n", "case", "T_sec", "T_over_nlogn", "T_over_n2"]
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"\n[Saved] {csv_filename}")

    # ---------- save as Markdown ----------
    md_filename = "quicksort_results.md"
    with open(md_filename, "w") as f:
        f.write("| n | case | T (s) | T/(n log₂ n) | T/n² |\n")
        f.write("|---|------|--------|--------------|------|\n")
        for r in rows:
            f.write(
                f"| {r['n']} | {r['case']} | "
                f"{r['T_sec']:.6f} | {r['T_over_nlogn']:.3e} | {r['T_over_n2']:.3e} |\n"
            )
    print(f"[Saved] {md_filename}")

    # ---------- optional: compare with built-in sort on full 100000 ----------
    print("\nCompare with Python built-in sort on n = 100000:")
    n = 100_000
    for name, arr in [
        ("random", arr_random_full),
        ("best",   arr_best_full),
        ("worst",  arr_worst_full),
    ]:
        b = copy.copy(arr)
        start = time.perf_counter()
        b.sort()
        end = time.perf_counter()
        print(f"builtin.sort, {name}, n={n}: {end - start:.6f} s")


if __name__ == "__main__":
    main()
