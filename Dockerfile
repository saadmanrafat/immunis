# Use the official Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY immunis ./immunis

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Expose the port Cloud Run will use
EXPOSE 8080

# Run the server using uvicorn
# Cloud Run sets the PORT environment variable
CMD ["uv", "run", "uvicorn", "immunis.server:app", "--host", "0.0.0.0", "--port", "8080"]
