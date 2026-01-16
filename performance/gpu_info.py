# ============================================================
# File: performance/gpu_info.py
# Author: Samira Babalou
# Date: 2026-01-16
# Purpose:
#   Collect GPU/CUDA metadata and save it reproducibly
#   Includes:
#     - Device name
#     - Vendor
#     - CUDA runtime version
#     - CuPy version
#     - Total GPU memory (MB)
# ============================================================


import json
import os

# ---------------- Paths ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(BASE_DIR, "performance", "gpu_metadata.json")

# ---------------- Initialize metadata ----------------
info = {
    "gpu_available": False,
    "device_name": None,
    "vendor": None,
    "cuda_version": None,      # renamed for pytest compatibility
    "cupy_version": None,
    "gpu_memory_mb": None,     # total GPU memory
}

# ---------------- Collect GPU info ----------------
try:
    import cupy as cp

    info["gpu_available"] = True
    info["cupy_version"] = cp.__version__

    # CUDA version as major.minor
    cuda_ver_int = cp.cuda.runtime.runtimeGetVersion()
    major = cuda_ver_int // 1000
    minor = (cuda_ver_int % 1000) // 10
    info["cuda_version"] = f"{major}.{minor}"

    device = cp.cuda.Device(0)
    attrs = device.attributes

    # Device name (fallback to vendor + compute capability)
    name = attrs.get("Name")
    if not name:
        vendor_id = attrs.get("pciVendorId", 0)
        compute_cap = device.compute_capability
        vendor_map = {4318: "NVIDIA", 4098: "AMD"}
        vendor_name = vendor_map.get(vendor_id, "UnknownVendor")
        name = f"{vendor_name}-GPU CC{compute_cap[0]}.{compute_cap[1]}"
        info["vendor"] = vendor_name
    info["device_name"] = name

    # GPU memory (MB) — safe for WSL/Linux
    try:
        mem_total = device.mem_info.total / (1024**2)
        info["gpu_memory_mb"] = int(mem_total)
    except Exception:
        info["gpu_memory_mb"] = None

except Exception as e:
    info["error"] = str(e)

# ---------------- Save JSON ----------------
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w") as f:
    json.dump(info, f, indent=2)

print(f"GPU metadata written to {OUTPUT_PATH}")

