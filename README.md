# GPU Portfolio Project: Vector Addition Benchmark

## Overview

This repository demonstrates a reproducible GPU computing workflow using
NumPy (CPU) and CuPy (GPU) to benchmark vector addition performance.

The project is designed as a **portfolio-grade GPU systems project**,
showcasing:
- GPU acceleration principles
- Performance benchmarking methodology
- Reproducible environments (Conda, Docker)
- Automated execution (CI-ready)

The code runs correctly on systems **with or without a GPU**, using
automatic CPU fallback when needed.

---

## Objectives

- Compare CPU and GPU execution time for data-parallel workloads
- Demonstrate when GPU acceleration is beneficial
- Build a professional, reproducible GPU experiment pipeline
- Practice real-world tooling used in ML and HPC projects

---

## Methodology

1. Generate large random vectors
2. Perform element-wise vector addition on:
   - CPU using NumPy
   - GPU using CuPy (if available)
3. Measure execution time with synchronization
4. Compute speedup and analyze performance behavior
5. Automate execution via scripts and CI-compatible tooling

---

## Key Findings

- For moderate vector sizes, CPU performance may match or exceed GPU
- GPU benefits appear when workloads are large enough to amortize:
  - Kernel launch overhead
  - Host–device memory transfer costs
- This aligns with real-world GPU performance theory

---

## Repository Structure

```text
gpu-portfolio/
├── notebooks/
│   └── vector_addition.ipynb      # Main experiment notebook
├── performance/
│   ├── benchmark_vector_add.py    # CPU/GPU benchmark script
│   └── plot_performance.py        # Performance visualization
├── reports/
│   └── figures/                   # Generated plots
├── environment.yml                # Conda environment definition
├── Dockerfile                     # GPU-enabled Docker environment
├── run_notebooks.sh               # Automated notebook execution
├── .github/workflows/
│   └── gpu-ci.yml                 # CI workflow
└── README.md
````

---

## Quickstart

### Option 1: Docker (Recommended)

#### Requirements

* NVIDIA GPU
* NVIDIA driver installed
* Docker + NVIDIA Container Toolkit

#### Build image

```bash
docker build -t gpu-portfolio .
```

#### Run container

```bash
docker run --gpus all -it -p 8888:8888 gpu-portfolio
```

Copy the Jupyter URL with the token from the terminal and open it in a browser.

---

### Option 2: Conda (Local)

```bash
conda env create -f environment.yml
conda activate gpu-portfolio
jupyter notebook
```

---

## Notebook Execution (Automated)

To execute notebooks non-interactively:

```bash
bash run_notebooks.sh
```

This ensures:

* Correct kernel usage
* CI/Docker compatibility
* Reproducible execution

---

## Performance Analysis Notes

GPU acceleration is not guaranteed for all workloads.

Key factors affecting performance:

* Problem size
* Memory bandwidth
* Kernel launch overhead
* Host–device transfer cost

Designing GPU workloads requires careful scaling analysis.

---

## Notes

* The project runs safely on CPU-only systems
* GPU detection is automatic
* All components are CI-ready and Docker-compatible

