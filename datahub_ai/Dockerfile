# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY ./datahub_ai/requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the current directory contents into the container
COPY ./datahub_ai .

# Copy the .env file into the container
COPY .env .


# Expose the port on which the Flask app will run
EXPOSE 8001

# Run the Flask app when the container starts
CMD ["python", "-m", "datahub_ai.api.llm_query_engine_api"]
