import openai
import time
import logging
from typing import Dict, Optional

class MessageGenerator:
    def __init__(self, api_key: str):
        """Initialize MessageGenerator with OpenAI API key"""
        self.api_key = api_key
        openai.api_key = api_key
        self.max_retries = 3
        self.retry_delay = 1  # seconds
        
    def generate_connection_message(self, profile_data: Dict) -> Optional[str]:
        """Generate a personalized connection message based on profile data"""
        system_prompt = """
        You are a professional tech career mentor. Create personalized LinkedIn connection messages that:
        1. Acknowledge their current role and company
        2. Show understanding of WITCH company work culture
        3. Introduce Super30 as an exclusive MAANG preparation program
        4. Keep it under 300 characters
        5. Be direct and value-focused
        """
        
        company_context = {
            'WIPRO': 'known for its global IT services',
            'INFOSYS': 'a leader in digital services and consulting',
            'TCS': 'India\'s largest IT services provider',
            'COGNIZANT': 'specializing in digital transformation',
            'HCL': 'known for its technology solutions'
        }
        
        experience = profile_data.get('experience', 0)
        company = profile_data.get('company_name', 'Other').upper()
        
        experience_context = (
            "as someone starting their career" if experience < 2
            else "with your growing experience in the industry"
        )
        
        company_context_str = company_context.get(company, "in the IT services industry")
        
        user_prompt = f"""
        Profile Details:
        - Current Company: {company} ({company_context_str})
        - Experience: {experience} years ({experience_context})
        
        Create a connection message that:
        1. Acknowledges their role at {company}
        2. Mentions how Super30's MAANG preparation program could accelerate their career growth
        3. Ends with "Would you like to learn more about transitioning to MAANG companies?"
        
        Keep it professional but conversational.
        """
        
        for attempt in range(self.max_retries):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=150,
                    temperature=0.7
                )
                message = response['choices'][0]['message']['content'].strip()
                
                if self._validate_message(message):
                    return message
                
                logging.warning("Generated message did not meet criteria. Retrying...")
                time.sleep(self.retry_delay)
                
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                logging.warning(f"Error generating message (attempt {attempt + 1}): {str(e)}")
                time.sleep(self.retry_delay)
        
        return None
    
    def _validate_message(self, message: str) -> Optional[str]:
        """Validate and clean the generated message"""
        if not message:
            logging.warning("Empty message received")
            return None
            
        # Remove extra whitespace and newlines
        message = " ".join(message.split())
        
        # Check message length (LinkedIn connection message limit is 300 chars)
        if len(message) > 300:
            logging.warning(f"Message too long ({len(message)} chars), truncating...")
            message = message[:297] + "..."
            
        return message
