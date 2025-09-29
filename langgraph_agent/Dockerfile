FROM python:3.12.5-slim

WORKDIR /app

# Copy only the necessary files
# COPY requirements.txt .
COPY pyproject.toml .
COPY src/ src/
COPY langgraph.json .

# Install dependencies
RUN pip install --no-cache-dir -e .[dev]

# Expose the port that langgraph will run on
EXPOSE 2024

# Start langgraph with the specified settings
CMD ["langgraph", "dev", "--allow-blocking", "--host", "0.0.0.0"] 