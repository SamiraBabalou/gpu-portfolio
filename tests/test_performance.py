# ----------------------------------------------------------------------
# File: test_performance.py
# Author: Samira Babalou
# Date: 2026-01-16
# Purpose: Unit tests for performance scripts
# ----------------------------------------------------------------------

import os
import json

def test_performance_results_exists():
    assert os.path.exists("performance/performance_results.txt"), \
        "performance_results.txt should exist"

def test_gpu_metadata_exists():
    assert os.path.exists("performance/gpu_metadata.json"), \
        "gpu_metadata.json should exist"

def test_plot_exists():
    assert os.path.exists("reports/figures/vector_add_performance.png"), \
        "Performance plot PNG should exist"

def test_gpu_metadata_json_format():
    with open("performance/gpu_metadata.json") as f:
        data = json.load(f)
    assert "device_name" in data, "GPU metadata must include device_name"
    assert "cuda_version" in data, "GPU metadata must include cuda_version"
