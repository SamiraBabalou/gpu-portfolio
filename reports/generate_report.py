# ============================================================
# File: reports/generate_report.py
# Author: Samira Babalou
# Date: 2026-01-16
# Purpose:
#   Generate a PDF report for CPU vs GPU vector addition
#   Includes:
#     - Performance observations
#     - Figure(s) of results
#     - GPU environment metadata
#     - Unit test verification status
# ============================================================

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import os
import json
import subprocess

# ---------------- Paths ----------------
output_pdf = "reports/performance_report.pdf"
figure_path = "reports/figures/vector_add_performance.png"
gpu_metadata_path = "performance/gpu_metadata.json"

# Ensure output folder exists
os.makedirs(os.path.dirname(output_pdf), exist_ok=True)

# ---------------- Create canvas ----------------
c = canvas.Canvas(output_pdf, pagesize=A4)
width, height = A4

# ---------------- Title ----------------
c.setFont("Helvetica-Bold", 16)
c.drawString(2*cm, height - 2*cm, "GPU Vector Addition Performance Report")

# ---------------- Main Text ----------------
c.setFont("Helvetica", 11)
text = c.beginText(2*cm, height - 3.5*cm)

text.textLine("Experiment: CPU vs GPU vector addition using NumPy and CuPy")
text.textLine("")

# Observations
text.textLine(
    "Observation: GPU acceleration does not outperform CPU for moderate vector sizes."
)
text.textLine(
    "Reason: kernel launch overhead and host-device memory transfer dominate computation."
)
text.textLine("")
text.textLine(
    "Conclusion: GPUs provide benefits when workload size is large enough to amortize overhead."
)
text.textLine("")

# ---------------- GPU Environment ----------------
text.textLine("GPU Environment:")

if os.path.exists(gpu_metadata_path):
    with open(gpu_metadata_path) as f:
        gpu_info = json.load(f)

    if gpu_info.get("gpu_available"):
        gpu_mem = gpu_info.get("gpu_memory_mb")
        gpu_mem_str = f"{gpu_mem} MB" if gpu_mem is not None else "Unknown"

        cuda_ver = gpu_info.get("cuda_version", "Unknown")
        cupy_ver = gpu_info.get("cupy_version", "Unknown")

        text.textLine(f"  GPU Device: {gpu_info.get('device_name', 'Unknown')}")
        text.textLine(f"  GPU Memory: {gpu_mem_str}")
        text.textLine(f"  CUDA Version: {cuda_ver}")
        text.textLine(f"  CuPy Version: {cupy_ver}")
    else:
        text.textLine("  GPU not available. CPU fallback used.")
else:
    text.textLine("  GPU metadata not found.")


# ---------------- Unit Tests Verification ----------------
text.textLine("Unit Test Verification:")

try:
    # Run pytest in quiet mode and capture status
    result = subprocess.run(
        ["pytest", "tests/", "--maxfail=1", "--disable-warnings", "-q"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        text.textLine("  All unit tests passed successfully ✅")
    else:
        text.textLine("  Some unit tests failed ❌")
        text.textLine(f"  See pytest output for details.")
except Exception as e:
    text.textLine(f"  Could not run unit tests: {e}")

# Draw the text on PDF
c.drawText(text)

# ---------------- Add Figure ----------------
if os.path.exists(figure_path):
    c.drawImage(
        figure_path,
        2*cm,
        3*cm,
        width=17*cm,
        preserveAspectRatio=True,
        mask="auto"
    )

# Finish PDF
c.showPage()
c.save()

print(f"PDF report generated: {output_pdf}")
