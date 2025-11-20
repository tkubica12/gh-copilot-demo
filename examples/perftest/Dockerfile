FROM grafana/k6:latest

# Set the working directory
WORKDIR /app

# Copy the k6 script and any necessary files
COPY script.js .
COPY example.jpg .

# Command to run the k6 test
ENTRYPOINT ["k6", "run", "/app/script.js"]
