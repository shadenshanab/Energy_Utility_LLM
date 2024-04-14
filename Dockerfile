FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

## Install system dependencies for GUI applications
#RUN apt-get update && apt-get install -y \
#    libglib2.0-0 \
#    libsm6 \
#    libxrender1 \
#    libxext6 \
#    x11-apps

# Install Python dependencies including the Markdown dependencies for `unstructured`
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "unstructured[md]"

EXPOSE 8080

ENV NAME World

CMD ["python", "main.py"]
