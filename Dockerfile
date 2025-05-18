FROM python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git build-essential wget libxml2-dev libxslt1-dev zlib1g-dev \
    libffi-dev libjpeg-dev libpng-dev libopenblas-dev liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pip packages with increased timeout
RUN pip install --upgrade pip setuptools wheel

# Install packages in smaller groups to avoid timeout issues
# Group 1: Base packages
RUN pip install --timeout=300 appdirs==1.4.4 apscheduler==3.9.1 requests==2.31.0 numpy<2 packaging==23.1

# Group 2: Flask-related packages
RUN pip install --timeout=300 flask==2.2.5 flask-babel==3.1.0 flask-limiter==2.6.3 \
    flask-session==0.4.0 flask-swagger-ui==4.11.1 flask-swagger==0.2.14 itsdangerous==2.1.2 werkzeug==2.3.8

# Group 3: Translation-related packages
RUN pip install --timeout=300 argos-translate-files==1.2.0 argostranslate==1.9.6 \
    langdetect==1.0.9 lexilang==1.0.4 morfessor==2.0.6 polib==1.1.1 \
    translatehtml==1.5.2 sentencepiece==0.2.0

# Group 4: Server and monitoring
RUN pip install --timeout=300 expiringdict==1.2.2 prometheus-client==0.15.0 \
    redis==4.4.4 waitress==2.1.2

# Group 5: Install torch separately with increased timeout
RUN pip install --timeout=600 torch==2.2.0

# Group 6: Install ctranslate2 with specific version
RUN pip install --timeout=300 "ctranslate2<5,>=4.0"

# Finally install LibreTranslate
RUN pip install --timeout=300 libretranslate

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
