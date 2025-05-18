# Product Requirements Document (PRD)

## Project Overview

**Project Title:**  
Multilingual AI Chatbot MVP for Customer Support (Arabic ↔ English)

**Goal:**  
Build and deploy a lightweight, robust chatbot MVP that detects the user's language (Arabic or English), translates Arabic queries to English using LibreTranslate, fetches answers from a simple knowledge base (KB), and returns the response in the user's original language.

**Primary Users:**  
Arabic-speaking customers using Octopus AI's customer support platform/bot.

**Deployment Scope (Phase 1):**  
- Host chatbot locally via Streamlit.
- Run LibreTranslate locally via Docker.
- Provide an interactive chatbot URL to demonstrate functionality.
- Plan to later host LibreTranslate on Render or another VPS for production.

---

## 🛠️ Tech Stack

### 1. Frontend
- **Framework**: Streamlit  
  - For rapid UI prototyping and MVP deployment via a simple web interface.

### 2. Backend
- **Language**: Python 3.10+
  - Simple syntax, robust libraries, and fast prototyping.
- **Framework**: None (lightweight script-based backend using functions only)
  - Keeps code minimal and easy to integrate into other systems like Octopus.

### 3. Language Detection & Translation
- **Library**: `langdetect`  
  - For detecting if the user input is Arabic or English.
- **Translation API**: [LibreTranslate](https://libretranslate.com) (self-hosted)
  - Fast, open-source, cost-free translation between Arabic and English.
  - Localhost during MVP, will be hosted on cloud (e.g., Render) later.

### 4. Knowledge Base
- **Initial MVP**: In-memory QA pairs (Python dictionary or JSON file)
- **Future Upgrade**: 
  - Vector DB (e.g., FAISS, ChromaDB) + Embedding model (OpenAI, HuggingFace)
  - Could integrate with existing support ticket systems or Octopus KB.

### 5. Deployment
- **Local**: Streamlit app run via `streamlit run`
- **Cloud (Planned)**: Streamlit Cloud, Render, or Hugging Face Spaces
  - LibreTranslate to be hosted on Render or any Docker-compatible cloud.

### 6. Integrations
- **Future**: Expose core translation and chatbot logic as REST API or Python module
  - Easy plug-in for Octopus or other customer service backends.

---

## Core Functionalities

### 1. Language Detection
- Automatically detect if user input is in Arabic or English.
- If Arabic, translate to English before processing.

### 2. Translation System
- Use LibreTranslate (locally hosted via Docker for MVP).
- Translate:
  - Arabic → English (input preprocessing)
  - English → Arabic (response postprocessing)

### 3. Query Processing
- Search a knowledge base (e.g., dictionary or JSON file) using basic keyword match.
- If match found, return the mapped answer.
- If no match, respond with default fallback message.

### 4. User Interaction (UI)
- Chat-like interface using Streamlit.
- Input field for text queries.
- Display both user messages and AI responses in proper language.

### 5. Integrability
- All logic is modular (language detection, translation, KB query) and exposed via clean function calls.
- Easy to extract core logic into a backend microservice for Octopus later.

---

## Website Layout (Streamlit)

### Streamlit Page Sections

```

---

## |          Multilingual AI Chatbot MVP         |

\|  🗨️  Type your question below:                |
\|  \[\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_] \[Submit]   |
-----------------------------------------------------------------------------------

\| Conversation History:                        |
\|                                               |
\| 👤 You: كم عدد أيام الشحن؟                    |
\| 🤖 Bot: The shipping time is usually 3 days.  |
\| 🤖 Bot (Arabic): عادة ما تكون مدة الشحن 3 أيام |
---------------------------------------------------

````

### Streamlit Components
- `st.title()` → "Multilingual AI Chatbot MVP"
- `st.text_input()` → For user query
- `st.button()` → Submit
- `st.session_state` → Track conversation history

---

## API Docs

These describe the internal API contracts between components, especially important once you extract to backend services.

### `/translate`
**Description:** Translate a string between Arabic and English  
**Method:** `POST`  
**URL:** `http://localhost:5000/translate` (LibreTranslate)

**Request JSON:**
```json
{
  "q": "مرحبا",
  "source": "ar",
  "target": "en",
  "format": "text"
}
````

**Response JSON:**

```json
{
  "translatedText": "Hello"
}
```

---

### `get_answer(query: str) → str`

**Description:** Searches for an appropriate answer in the KB based on keywords.

**Input:**

* `query` — string (assumed to be in English)

**Output:**

* `response` — string answer

**Logic:**
Simple keyword mapping or fallback to default.

---

### `detect_language(text: str) → str`

**Description:** Identifies if input is Arabic or English.

**Return:** `"en"` or `"ar"`
**Logic:** Unicode range match for Arabic characters.

---

### `handle_query(input_text: str) → str`

Main handler that:

1. Detects language
2. Translates if needed
3. Queries KB
4. Translates back if needed

Used inside `app.py` for UI interaction.

---

## File/Folder Structure

```
octopus-ai-mvp/
├── chatbot_mvp
│   ├── __pycache__
│   │   ├── detector.cpython-312.pyc
│   │   ├── knowledge_base.cpython-312.pyc
│   │   └── translator.cpython-312.pyc
│   ├── app.py
│   ├── data
│   │   └── kb.json
│   ├── detector.py
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── knowledge_base.py
│   ├── requirements.txt
│   └── translator.py
├── instructions
│   └── instructions.md
└── README.md
```
