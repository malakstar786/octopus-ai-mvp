FROM python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git build-essential wget libxml2-dev libxslt1-dev zlib1g-dev \
    libffi-dev libjpeg-dev libpng-dev libopenblas-dev liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pip packages with increased timeout and split into separate steps to avoid timeout
RUN pip install --upgrade pip

# Install torch separately with increased timeout
RUN pip install --timeout=600 torch==2.2.0

# Install LibreTranslate without dependencies for faster install
RUN pip install --no-deps libretranslate

# Now install the remaining dependencies but exclude torch
RUN pip install --timeout=300 appdirs==1.4.4 apscheduler==3.9.1 argos-translate-files==1.2.0 \
    argostranslate==1.9.6 expiringdict==1.2.2 flask-babel==3.1.0 flask-limiter==2.6.3 \
    flask-session==0.4.0 flask-swagger-ui==4.11.1 flask-swagger==0.2.14 flask==2.2.5 \
    itsdangerous==2.1.2 langdetect==1.0.9 lexilang==1.0.4 morfessor==2.0.6 numpy<2 \
    packaging==23.1 polib==1.1.1 prometheus-client==0.15.0 redis==4.4.4 requests==2.31.0 \
    translatehtml==1.5.2 waitress==2.1.2 werkzeug==2.3.8 sentencepiece==0.2.0 ctranslate2<5,>=4.0

# Work directory for your app
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your app files
COPY . .

# Set Streamlit config
RUN mkdir -p ~/.streamlit
COPY .streamlit/config.toml ~/.streamlit/config.toml

# Expose the Streamlit port
EXPOSE 8501

# Run LibreTranslate + Streamlit at runtime (NOT during build)
# Use JSON format to properly handle signals
CMD ["sh", "-c", "libretranslate --update-models --load-only en,ar & streamlit run chatbot_mvp/app.py --server.port=8501 --server.address=0.0.0.0"]
