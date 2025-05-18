FROM python:3.10-slim

# System dependencies
RUN apt-get update && \
    apt-get install -y git curl build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install LibreTranslate
RUN git clone https://github.com/LibreTranslate/LibreTranslate.git /libretranslate
WORKDIR /libretranslate
RUN pip install -r requirements.txt
RUN python3 scripts/download-models.py --langs en ar

# Install your app dependencies
WORKDIR /app
COPY chatbot_mvp/requirements.txt .
RUN pip install -r requirements.txt

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
CMD bash -c "cd /libretranslate && python3 app.py & cd /app && streamlit run app.py --server.port 7860 --server.enableXsrfProtection false"
