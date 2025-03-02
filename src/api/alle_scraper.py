"""
Alle Business Site Scraper

This module provides functionality to scrape data from the Alle business site
by logging in, searching for phone numbers, and extracting member data.
"""

import os
import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class AlleScraper:
    """
    Scraper for the Alle business site to search for members by phone number
    and extract their data.
    """
    
    def __init__(self):
        """Initialize the scraper with configuration from environment variables."""
        self.base_url = "https://business.alle.com"
        self.login_url = f"{self.base_url}/login"
        self.search_url = f"{self.base_url}/search"
        
        # Get credentials from environment variables or use defaults from constructor
        self.username = os.environ.get('ALLE_USERNAME', 'medaestheticsoffice@gmail.com')
        self.password = os.environ.get('ALLE_PASSWORD', 'Newlife33!')
        
        # Delay configuration (in seconds)
        self.min_delay = float(os.environ.get('MIN_DELAY', '1.0'))
        self.max_delay = float(os.environ.get('MAX_DELAY', '3.0'))
        self.page_load_delay = float(os.environ.get('PAGE_LOAD_DELAY', '2.0'))
        
        # Initialize webdriver
        self.driver = None
        self.is_logged_in = False
    
    def _initialize_driver(self):
        """Initialize the Selenium WebDriver."""
        options = webdriver.ChromeOptions()
        # Run in headless mode for production
        if os.environ.get('ENVIRONMENT') == 'production':
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
    
    def _random_delay(self, min_factor=1.0, max_factor=1.0):
        """
        Wait for a random amount of time within the configured delay range.
        
        Args:
            min_factor (float): Factor to multiply the minimum delay by.
            max_factor (float): Factor to multiply the maximum delay by.
        """
        min_wait = self.min_delay * min_factor
        max_wait = self.max_delay * max_factor
        delay = random.uniform(min_wait, max_wait)
        time.sleep(delay)
        return delay
    
    def _wait_for_page_load(self):
        """Wait for the page to fully load."""
        # Wait for the document to be in ready state
        self.driver.execute_script("return document.readyState") == "complete"
        # Add a small additional delay for any JavaScript to execute
        time.sleep(self.page_load_delay)
    
    def _type_like_human(self, element, text):
        """
        Type text into an element with random delays between keystrokes to simulate human typing.
        
        Args:
            element: The web element to type into.
            text (str): The text to type.
        """
        element.clear()
        for char in text:
            element.send_keys(char)
            # Small random delay between keystrokes (50-200ms)
            time.sleep(random.uniform(0.05, 0.2))
        
        # Pause after typing is complete
        self._random_delay(0.3, 0.7)
    
    def login(self):
        """
        Log in to the Alle business site.
        
        Returns:
            bool: True if login was successful, False otherwise.
        """
        if self.is_logged_in:
            return True
            
        if not self.driver:
            self._initialize_driver()
        
        try:
            logger.info("Logging in to Alle business site...")
            self.driver.get(self.login_url)
            
            # Wait for the page to load
            self._wait_for_page_load()
            
            # Wait for the login form to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            
            # Pause before starting to fill the form
            self._random_delay()
            
            # Enter username with human-like typing
            email_field = self.driver.find_element(By.ID, "email")
            self._type_like_human(email_field, self.username)
            
            # Pause before typing password
            self._random_delay(0.5, 1.0)
            
            # Enter password with human-like typing
            password_field = self.driver.find_element(By.ID, "password")
            self._type_like_human(password_field, self.password)
            
            # Pause before clicking the login button
            self._random_delay()
            
            # Click the login button
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
            
            # Wait for login to complete
            WebDriverWait(self.driver, 15).until(
                EC.url_contains("/dashboard")
            )
            
            # Wait for the dashboard to fully load
            self._wait_for_page_load()
            
            # Additional pause after successful login
            self._random_delay(1.0, 2.0)
            
            self.is_logged_in = True
            logger.info("Successfully logged in to Alle business site")
            return True
            
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Login failed: {e}")
            return False
    
    def search_by_phone(self, phone_number):
        """
        Search for a member by phone number.
        
        Args:
            phone_number (str): The phone number to search for.
            
        Returns:
            dict: Dictionary containing member data if found, empty dict otherwise.
        """
        if not self.is_logged_in and not self.login():
            logger.error("Cannot search: Not logged in")
            return {}
        
        try:
            logger.info(f"Searching for phone number: {phone_number}")
            
            # Navigate to the search page
            self.driver.get(self.search_url)
            
            # Wait for the page to load
            self._wait_for_page_load()
            
            # Wait for the search input to load
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
            )
            
            # Pause before starting to fill the search field
            self._random_delay()
            
            # Clear any existing input and enter the phone number with human-like typing
            self._type_like_human(search_input, phone_number)
            
            # Pause before submitting the search
            self._random_delay(0.5, 1.0)
            
            # Submit the search
            search_input.send_keys(Keys.RETURN)
            
            # Wait for search results
            delay = self._random_delay(1.0, 2.0)
            logger.info(f"Waiting {delay:.2f} seconds for search results...")
            
            # Check if we have search results
            try:
                # Look for search results
                result_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'search-result')]"))
                )
                
                # Pause before clicking on the result
                self._random_delay()
                
                # Click on the first result
                result_element.click()
                
                # Wait for the member details page to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'member-details')]"))
                )
                
                # Wait for the page to fully load
                self._wait_for_page_load()
                
                # Pause before extracting data
                self._random_delay()
                
                # Extract member data
                return self._extract_member_data()
                
            except TimeoutException:
                logger.info(f"No results found for phone number: {phone_number}")
                return {}
                
        except Exception as e:
            logger.error(f"Error searching for phone number: {e}")
            return {}
    
    def _extract_member_data(self):
        """
        Extract member data from the member details page.
        
        Returns:
            dict: Dictionary containing member data.
        """
        try:
            # Initialize member data dictionary
            member_data = {}
            
            # Small delay before starting to extract data
            self._random_delay(0.3, 0.7)
            
            # Extract name
            try:
                name_element = self.driver.find_element(By.XPATH, "//h1[contains(@class, 'member-name')]")
                member_data['name'] = name_element.text
            except NoSuchElementException:
                member_data['name'] = "N/A"
            
            # Extract phone number
            try:
                phone_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Phone')]/following-sibling::div")
                member_data['phone'] = phone_element.text
            except NoSuchElementException:
                member_data['phone'] = "N/A"
            
            # Extract email
            try:
                email_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Email')]/following-sibling::div")
                member_data['email'] = email_element.text
            except NoSuchElementException:
                member_data['email'] = "N/A"
            
            # Small delay to mimic reading the page
            self._random_delay(0.2, 0.5)
            
            # Extract points
            try:
                points_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Points')]/following-sibling::div")
                points_text = points_element.text.replace(',', '')
                member_data['points'] = int(points_text) if points_text.isdigit() else 0
            except NoSuchElementException:
                member_data['points'] = 0
            
            # Extract member ID
            try:
                member_id_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Member ID')]/following-sibling::div")
                member_data['id'] = member_id_element.text
            except NoSuchElementException:
                member_data['id'] = "N/A"
            
            # Extract additional fields as needed
            # ...
            
            # Final delay after collecting all data
            self._random_delay(0.5, 1.0)
            
            return member_data
            
        except Exception as e:
            logger.error(f"Error extracting member data: {e}")
            return {}
    
    def close(self):
        """Close the WebDriver and clean up resources."""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.is_logged_in = False 