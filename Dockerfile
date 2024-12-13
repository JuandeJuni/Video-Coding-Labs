# Use an official Python runtime as a parent image
FROM python:3.11-slim
# Set environment variables for GUI
ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:0

# Install dependencies
RUN apt-get update && apt-get install -y \
    libxkbcommon-x11-0 \
    libgl1-mesa-glx \
    x11-apps && \
    rm -rf /var/lib/apt/lists/*
# Set the working directory in the container
WORKDIR /app
# Copying all files to /app
# COPY requirements.txt /app
# COPY ./inputs /app/inputs
# COPY ./outputs /app/outputs
# COPY main.py /app
# COPY first_seminar.py /app
COPY . .

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
# Install any needed dependencies specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

# Run app.py when the container launches
# CMD ["fastapi", "run", "main.py", "--port", "80"]