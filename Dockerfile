FROM python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential wget libxml2-dev libxslt1-dev zlib1g-dev \
    libffi-dev libjpeg-dev libpng-dev libopenblas-dev liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip tools
RUN pip install --upgrade pip setuptools wheel

# Group 1: Base & PyTorch
RUN pip install --no-cache-dir --timeout=600 torch==2.2.0
RUN pip install --no-cache-dir appdirs==1.4.4 apscheduler==3.9.1 requests==2.31.0 'numpy<2' packaging==23.1

# Group 2: Flask & web
RUN pip install --no-cache-dir flask==2.2.5 flask-babel==3.1.0 flask-limiter==2.6.3 \
    flask-session==0.4.0 flask-swagger-ui==4.11.1 flask-swagger==0.2.14 \
    itsdangerous==2.1.2 werkzeug==2.3.8 waitress==2.1.2

# Group 3: Translation & CTranslate
RUN pip install --no-cache-dir argos-translate-files==1.2.0 argostranslate==1.9.6 \
    langdetect==1.0.9 lexilang==1.0.4 morfessor==2.0.6 polib==1.1.1 \
    translatehtml==1.5.2 sentencepiece==0.2.0

RUN pip install --no-cache-dir 'ctranslate2<5,>=4.0'

# Group 4: Remaining dependencies
RUN pip install --no-cache-dir expiringdict==1.2.2 prometheus-client==0.15.0 redis==4.4.4

# Install LibreTranslate
RUN pip install --no-cache-dir libretranslate

# Set work directory
WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Configure Streamlit
RUN mkdir -p ~/.streamlit
RUN mkdir -p .streamlit
COPY .streamlit/config.toml .streamlit/config.toml

# Expose common ports (local dev only)
EXPOSE 5000 8501

# Environment variables (STREAMLIT picks up these automatically)
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# FIXED CMD - without exec to ensure both processes run correctly
CMD ["sh", "-c", "libretranslate --host 0.0.0.0 --port 5000 --update-models --load-only en,ar & sleep 10 && streamlit run chatbot_mvp/app.py --server.port=$PORT --server.address=0.0.0.0"]
