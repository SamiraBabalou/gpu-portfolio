#!/bin/bash
# ----------------------------------------------------------------------
# File: run_notebooks.sh
# Author: Samira Babalou
# Purpose: Execute Jupyter notebooks for GPU portfolio
# Notes:
#   - Uses the 'gpu-portfolio' Jupyter kernel
#   - Works inside Docker and in CI pipelines
# ----------------------------------------------------------------------

# Exit immediately if any command fails
set -e

# Array of notebook paths to execute
NOTEBOOKS=("notebooks/vector_addition.ipynb")

# Loop through notebooks and execute each
for nb in "${NOTEBOOKS[@]}"; do
    echo "Running notebook: $nb"
    jupyter nbconvert \
        --to notebook \
        --execute "$nb" \
        --ExecutePreprocessor.kernel_name=gpu-portfolio \
        --inplace   
done

echo "All notebooks executed successfully."
