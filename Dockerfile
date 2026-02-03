# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK VADER lexicon
RUN python -m nltk.downloader vader_lexicon

# Expose port for Streamlit dashboard
EXPOSE 8501

# Set environment variable for Streamlit
ENV STREAMLIT_SERVER_HEADLESS=true

# Run the entrypoint
CMD ["python", "entrypoint.py"]
