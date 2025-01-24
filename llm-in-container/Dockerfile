# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY ./llm-in-container/requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the current directory contents into the container
COPY ./llm-in-container .

# Copy the .env file into the container
COPY .env .

# Install dependencies
RUN pip install -r requirements.txt


# Expose the port on which the Flask app will run
EXPOSE 8001

# Run tests if RUN_TESTS = true
ARG RUN_TESTS=false
RUN if [ "$RUN_TESTS" = "true" ] ; then pip install pytest && pytest ; fi

# Run the Flask app when the container starts
CMD ["python", "-m", "datahub_ai.api.llm_query_engine_api"]
