import requests
import json
import time
import os
import sys

# LibreTranslate endpoint
# Always use localhost for internal container communication
LIBRETRANSLATE_HOST = "localhost"  # Fixed to localhost for internal communication
LIBRETRANSLATE_PORT = os.environ.get("LIBRETRANSLATE_PORT", "5000")  # LibreTranslate's default port
LIBRETRANSLATE_URL = f"http://{LIBRETRANSLATE_HOST}:{LIBRETRANSLATE_PORT}/translate"

# Print connection details on startup
print(f"[TRANSLATOR] Configured to connect to LibreTranslate at: {LIBRETRANSLATE_URL}", file=sys.stderr)
print(f"[TRANSLATOR] Environment variables: PORT={os.environ.get('PORT')}, LIBRETRANSLATE_PORT={os.environ.get('LIBRETRANSLATE_PORT')}", file=sys.stderr)

def check_libretranslate_connection():
    """
    Check if LibreTranslate is running and responding.
    
    Returns:
        bool: True if LibreTranslate is accessible, False otherwise
    """
    try:
        # Try to connect to LibreTranslate
        print(f"[TRANSLATOR] Trying to connect to LibreTranslate at {LIBRETRANSLATE_HOST}:{LIBRETRANSLATE_PORT}", file=sys.stderr)
        response = requests.get(f"http://{LIBRETRANSLATE_HOST}:{LIBRETRANSLATE_PORT}/languages", timeout=5)
        print(f"[TRANSLATOR] Connection successful: {response.status_code}", file=sys.stderr)
        return response.status_code == 200
    except requests.exceptions.ConnectionError as e:
        print(f"[TRANSLATOR] Connection error to LibreTranslate at {LIBRETRANSLATE_HOST}:{LIBRETRANSLATE_PORT}: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[TRANSLATOR] Unexpected error connecting to LibreTranslate: {e}", file=sys.stderr)
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
            print(f"[TRANSLATOR] Attempt {attempt+1}: Sending translation request to {LIBRETRANSLATE_URL}", file=sys.stderr)
            response = requests.post(LIBRETRANSLATE_URL, json=data, timeout=10)
            
            # Check if request was successful
            if response.status_code == 200:
                result = response.json()
                return result["translatedText"]
            else:
                print(f"[TRANSLATOR] Translation error (attempt {attempt+1}/{max_retries}): {response.text}", file=sys.stderr)
                if attempt < max_retries - 1:
                    # Wait before retrying
                    time.sleep(1)
        except Exception as e:
            print(f"[TRANSLATOR] Translation error (attempt {attempt+1}/{max_retries}): {str(e)}", file=sys.stderr)
            if attempt < max_retries - 1:
                # Wait before retrying
                time.sleep(1)
    
    # Return original text if all attempts fail
    print(f"[TRANSLATOR] Translation failed after {max_retries} attempts. Returning original text.", file=sys.stderr)
    return text 