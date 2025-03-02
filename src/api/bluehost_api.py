"""
Bluehost API Client

This module provides functionality to interact with the Bluehost site
for deploying and managing the dashboard.
"""

import os
import time
import random
import logging
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class BluehostClient:
    """
    Client for interacting with the Bluehost site.
    """
    
    def __init__(self):
        """Initialize the Bluehost client with configuration from environment variables."""
        self.base_url = "https://www.bluehost.com"
        self.login_url = f"{self.base_url}/login"
        self.account_url = f"{self.base_url}/my-account/hosting/details"
        
        # Get credentials from environment variables or use defaults from constructor
        self.username = os.environ.get('BLUEHOST_USERNAME', 'yourmeda')
        self.password = os.environ.get('BLUEHOST_PASSWORD', 'Positive33!!')
        
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
        Log in to the Bluehost site.
        
        Returns:
            bool: True if login was successful, False otherwise.
        """
        if self.is_logged_in:
            return True
            
        if not self.driver:
            self._initialize_driver()
        
        try:
            logger.info("Logging in to Bluehost...")
            self.driver.get(self.login_url)
            
            # Wait for the page to load
            self._wait_for_page_load()
            
            # Wait for the login form to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            
            # Pause before starting to fill the form
            self._random_delay()
            
            # Enter username with human-like typing
            username_field = self.driver.find_element(By.ID, "username")
            self._type_like_human(username_field, self.username)
            
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
                EC.url_contains("/my-account")
            )
            
            # Wait for the page to fully load
            self._wait_for_page_load()
            
            # Additional pause after successful login
            self._random_delay(1.0, 2.0)
            
            self.is_logged_in = True
            logger.info("Successfully logged in to Bluehost")
            return True
            
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Login failed: {e}")
            return False
    
    def navigate_to_file_manager(self):
        """
        Navigate to the file manager in the Bluehost control panel.
        
        Returns:
            bool: True if navigation was successful, False otherwise.
        """
        if not self.is_logged_in and not self.login():
            logger.error("Cannot navigate: Not logged in")
            return False
        
        try:
            logger.info("Navigating to file manager...")
            
            # Navigate to the account page
            self.driver.get(self.account_url)
            
            # Wait for the page to load
            self._wait_for_page_load()
            
            # Wait for the page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'File Manager')]"))
            )
            
            # Pause before clicking
            self._random_delay()
            
            # Click on the File Manager link
            self.driver.find_element(By.XPATH, "//a[contains(text(), 'File Manager')]").click()
            
            # Wait for the file manager to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "file-manager"))
            )
            
            # Wait for the page to fully load
            self._wait_for_page_load()
            
            logger.info("Successfully navigated to file manager")
            return True
            
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Navigation failed: {e}")
            return False
    
    def upload_file(self, local_path, remote_path):
        """
        Upload a file to the Bluehost server.
        
        Args:
            local_path (str): The local path of the file to upload.
            remote_path (str): The remote path to upload the file to.
            
        Returns:
            bool: True if upload was successful, False otherwise.
        """
        if not self.is_logged_in and not self.login():
            logger.error("Cannot upload: Not logged in")
            return False
            
        if not self.navigate_to_file_manager():
            logger.error("Cannot upload: Failed to navigate to file manager")
            return False
        
        try:
            logger.info(f"Uploading file from {local_path} to {remote_path}...")
            
            # Pause before clicking upload
            self._random_delay()
            
            # Click on the upload button
            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Upload')]").click()
            
            # Wait for the upload dialog to appear
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "file-upload-input"))
            )
            
            # Pause before entering file information
            self._random_delay()
            
            # Enter the local file path
            file_input = self.driver.find_element(By.ID, "file-upload-input")
            file_input.send_keys(local_path)
            
            # Pause between fields
            self._random_delay(0.5, 1.0)
            
            # Enter the remote path
            remote_path_input = self.driver.find_element(By.ID, "remote-path-input")
            self._type_like_human(remote_path_input, remote_path)
            
            # Pause before clicking upload
            self._random_delay()
            
            # Click the upload button
            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Upload File')]").click()
            
            # Wait for the upload to complete with a longer timeout
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Upload complete')]"))
            )
            
            # Pause after upload completes
            self._random_delay(1.0, 2.0)
            
            logger.info(f"Successfully uploaded file to {remote_path}")
            return True
            
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Upload failed: {e}")
            return False
    
    def close(self):
        """Close the WebDriver and clean up resources."""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.is_logged_in = False 