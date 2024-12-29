from openai import OpenAI

class MessageGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        
    def generate_connection_message(self, profile_data):
        system_prompt = """
        You are a professional tech career mentor. Create personalized LinkedIn connection messages that:
        1. Start by acknowledging their recent activity or achievement
        2. Introduce Super30 as an exclusive MAANG preparation program
        3. End with a casual invitation to learn more
        4. Keep it under 300 characters
        5. Maintain a friendly, professional tone
        """
        
        user_prompt = f"""
        Profile Details:
        - Current Role: {profile_data['role']}
        - Company: {profile_data['company']}
        - Recent Activity: {profile_data['activity']}
        - Experience: {profile_data['experience']} years
        
        Create a connection message that:
        1. References their {profile_data['activity']}
        2. Mentions Super30's exclusive MAANG preparation program
        3. Ends with "Interested to learn more?"
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        return self._validate_message(response.choices[0].message.content)
