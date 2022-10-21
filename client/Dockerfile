# Start from the official Python base image.
FROM python:3.9

# Expose port
EXPOSE 8501

# Set the current working directory to /app.
WORKDIR /app

# Copy the file with the requirements to the /app directory.
COPY ./requirements.txt /app/requirements.txt

# Install the package dependencies in the requirements file.
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the current directory inside the /app directory.
COPY . /app

# Set the command to run the streamlit app.
ENTRYPOINT ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]