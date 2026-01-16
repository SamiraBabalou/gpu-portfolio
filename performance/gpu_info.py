# ============================================================
# File: performance/gpu_info.py
# Purpose:
#   Collect GPU/CUDA metadata and save it reproducibly
# ============================================================

import json
import os

# Always resolve paths relative to repo root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(BASE_DIR, "performance", "gpu_metadata.json")

info = {
    "gpu_available": False,
    "device_name": None,
    "cuda_runtime_version": None,
    "cupy_version": None,
}

try:
    import cupy as cp

    info["gpu_available"] = True
    info["cupy_version"] = cp.__version__
    info["cuda_runtime_version"] = cp.cuda.runtime.runtimeGetVersion()

    device = cp.cuda.Device(0)
    info["device_name"] = device.attributes.get("Name", "Unknown GPU")

except Exception as e:
    info["error"] = str(e)

with open(OUTPUT_PATH, "w") as f:
    json.dump(info, f, indent=2)

print(f"GPU metadata written to {OUTPUT_PATH}")
