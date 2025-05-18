---
title: Multilingual AI Chatbot MVP
emoji: "🤖"
colorFrom: indigo
colorTo: blue
sdk: docker
app_file: app.py
pinned: false
---


# Multilingual AI Chatbot MVP

A multilingual chatbot supporting English and Arabic, using LibreTranslate for translations.

## Features

- Supports both English and Arabic
- Automatic language detection
- Uses LibreTranslate for translation services
- Simple and intuitive UI with Streamlit

## Running Locally

### Option 1: Using Docker Compose (Recommended)

The easiest way to run the application is with Docker Compose, which will set up both the Streamlit app and LibreTranslate service:

1. Make sure you have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed

2. Clone this repository:
   ```
   git clone <repository-url>
   cd octopus-ai-mvp
   ```

3. Build and start the containers:
   ```
   docker-compose up --build
   ```

4. Access the application at [http://localhost:8501](http://localhost:8501)

### Option 2: Running Components Separately

If you prefer to run the components separately:

#### Step 1: Run LibreTranslate

Run LibreTranslate using Docker:
```
docker run -p 5000:5000 -e LT_LOAD_ONLY=en,ar libretranslate/libretranslate
```

#### Step 2: Install Python Dependencies

```
pip install -r requirements.txt
```

#### Step 3: Run the Streamlit App

```
streamlit run chatbot_mvp/app.py
```

## Deployment

The application is configured for deployment on Render using the provided `render.yaml` configuration file.

## Project Structure

```
chatbot-mvp/
├── chatbot_mvp/
│   ├── app.py           # Main Streamlit application
│   ├── detector.py      # Language detection
│   ├── knowledge_base.py # Knowledge base for responses
│   ├── translator.py    # Translation services
│   └── data/
│       └── kb.json      # Knowledge base data
├── .streamlit/
│   └── config.toml      # Streamlit configuration
├── requirements.txt     # Python dependencies
├── Dockerfile           # For single container setup
├── Dockerfile.streamlit # For multi-container setup
├── docker-compose.yml   # Multi-container setup
└── render.yaml          # Render deployment configuration
```

## Troubleshooting

If you encounter issues with LibreTranslate connection:

1. Ensure the LibreTranslate service is running and accessible
2. Check that the environment variables are set correctly
3. For Docker, make sure that containers can communicate with each other 