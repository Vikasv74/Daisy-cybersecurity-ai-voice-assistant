# Use a light, official Python runtime base image
FROM python:3.12-slim

# Install system-level architecture dependencies for sound, networking, and compilation
RUN apt-get update && apt-get install -y \
    ffmpeg \
    espeak-ng \
    nmap \
    tshark \
    build-essential \
    portaudio19-dev \
    libasound2-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up the working directory inside the container
WORKDIR /app

# Copy the requirements file first to optimize Docker layer caching
COPY requirements.txt .

# Install the exact Python tool libraries needed for the project modules
RUN pip install --no-cache-dir -r requirements.txt

# Copy over the entire project structure from the host VM
COPY . .

# Expose port 8501 for the Streamlit UI hub dashboard 
EXPOSE 8501

# Run the Streamlit interface dashboard by default when the container launches
CMD ["streamlit", "run", "ui/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
