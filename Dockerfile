# ----------------------------------------------------------------------
# File: Dockerfile
# Author: Samira Babalou
# Date: 2026-01-16
# Purpose: GPU-enabled container for running CUDA/CuPy notebooks
#          and performance benchmarks in a reproducible environment.
# Notes:
#   - Uses NVIDIA CUDA base image
#   - Installs Python, pip, Jupyter, and GPU libraries
#   - Registers a Jupyter kernel named 'gpu-portfolio'
#   - Works with Docker, local runs, and CI pipelines
# ----------------------------------------------------------------------

# Base NVIDIA CUDA image (runtime only, no driver)
FROM nvidia/cuda:12.2.0-base-ubuntu22.04

# Metadata
LABEL project="gpu-portfolio"
LABEL purpose="GPU computing portfolio with notebooks and benchmarks"

# ------------------------------------------------------------
# System dependencies
# ------------------------------------------------------------
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        git \
        build-essential && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Python dependencies
# ------------------------------------------------------------
RUN pip3 install --upgrade pip && \
    pip3 install \
        numpy \
        matplotlib \
        jupyter \
        ipykernel \
        cupy-cuda12x

# ------------------------------------------------------------
# Register Jupyter kernel (generic for any user)
# ------------------------------------------------------------
RUN python3 -m ipykernel install \
    --user \
    --name gpu-portfolio \
    --display-name "Python (gpu-portfolio)"

# ------------------------------------------------------------
# Generic non-root user
# ------------------------------------------------------------
RUN useradd -ms /bin/bash gpuuser
USER gpuuser
WORKDIR /workspace

# Copy repository contents
COPY --chown=gpuuser:gpuuser . /workspace

# Expose Jupyter port
EXPOSE 8888

# ------------------------------------------------------------
# Default command: start Jupyter Notebook
# ------------------------------------------------------------
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser"]
