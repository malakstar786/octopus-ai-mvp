import streamlit as st
from detector import detect_language
from translator import translate_text, check_libretranslate_connection
from knowledge_base import KnowledgeBase

# Initialize the knowledge base
kb = KnowledgeBase()

def handle_query(input_text):
    """
    Process the user query: detect language, translate if needed, 
    get answer, and translate back if needed.
    
    Args:
        input_text (str): User's input text
        
    Returns:
        tuple: (original_language, english_query, original_response, translated_response)
    """
    # Detect language
    lang = detect_language(input_text)
    
    # Translate to English if needed
    if lang == 'ar':
        english_query = translate_text(input_text, 'ar', 'en')
    else:
        english_query = input_text
    
    # Get answer from knowledge base
    english_response = kb.get_answer(english_query)
    
    # Translate back to original language if needed
    if lang == 'ar':
        translated_response = translate_text(english_response, 'en', 'ar')
    else:
        translated_response = english_response
    
    return lang, english_query, english_response, translated_response

# Set up the Streamlit app
def main():
    st.set_page_config(page_title="Multilingual AI Chatbot MVP", layout="wide")
    
    # App title
    st.title("Multilingual AI Chatbot MVP")
    
    # Check LibreTranslate connection
    libretranslate_available = check_libretranslate_connection()
    
    if not libretranslate_available:
        st.warning("""
        ⚠️ LibreTranslate service is not available. 
        
        Please make sure LibreTranslate is running at http://localhost:5000.
        
        Arabic translation will not work until LibreTranslate is available.
        See README.md for setup instructions.
        """)
    
    # Initialize session state for storing conversation history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.chat_message('user').write(f"👤 {message['content']}")
        else:
            st.chat_message('assistant').write(f"🤖 {message['content']}")
    
    # Query input
    user_input = st.chat_input("Type your question (Arabic or English):")
    
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({'role': 'user', 'content': user_input})
        
        # Display user message
        st.chat_message('user').write(f"👤 {user_input}")
        
        # Show warning if Arabic input is detected but LibreTranslate is not available
        if not libretranslate_available and detect_language(user_input) == 'ar':
            st.warning("⚠️ Arabic detected but LibreTranslate is not available. Translation may not work properly.")
        
        # Process the query
        with st.spinner("Thinking..."):
            lang, english_query, english_response, translated_response = handle_query(user_input)
            
            # Display bot response
            if lang == 'ar':
                # For Arabic queries, show both English and Arabic responses
                st.chat_message('assistant').write(f"🤖 {english_response}")
                st.chat_message('assistant').write(f"🤖 (Arabic): {translated_response}")
                
                # Store both responses in chat history
                st.session_state.messages.append({'role': 'assistant', 'content': english_response})
                st.session_state.messages.append({'role': 'assistant', 'content': f"(Arabic): {translated_response}"})
            else:
                # For English queries, just show English response
                st.chat_message('assistant').write(f"🤖 {english_response}")
                
                # Store response in chat history
                st.session_state.messages.append({'role': 'assistant', 'content': english_response})

if __name__ == "__main__":
    main() 