import json
import os

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
        
        Args:
            query (str): The user's query (in English)
            
        Returns:
            str: The answer from the knowledge base or default response
        """
        # Convert query to lowercase for case-insensitive matching
        query = query.lower()
        
        # Look for keyword matches in the query
        for qa_pair in self.questions:
            keywords = qa_pair.get('keywords', [])
            
            # Check if any keyword is in the query
            if any(keyword.lower() in query for keyword in keywords):
                return qa_pair.get('answer')
        
        # Return default response if no match is found
        return self.default_response 