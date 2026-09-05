# Use an official lightweight Python image  
FROM python:3.14.7-slim-trixie  
   
# Set the working directory  
WORKDIR /app  
    
# Copy project files into the container  
COPY . /app  
   
# Install dependencies  
RUN pip install -r requirements.txt
RUN apt update && apt install sqlite3   
# Expose port 5000 for Flask  
EXPOSE 5000     
# Command to run the app  
CMD ["python3", "app.py"]
