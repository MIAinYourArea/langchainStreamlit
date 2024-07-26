# Use the official Python image from the Docker hub
FROM python:3.8-slim

# Set the working directory in the container
RUN mkdir /langchain
WORKDIR /langchain

# Copy the content of the local src directory to the working directory
ADD . /langchain

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt
 
# Streamlit uses port 8501
EXPOSE 8501


# Command to run on container start
ENTRYPOINT ["streamlit", "run", "src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]