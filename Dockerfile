FROM libretranslate/libretranslate:latest AS libretranslate

# Start with a clean Python image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Copy LibreTranslate from the official image
COPY --from=libretranslate /app /libretranslate

# Install the app's dependencies
WORKDIR /app
COPY chatbot_mvp/requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the app code and data
COPY chatbot_mvp/app.py .
COPY chatbot_mvp/detector.py .
COPY chatbot_mvp/knowledge_base.py .
COPY chatbot_mvp/translator.py .
COPY chatbot_mvp/data/ ./data/

# Create .streamlit directory and add config
RUN mkdir -p .streamlit
RUN echo '[server]\nenableXsrfProtection = false' > .streamlit/config.toml

# Expose required ports
EXPOSE 5000 7860

# Start LibreTranslate in the background, then the Streamlit app
CMD bash -c "cd /libretranslate && python3 app.py --host 0.0.0.0 --port 5000 & cd /app && streamlit run app.py --server.port 7860 --server.enableXsrfProtection false"
