# Use a base image with Python
FROM python:3.10.3-slim

# Set the working directory
WORKDIR /app

# Set the environment variable for the port
ENV PORT=8000

# Copy the requirements.txt file and install dependencies
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application into the container
COPY . /app/

# Expose the port that your FastAPI app uses
EXPOSE $PORT

# Command to run the FastAPI application using Uvicorn
# CMD ["uvicorn", "entry_point:app", "--host", "0.0.0.0", "--port", "$PORT"]
CMD sh -c "uvicorn entry_point:app --host 0.0.0.0 --port $PORT"
