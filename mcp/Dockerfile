# Dockerfile for Google Maps MCP Server on Cloud Run
FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV HOST=0.0.0.0
ENV FASTMCP_HOST=0.0.0.0
ENV FASTMCP_PORT=8080

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY server.py .

# Expose container port
EXPOSE 8080

# Command to run the MCP Server
CMD ["python", "server.py"]
