FROM python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git build-essential wget libxml2-dev libxslt1-dev zlib1g-dev \
    libffi-dev libjpeg-dev libpng-dev libopenblas-dev liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Install LibreTranslate
RUN git clone https://github.com/LibreTranslate/LibreTranslate.git /libretranslate
WORKDIR /libretranslate
RUN pip install --upgrade pip && pip install -r requirements.txt

# Work directory for your app
WORKDIR /app

# Copy your app files
COPY . .

# Set Streamlit config
RUN mkdir -p ~/.streamlit
COPY .streamlit/config.toml ~/.streamlit/config.toml

# Install app dependencies
RUN pip install -r requirements.txt

# Expose the Streamlit port
EXPOSE 8501

# Run LibreTranslate + Streamlit at runtime (NOT during build)
CMD libretranslate --update-models --load-only en,ar & streamlit run chatbot_mvp/app.py --server.port=8501 --server.address=0.0.0.0
