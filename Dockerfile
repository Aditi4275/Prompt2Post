FROM ghcr.io/astral-sh/uv:python3.12-alpine

# Install system dependencies
RUN apk add --no-cache ffmpeg git ttf-dejavu


# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Copy source code
COPY . .

# Build arguments
ARG OPENROUTER_API_KEY

# Expose port
EXPOSE 8501

# Run the application
CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
