# Use an official Python runtime as a parent image, specifically the slim version to keep the image size down
FROM python:3.11-slim

# Set the working directory to /app inside the container
WORKDIR /app

# Set environment variable to disable llama-parse to avoid issues
ENV USE_LLAMA_PARSE=0

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt with specific versions that work
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --upgrade llama-parse llama-index pydantic

# Initialize the database
RUN python create_sqlite_db.py

# Create a new start.sh script with proper line endings
RUN echo '#!/bin/bash' > start.sh && \
    echo 'python create_sqlite_db.py' >> start.sh && \
    echo 'python rag_gpt_app.py' >> start.sh && \
    chmod +x start.sh

# Make port 7000 available to the world outside this container
EXPOSE 7000

# Define the command to run on container start
CMD ["./start.sh"]