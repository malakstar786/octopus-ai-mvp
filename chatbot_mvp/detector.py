from langdetect import detect, LangDetectException

def detect_language(text):
    """
    Detect if the input text is in Arabic or English.
    
    Args:
        text (str): Input text to detect
        
    Returns:
        str: Language code 'ar' for Arabic, 'en' for English, 'en' as default fallback
    """
    try:
        if not text or text.strip() == "":
            return "en"
        
        # Detect language
        lang = detect(text)
        
        # Return ar or en, default to en for other languages
        if lang == 'ar':
            return 'ar'
        else:
            return 'en'
    except LangDetectException:
        # Default to English if detection fails
        return "en" 