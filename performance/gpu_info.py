# ============================================================
# File: performance/gpu_info.py
# Author: Samira Babalou
# Date: 2026-01-16
# Purpose:
#   Collect GPU/CUDA metadata in a robust, reproducible way
#   Works on Linux, WSL2, Docker, and CI runners
# ============================================================

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(BASE_DIR, "performance", "gpu_metadata.json")

info = {
    "gpu_available": False,
    "device_name": None,
    "gpu_memory_mb": None,
    "cuda_version": None,
    "cupy_version": None,
}

try:
    import cupy as cp

    info["gpu_available"] = True
    info["cupy_version"] = cp.__version__

    # ---------------- CUDA Version ----------------
    cuda_ver_int = cp.cuda.runtime.runtimeGetVersion()
    major = cuda_ver_int // 1000
    minor = (cuda_ver_int % 1000) // 10
    info["cuda_version"] = f"{major}.{minor}"

    # ---------------- GPU Name ----------------
    # Query CUDA runtime directly (most reliable method)
    name_bytes = cp.cuda.runtime.getDeviceProperties(0)["name"]
    info["device_name"] = name_bytes.decode("utf-8")

    # ---------------- GPU Memory ----------------
    free_mem, total_mem = cp.cuda.runtime.memGetInfo()
    info["gpu_memory_mb"] = int(total_mem // (1024 ** 2))

except Exception as e:
    info["error"] = str(e)

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w") as f:
    json.dump(info, f, indent=2)

print(f"GPU metadata written to {OUTPUT_PATH}")
