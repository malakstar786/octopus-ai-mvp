import json
import os
import re

class KnowledgeBase:
    def __init__(self, kb_file='data/kb.json'):
        """
        Initialize the knowledge base from a JSON file.
        
        Args:
            kb_file (str): Path to knowledge base JSON file
        """
        self.kb_path = os.path.join(os.path.dirname(__file__), kb_file)
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """Load the knowledge base from the JSON file"""
        try:
            with open(self.kb_path, 'r', encoding='utf-8') as file:
                self.kb_data = json.load(file)
            
            self.questions = self.kb_data.get('questions', [])
            self.default_response = self.kb_data.get('default_response', 
                "I'm sorry, I don't have information about that.")
        except Exception as e:
            print(f"Error loading knowledge base: {str(e)}")
            # Initialize with empty data if file can't be loaded
            self.questions = []
            self.default_response = "I'm sorry, I don't have information about that."
    
    def get_answer(self, query):
        """
        Search for an answer in the knowledge base based on keywords in the query.
        Uses a more sophisticated matching algorithm to handle translations better.
        
        Args:
            query (str): The user's query (in English)
            
        Returns:
            str: The answer from the knowledge base or default response
        """
        if not query or query.strip() == "":
            return self.default_response
            
        # Convert query to lowercase for case-insensitive matching
        query = query.lower()
        
        # Store matches with their score
        matches = []
        
        # Clean query of punctuation for better matching
        cleaned_query = re.sub(r'[^\w\s]', ' ', query)
        query_words = cleaned_query.split()
        
        # Process each QA pair
        for qa_pair in self.questions:
            keywords = qa_pair.get('keywords', [])
            score = 0
            
            # Check for exact matches (highest priority)
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in query:
                    # Exact match gets a high score
                    score += 10
                    break
            
            # If no exact match, check for word-by-word matches
            if score == 0:
                for query_word in query_words:
                    if len(query_word) <= 2:  # Skip very short words
                        continue
                        
                    for keyword in keywords:
                        keyword_lower = keyword.lower()
                        keyword_parts = keyword_lower.split()
                        
                        # Check if the query word is in any of the keyword parts
                        if query_word in keyword_parts or any(query_word in kp for kp in keyword_parts):
                            score += 1
                        # Check if the keyword is in the query word (partial match)
                        elif len(keyword_lower) > 2 and keyword_lower in query_word:
                            score += 1
            
            if score > 0:
                matches.append((score, qa_pair.get('answer')))
        
        # Sort matches by score (highest first)
        matches.sort(reverse=True)
        
        # Return the answer with the highest score, or default if no matches
        if matches:
            return matches[0][1]
        
        return self.default_response 