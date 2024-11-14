# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app
# Copying all files to /app
COPY requirements.txt /app
COPY ./inputs /app/inputs
COPY ./outputs /app/outputs
COPY main.py /app
COPY first_seminar.py /app


RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
# Install any needed dependencies specified in requirements.txt
RUN pip install -r requirements.txt


# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["fastapi", "run", "main.py", "--port", "80"]