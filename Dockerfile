FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader vader_lexicon
EXPOSE 8501
ENV STREAMLIT_SERVER_HEADLESS=true
CMD ["python", "entrypoint.py"]
