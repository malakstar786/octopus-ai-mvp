FROM python:3.10-slim

# System dependencies
RUN apt-get update && \
    apt-get install -y git curl build-essential && \
    rm -rf /var/lib/apt/lists/*

# Clone LibreTranslate and install its dependencies
RUN git clone --depth 1 https://github.com/LibreTranslate/LibreTranslate.git /libretranslate && \
    cd /libretranslate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    python3 scripts/download-models.py --langs en ar

# Install your app dependencies
WORKDIR /app
COPY chatbot_mvp/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy your app code and data
COPY chatbot_mvp/app.py .
COPY chatbot_mvp/detector.py .
COPY chatbot_mvp/knowledge_base.py .
COPY chatbot_mvp/translator.py .
COPY chatbot_mvp/data/ ./data/

# Create .streamlit directory and add config
RUN mkdir -p .streamlit
RUN echo '[server]\nenableXsrfProtection = false' > .streamlit/config.toml

# Expose Streamlit port
EXPOSE 7860

# Start LibreTranslate in the background, then Streamlit
# Note: LibreTranslate's app.py will run on its default port 5000
CMD bash -c "cd /libretranslate && python3 app.py & cd /app && streamlit run app.py --server.port 7860 --server.enableXsrfProtection false"
