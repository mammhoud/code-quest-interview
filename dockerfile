# Use the official Python 3.10 image based on Alpine Linux
FROM python:3.10-alpine

# Set environment variables to prevent Python from writing .pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

# Create and set the working directory
WORKDIR /app

# Copy your application files into the container
COPY . /app

# Install Python dependencies
RUN pip install pipx
RUN pipx install uv

# Command to run your application (replace 'app.py' with your script)
CMD ["run.sh"]
