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
# ============================================================

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import os
import json

# ---------------- Paths ----------------
# Output PDF file
output_pdf = "reports/performance_report.pdf"

# Path to performance figure
figure_path = "reports/figures/vector_add_performance.png"

# GPU metadata JSON file
gpu_metadata_path = "performance/gpu_metadata.json"

# ---------------- Create canvas ----------------
c = canvas.Canvas(output_pdf, pagesize=A4)
width, height = A4

# ---------------- Title ----------------
c.setFont("Helvetica-Bold", 16)
c.drawString(2*cm, height - 2*cm, "GPU Vector Addition Performance Report")

# ---------------- Main Text ----------------
c.setFont("Helvetica", 11)
text = c.beginText(2*cm, height - 3.5*cm)

# Experiment description
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

# ---------------- GPU Environment ----------------
text.textLine("")
text.textLine("GPU Environment:")

# Load GPU metadata if available
if os.path.exists(gpu_metadata_path):
    with open(gpu_metadata_path) as f:
        gpu_info = json.load(f)

    if gpu_info.get("gpu_available"):
        text.textLine(f"  GPU Device: {gpu_info.get('device_name')}")
        text.textLine(f"  CUDA Runtime Version: {gpu_info.get('cuda_runtime_version')}")
        text.textLine(f"  CuPy Version: {gpu_info.get('cupy_version')}")
    else:
        text.textLine("  GPU not available. CPU fallback used.")
else:
    text.textLine("  GPU metadata not found.")

# Draw the text on the PDF
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
