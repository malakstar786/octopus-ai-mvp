FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Install LibreTranslate via pip
RUN pip install --upgrade pip && \
    pip install libretranslate

# Set up the app
WORKDIR /app

# Install app dependencies
COPY chatbot_mvp/requirements.txt .
RUN pip install -r requirements.txt

# Copy the app code and data
COPY chatbot_mvp/app.py .
COPY chatbot_mvp/detector.py .
COPY chatbot_mvp/knowledge_base.py .
COPY chatbot_mvp/translator.py .
COPY chatbot_mvp/data/ ./data/

# Create .streamlit directory and add config
RUN mkdir -p .streamlit
RUN echo '[server]\nenableXsrfProtection = false' > .streamlit/config.toml

# Set environment variables
ENV LIBRETRANSLATE_HOST="localhost"
ENV LIBRETRANSLATE_PORT="5001"

# Expose required ports
EXPOSE 5001 7860

# Download LibreTranslate models - based on confirmed working command format
RUN libretranslate --update-models --load-only en,ar

# Start LibreTranslate in the background, then the Streamlit app
CMD bash -c "libretranslate --host 0.0.0.0 --port 5001 --load-only en,ar & streamlit run app.py --server.port 7860 --server.enableXsrfProtection false"
