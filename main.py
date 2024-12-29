from src.scraper.linkedin_bot import LinkedInBot
from src.messaging.message_generator import MessageGenerator
from src.utils.profile_analyzer import ProfileAnalyzer
from config.settings import *
import time
import random

def main():
    bot = LinkedInBot(LINKEDIN_CONFIG)
    message_gen = MessageGenerator(OPENAI_API_KEY)
    analyzer = ProfileAnalyzer(TARGET_CRITERIA)
    
    # Login to LinkedIn
    bot.login()
    
    # Get target profiles
    profiles = bot.search_target_profiles()
    
    for profile in profiles:
        analysis = analyzer.analyze_profile(profile)
        
        if analysis['is_target']:
            message = message_gen.generate_connection_message(profile)
            success = bot.send_connection(profile['url'], message)
            
            if success:
                time.sleep(random.uniform(
                    LINKEDIN_CONFIG['delay_between_requests'][0],
                    LINKEDIN_CONFIG['delay_between_requests'][1]
                ))

if __name__ == "__main__":
    main()
