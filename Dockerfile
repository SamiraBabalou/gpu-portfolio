# Use NVIDIA CUDA base image
FROM nvidia/cuda:12.2.0-base-ubuntu22.04

# Author & purpose
LABEL author="Samira Babalou"
LABEL purpose="GPU portfolio for CUDA experiments"

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip git build-essential && \
    pip3 install --upgrade pip matplotlib numpy jupyter

# Create a non-root user
RUN useradd -ms /bin/bash samira
USER samira
WORKDIR /workspace

# Copy repo contents
COPY . /workspace

# Expose Jupyter port
EXPOSE 8888

# Start Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--no-browser"]
