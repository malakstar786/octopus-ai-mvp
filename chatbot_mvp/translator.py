import requests
import json
import time
import os

# LibreTranslate endpoint
# Use environment variable if set (for containerized environments),
# otherwise fall back to localhost (for local development)
LIBRETRANSLATE_HOST = os.environ.get("LIBRETRANSLATE_HOST", "localhost")
LIBRETRANSLATE_URL = f"http://{LIBRETRANSLATE_HOST}:5000/translate"

def check_libretranslate_connection():
    """
    Check if LibreTranslate is running and responding.
    
    Returns:
        bool: True if LibreTranslate is accessible, False otherwise
    """
    try:
        # Try to connect to LibreTranslate
        response = requests.get(f"http://{LIBRETRANSLATE_HOST}:5000/languages")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print(f"Could not connect to LibreTranslate at {LIBRETRANSLATE_HOST}:5000")
        # Try localhost as a fallback if we're not already using it
        if LIBRETRANSLATE_HOST != "localhost":
            try:
                response = requests.get("http://localhost:5000/languages")
                return response.status_code == 200
            except:
                pass
        return False

def translate_text(text, source, target, max_retries=3):
    """
    Translate text from source language to target language using LibreTranslate.
    
    Args:
        text (str): Text to translate
        source (str): Source language code ('ar' or 'en')
        target (str): Target language code ('ar' or 'en')
        max_retries (int): Maximum number of retries on connection failure
        
    Returns:
        str: Translated text or original text if translation fails
    """
    if not text or text.strip() == "":
        return text
    
    # No need to translate if source and target are the same
    if source == target:
        return text
    
    # Try to translate with retries
    for attempt in range(max_retries):
        try:
            # Prepare request data
            data = {
                "q": text,
                "source": source,
                "target": target,
                "format": "text"
            }
            
            # Send request to LibreTranslate
            response = requests.post(LIBRETRANSLATE_URL, json=data, timeout=10)
            
            # Check if request was successful
            if response.status_code == 200:
                result = response.json()
                return result["translatedText"]
            else:
                print(f"Translation error (attempt {attempt+1}/{max_retries}): {response.text}")
                if attempt < max_retries - 1:
                    # Wait before retrying
                    time.sleep(1)
        except Exception as e:
            print(f"Translation error (attempt {attempt+1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                # Wait before retrying
                time.sleep(1)
    
    # Return original text if all attempts fail
    print(f"Translation failed after {max_retries} attempts. Returning original text.")
    return text 