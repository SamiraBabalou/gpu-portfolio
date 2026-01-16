#!/usr/bin/env python3
# ----------------------------------------------------------------------
# File: plot_performance.py
# Author: Samira Babalou
# Date: 2026-01-15
# Purpose: Plot CPU vs GPU vector addition performance
# ----------------------------------------------------------------------

import matplotlib.pyplot as plt
import os

base_dir = os.path.dirname(__file__)
results_file = os.path.join(base_dir, "performance_results.txt")
figures_dir = os.path.join(base_dir, "..", "reports", "figures")


os.makedirs(figures_dir, exist_ok=True)

Ns = []
cpu_times = []
gpu_times = []

with open(results_file) as f:
    next(f)
    for line in f:
        N, cpu, gpu = line.strip().split(",")
        Ns.append(int(N))
        cpu_times.append(float(cpu))
        gpu_times.append(None if gpu == "None" else float(gpu))

plt.figure()
plt.plot(Ns, cpu_times, "o-", label="CPU")

if any(gpu_times):
    plt.plot(Ns, gpu_times, "o-", label="GPU")

plt.xlabel("Vector Size")
plt.ylabel("Time (seconds)")
plt.title("CPU vs GPU Vector Addition Performance")
plt.legend()
plt.grid(True)

output_path = os.path.join(figures_dir, "vector_add_performance.png")
plt.savefig(output_path)

print(f"Plot saved to {output_path}")
