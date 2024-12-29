import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import logging

class LinkedInBot:
    def __init__(self, config):
        self.config = config
        logging.info("Initializing LinkedIn Bot...")
        self.driver = self._setup_driver()
        
    def _setup_driver(self):
        logging.info("Setting up undetected Chrome driver...")
        options = uc.ChromeOptions()
        options.add_argument("--start-maximized")
        
        # Create undetected Chrome driver
        driver = uc.Chrome(
            options=options,
            headless=False,
            log_level=3
        )
        
        # Set page load timeout
        driver.set_page_load_timeout(30)
        return driver

    def wait_random(self, min_seconds=2, max_seconds=5):
        """Add random delay to appear more human-like"""
        time.sleep(random.uniform(min_seconds, max_seconds))

    def wait_for_element(self, by, value, timeout=10):
        """Wait for element to be present and visible"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception as e:
            logging.error(f"Element not found: {value}")
            return None

    def login(self):
        try:
            logging.info("Navigating to LinkedIn login page...")
            self.driver.get("https://www.linkedin.com/login")
            self.wait_random(2, 3)
            
            # Wait for login form
            username_field = self.wait_for_element(By.ID, "username")
            if not username_field:
                raise Exception("Login form not found")
                
            # Enter credentials
            username_field.send_keys(self.config['email'])
            self.wait_random(1, 2)
            
            password_field = self.wait_for_element(By.ID, "password")
            password_field.send_keys(self.config['password'])
            self.wait_random(1, 2)
            
            # Click login
            sign_in_button = self.wait_for_element(By.XPATH, "//button[@type='submit']")
            sign_in_button.click()
            
            # Wait for login to complete
            time.sleep(5)  # Wait for potential redirects
            
            # Check if login was successful
            if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url:
                logging.info("Login successful!")
            else:
                logging.warning(f"Login might require verification. Current URL: {self.driver.current_url}")
                # Wait for manual verification if needed
                while not ("feed" in self.driver.current_url or "mynetwork" in self.driver.current_url):
                    logging.info("Waiting for manual verification...")
                    time.sleep(5)
                logging.info("Verification completed successfully!")
                
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            raise

    def _get_name(self):
        """Extract name from profile page"""
        return self.wait_for_element(By.XPATH, "//h1").text.strip()
    
    def _get_company(self):
        """Extract current company from profile page"""
        try:
            company_elem = self.wait_for_element(
                By.XPATH, "//div[contains(@aria-label, 'Current company')]"
            )
            return company_elem.text.strip() if company_elem else ""
        except:
            return ""
    
    def _get_recent_activity(self):
        """Extract recent activity from profile page"""
        try:
            activities = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'feed-shared-update-v2')]"
            )
            if activities:
                return activities[0].text.strip()
            return ""
        except:
            return ""
    
    def _get_experience(self):
        """Extract experience count from profile page"""
        try:
            exp_section = self.wait_for_element(
                By.XPATH, "//section[@id='experience-section']"
            )
            if exp_section:
                experiences = exp_section.find_elements(By.XPATH, ".//li")
                return len(experiences)
            return 0
        except:
            return 0
    
    def scrape_profile(self, profile_url):
        """Scrape detailed information from a profile page"""
        try:
            logging.info(f"Scraping profile: {profile_url}")
            self.driver.get(profile_url)
            self.wait_random(2, 4)
            
            profile_data = {
                'name': self._get_name(),
                'company': self._get_company(),
                'activity': self._get_recent_activity(),
                'experience': self._get_experience(),
                'url': profile_url
            }
            
            logging.info(f"Successfully scraped profile: {profile_data['name']}")
            return profile_data
            
        except Exception as e:
            logging.error(f"Error scraping profile: {str(e)}")
            return None

    def search_target_profiles(self, company_name=None):
        """
        Search for target profiles with specific company and experience filters
        Args:
            company_name: Optional specific WITCH company to target (e.g., 'Wipro', 'TCS')
        """
        logging.info("Starting profile search...")
        profiles = []
        
        # Define search parameters
        witch_companies = {
            'wipro': 'Wipro',
            'infosys': 'Infosys',
            'tcs': 'Tata Consultancy Services',
            'cognizant': 'Cognizant',
            'hcl': 'HCL Technologies'
        }
        
        try:
            companies_to_search = [witch_companies[company_name.lower()]] if company_name else witch_companies.values()
            
            for company in companies_to_search:
                logging.info(f"Searching profiles from {company}...")
                
                # Construct search URL with company and experience filters
                search_url = (
                    "https://www.linkedin.com/search/results/people/?"
                    f"currentCompany=[%22{company}%22]&"
                    "keywords=software%20engineer%20OR%20developer&"
                    "timeAtCompany=[%22R0-5%22]&"  # 0-5 years at company
                    "origin=FACETED_SEARCH"
                )
                
                logging.info(f"Navigating to search URL: {search_url}")
                self.driver.get(search_url)
                self.wait_random(3, 5)

                # Scroll down a few times to load more results
                for _ in range(3):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    self.wait_random(1, 2)

                # Extract profile information
                profile_cards = self.driver.find_elements(By.CLASS_NAME, "reusable-search__result-container")
                
                for card in profile_cards[:10]:  # Limit to 10 profiles per company to avoid detection
                    try:
                        name_elem = card.find_element(By.CLASS_NAME, "app-aware-link")
                        profile_url = name_elem.get_attribute("href")
                        
                        if profile_url and "/in/" in profile_url:  # Ensure it's a valid profile URL
                            profile_data = self.scrape_profile(profile_url)
                            if profile_data:
                                profiles.append(profile_data)
                                logging.info(f"Found profile: {profile_data['name']} - {profile_data['company']}")
                    
                    except Exception as e:
                        logging.warning(f"Error extracting profile data: {str(e)}")
                        continue
                        
                self.wait_random(5, 8)  # Wait between company searches
                
            logging.info(f"Profile search completed. Found {len(profiles)} profiles")
            return profiles
            
        except Exception as e:
            logging.error(f"Error during profile search: {str(e)}")
            return []

    def send_connection(self, profile_url, message):
        try:
            logging.info(f"Visiting profile: {profile_url}")
            self.driver.get(profile_url)
            self.wait_random(3, 5)  # Wait and appear human-like
            
            # Scroll the page naturally
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight * 0.4);"
            )
            self.wait_random(2, 4)
            
            # Try different connect button selectors
            connect_button = None
            connect_selectors = [
                "//button[contains(@aria-label, 'Connect')]",
                "//button[contains(@class, 'connect')]",
                "//button[contains(@class, 'connection')]"
            ]
            
            for selector in connect_selectors:
                try:
                    connect_button = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    if connect_button:
                        break
                except:
                    continue
            
            if not connect_button:
                logging.warning("Connect button not found. Profile might not be available for connection.")
                return False
                
            connect_button.click()
            self.wait_random(1, 2)
            
            # Wait for message dialog
            message_field = self.wait_for_element(By.XPATH, "//textarea[@name='message']")
            if not message_field:
                logging.warning("Message field not found")
                return False
            
            # random delay in typing to simulate human-like typing
            for char in message:
                message_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            
            self.wait_random(1, 2)
            
            # Find and click send button
            send_button = self.wait_for_element(By.XPATH, "//button[contains(@aria-label, 'Send now')]")
            if not send_button:
                logging.warning("Send button not found")
                return False
                
            send_button.click()
            
            logging.info(f"Connection request sent successfully")
            self.wait_random(4, 6)  # wait after sending request
            return True
            
        except Exception as e:
            logging.error(f"Failed to send connection request: {str(e)}")
            return False
