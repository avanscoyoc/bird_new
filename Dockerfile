# Use Python 3.10.12 as base image
FROM python:3.10.12

# Set the working directory inside the container
WORKDIR /app

# Copy everything into the container
COPY . /app

# Create and activate a virtual environment (optional but recommended)
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command to run Jupyter Notebook (change if running a script)
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root"]

