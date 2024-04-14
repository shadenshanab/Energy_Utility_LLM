FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

# Install Python dependencies including the Markdown dependencies for `unstructured`
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "unstructured[md]"

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Command to run on container start
CMD ["python", "main.py"]
