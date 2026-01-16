#!/usr/bin/env python3
# ----------------------------------------------------------------------
# File: benchmark_vector_add.py
# Author: Samira Babalou
# Date: 2026-01-15
# Purpose: Benchmark CPU vs GPU vector addition performance
# Notes:
#   - Runs on CPU-only systems
#   - Automatically enables GPU if available
#   - Saves results for plotting and CI usage
# ----------------------------------------------------------------------

import time
import numpy as np
import os

# Try GPU (CuPy)
try:
    import cupy as cp
    gpu_available = True
except ImportError:
    gpu_available = False

# Ensure output directory exists
output_dir = os.path.dirname(__file__)
output_file = os.path.join(output_dir, "performance_results.txt")

# Vector sizes to test
sizes = [1_000_000, 5_000_000, 10_000_000]

results = []

for N in sizes:
    # CPU benchmark
    a_cpu = np.random.rand(N)
    b_cpu = np.random.rand(N)

    start = time.time()
    _ = a_cpu + b_cpu
    cpu_time = time.time() - start

    gpu_time = None

    # GPU benchmark
    if gpu_available:
        a_gpu = cp.asarray(a_cpu)
        b_gpu = cp.asarray(b_cpu)

        cp.cuda.Stream.null.synchronize()
        start = time.time()
        _ = a_gpu + b_gpu
        cp.cuda.Stream.null.synchronize()
        gpu_time = time.time() - start

    results.append((N, cpu_time, gpu_time))

# Save results inside performance/ folder
with open(output_file, "w") as f:
    f.write("N,CPU_time,GPU_time\n")
    for N, cpu, gpu in results:
        f.write(f"{N},{cpu},{gpu}\n")

print(f"Benchmark completed. Results saved to {output_file}")
