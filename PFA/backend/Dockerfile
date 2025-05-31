# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

ENV FLASK_INTERNAL_PORT=5000

# Run gunicorn (a production-ready WSGI HTTP server)
# You might need to install gunicorn in your requirements.txt
# e.g., requirements.txt:
# Flask
# gunicorn
CMD gunicorn -b 0.0.0.0:${FLASK_INTERNAL_PORT} app:app