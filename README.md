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

A lightweight chatbot MVP that detects a user's language (Arabic or English), processes queries, and responds in the original language.

## Features

- Automatic language detection (Arabic/English)
- Seamless translation using LibreTranslate (open-source language translation)
- Simple knowledge base for customer support queries
- Clean chat interface built with Streamlit

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up LibreTranslate

Using Docker

1. Install Docker if not already installed:
   - [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
   - [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
   - [Docker Engine for Linux](https://docs.docker.com/engine/install/)

2. Run LibreTranslate with Docker:
   ```bash
   docker run -d -p 5000:5000 libretranslate/libretranslate
   ```

   Or with docker-compose:
   ```bash
   docker-compose up -d
   ```


### 3. Run the Streamlit App

```bash
streamlit run app.py
```

This will start the app and open it in your browser (typically at http://localhost:8501).

## Usage

1. Type a question in either Arabic or English
2. The system will:
   - Detect the language
   - Translate to English if needed
   - Find a response from the knowledge base
   - Translate back to Arabic if the original query was in Arabic
   - Display both the English response and the translated response

## Project Structure

- `app.py` - Main Streamlit application
- `detector.py` - Language detection module
- `translator.py` - Translation module using LibreTranslate
- `knowledge_base.py` - Simple knowledge base implementation
- `data/kb.json` - JSON file with QA pairs
- `docker-compose.yml` - Docker configuration for LibreTranslate

## Customizing the Knowledge Base

Edit the `data/kb.json` file to add more questions and answers to the knowledge base. Each entry should have:
- `keywords`: Array of keywords to match in queries
- `answer`: The response to provide when a keyword matches

## Troubleshooting

### LibreTranslate Connection Issues

If you encounter connection issues with LibreTranslate:

1. Verify LibreTranslate is running by visiting http://localhost:5000 in your browser
2. Check if the correct ports are exposed (5000)
3. If using Option B (Python), ensure you have sufficient RAM for the language models 