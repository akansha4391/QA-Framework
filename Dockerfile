# Use specific version for stability (matches project python requirement)
FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy

# Set working directory
WORKDIR /app

# Prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies if any additional needed (Playwright image covers most)
RUN apt-get update && apt-get install -y \
    vim \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20.x (LTS) for Documentation Site
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && \
    apt-get install -y nodejs && \
    node -v && npm -v

# Copy configuration files first for better caching
COPY pyproject.toml .

# Install dependencies
# Using --no-cache-dir to keep image small
RUN pip install --no-cache-dir -e .[dev]

# Install Playwright browsers (if not using the pre-baked playwright image, 
# but since we are, we just need to ensure the python bindings match)
# The base image already has browsers in /ms-playwright
# We check if we need to install anything else
RUN python -m playwright install --with-deps

# Copy the rest of the application
COPY . .

# Install Documentation Dependencies (if docs-site exists)
RUN if [ -d "docs-site" ]; then \
    cd docs-site && \
    npm install; \
    fi

# Expose ports for Docusaurus (3000)
EXPOSE 3000

# Set the entrypoint to a shell or your CLI tool
ENTRYPOINT ["/bin/bash"]
