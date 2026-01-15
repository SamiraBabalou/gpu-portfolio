## Quickstart

### Using Docker
```bash
# Build Docker image
docker build -t gpu-portfolio .

# Run interactive container
docker run --gpus all -it -p 8888:8888 gpu-portfolio

# Jupyter notebook opens in browser, go to /workspace/notebooks/
````

### Using Conda (local)

```bash
conda env create -f environment.yml
conda activate gpu-portfolio
jupyter notebook
```
