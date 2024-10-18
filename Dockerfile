# Use an official Python runtime as a parent image
FROM python:3.12.3

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY ./requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the relevant folders into the container
COPY ./arm /app/arm
COPY ./database_prod /app/database_prod
COPY ./imm /app/imm
COPY ./market /app/market
COPY ./pricer /app/pricer
COPY ./startServers.py /app

# Expose the port (5000 in this case)
EXPOSE 5000
EXPOSE 5001
EXPOSE 5002
EXPOSE 5003
EXPOSE 5004

ENV FLASK_RUN_HOST=0.0.0.0

# Define the command to run your app
CMD ["python", "startServers.py"]
