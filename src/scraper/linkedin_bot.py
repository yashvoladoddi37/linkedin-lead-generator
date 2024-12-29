from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

class LinkedInBot:
    def __init__(self, config):
        self.config = config
        self.driver = self._setup_driver()
        
    def send_connection(self, profile_url, message):
        try:
            self.driver.get(profile_url)
            time.sleep(random.uniform(2, 4))
            
            connect_button = self.driver.find_element(
                By.XPATH, 
                "//button[contains(@aria-label, 'Connect')]"
            )
            connect_button.click()
            
            message_field = self.driver.find_element(
                By.XPATH, 
                "//textarea[@name='message']"
            )
            message_field.send_keys(message)
            
            send_button = self.driver.find_element(
                By.XPATH, 
                "//button[contains(@aria-label, 'Send now')]"
            )
            send_button.click()
            
            return True
            
        except Exception as e:
            print(f"Error sending connection: {str(e)}")
            return False
