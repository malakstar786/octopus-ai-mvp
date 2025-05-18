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
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your app code and data
COPY app.py .
COPY detector.py .
COPY knowledge_base.py .
COPY translator.py .
COPY data/ ./data/
COPY .streamlit ./.streamlit

# Expose Streamlit port
EXPOSE 7860

# Set environment variables
ENV LIBRETRANSLATE_HOST="localhost"
ENV LIBRETRANSLATE_PORT="5001"

# Expose both LibreTranslate and Streamlit ports
EXPOSE 5001 7860

# Start LibreTranslate in the background, then Streamlit
CMD bash -c "cd /libretranslate && python3 app.py --host 0.0.0.0 --port 5001 & cd /app && streamlit run app.py --server.port 7860 --server.enableXsrfProtection false"
