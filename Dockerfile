# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python application and requirements file to the container
COPY ./ /app/
COPY requirements.txt /app/

# Install any necessary dependencies
RUN pip install -r requirements.txt

# Expose the port that your Flask application will run on (replace 5000 with your desired port)
EXPOSE 5000

# Define the command to run your Flask application
CMD ["python", "main.py"]