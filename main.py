from src.scraper.linkedin_bot import LinkedInBot
from src.messaging.message_generator import MessageGenerator
from src.utils.profile_analyzer import ProfileAnalyzer
from config.settings import *
import time
import random
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    logging.info("Starting LinkedIn Outreach Bot...")
    
    try:
        # Initialize components
        bot = LinkedInBot(LINKEDIN_CONFIG)
        message_gen = MessageGenerator(OPENAI_API_KEY)
        analyzer = ProfileAnalyzer(TARGET_CRITERIA)
        
        # Login to LinkedIn (manual login)
        bot.login()
        
        # Get target profiles
        profiles = bot.search_target_profiles()
        
        if not profiles:
            logging.warning("No profiles found. Please check the search criteria.")
            return
            
        # Process each profile
        connections_sent = 0
        max_connections = LINKEDIN_CONFIG.get('max_requests_per_day', 15)
        
        for profile in profiles:
            if connections_sent >= max_connections:
                logging.info(f"Reached maximum connections limit for today ({max_connections})")
                break
                
            logging.info(f"Analyzing profile: {profile.get('name')} - {profile.get('title')}")
            analysis = analyzer.analyze_profile(profile)
            
            if analysis['is_target']:
                logging.info("Profile matches target criteria. Generating personalized message...")
                message = message_gen.generate_connection_message(profile)
                
                logging.info("Sending connection request...")
                success = bot.send_connection(profile['url'], message)
                
                if success:
                    connections_sent += 1
                    logging.info(f"Successfully sent connection request ({connections_sent}/{max_connections})")
                    
                    # Add longer delay between successful connections
                    delay = random.uniform(
                        LINKEDIN_CONFIG['delay_between_requests'][0],
                        LINKEDIN_CONFIG['delay_between_requests'][1]
                    )
                    logging.info(f"Waiting {delay:.2f} seconds before next request...")
                    time.sleep(delay)
            else:
                logging.info("Profile does not match target criteria, skipping...")
        
        logging.info(f"Session completed. Sent {connections_sent} connection requests.")

    except KeyboardInterrupt:
        logging.info("Bot stopped by user.")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)
    finally:
        logging.info("Closing browser...")
        if 'bot' in locals() and bot.driver:
            bot.driver.quit()

if __name__ == "__main__":
    main()
