# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the web application files into the container
COPY app.py /app/
COPY templates/ /app/templates/

# Install required packages
RUN pip install flask opencv-python-headless pillow
RUN pip install gunicorn


# Install other system dependencies for OpenCV (if needed)
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev

# Expose the web application port
EXPOSE 5000

# Run the web application when the container starts
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
