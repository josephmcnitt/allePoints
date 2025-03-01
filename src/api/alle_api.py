"""
Alle API Client

This module provides functionality to interact with the Alle site's API
to retrieve member data including phone numbers and available points.
"""

import os
import requests
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class AlleAPI:
    """
    Client for interacting with the Alle API.
    """
    
    def __init__(self):
        """Initialize the API client with configuration from environment variables."""
        self.base_url = os.environ.get('ALLE_API_BASE_URL', 'https://api.alle.com')
        self.api_key = os.environ.get('ALLE_API_KEY')
        self.session = requests.Session()
        
        # Set up authentication headers if API key is available
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
        else:
            logger.warning("No API key found. Set ALLE_API_KEY environment variable.")
    
    def get_members_data(self):
        """
        Retrieve member data from the Alle API.
        
        Returns:
            list: List of dictionaries containing member data.
        """
        try:
            # This is a placeholder endpoint - update with actual endpoint
            endpoint = '/api/v1/members'
            response = self.session.get(f"{self.base_url}{endpoint}")
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"API request failed with status code {response.status_code}: {response.text}")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making API request: {e}")
            return []
    
    def get_member_points(self, member_id):
        """
        Retrieve points for a specific member.
        
        Args:
            member_id (str): The ID of the member to retrieve points for.
            
        Returns:
            dict: Dictionary containing member points information.
        """
        try:
            # This is a placeholder endpoint - update with actual endpoint
            endpoint = f'/api/v1/members/{member_id}/points'
            response = self.session.get(f"{self.base_url}{endpoint}")
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"API request failed with status code {response.status_code}: {response.text}")
                return {}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making API request: {e}")
            return {}
            
    # For development/testing purposes - simulates API response
    def get_mock_data(self):
        """
        Generate mock data for development and testing.
        
        Returns:
            list: List of dictionaries containing mock member data.
        """
        mock_data = [
            {"id": "1001", "name": "John Doe", "phone": "555-123-4567", "points": 150},
            {"id": "1002", "name": "Jane Smith", "phone": "555-234-5678", "points": 75},
            {"id": "1003", "name": "Bob Johnson", "phone": "555-345-6789", "points": 0},
            {"id": "1004", "name": "Alice Brown", "phone": "555-456-7890", "points": 200},
            {"id": "1005", "name": "Charlie Davis", "phone": "555-567-8901", "points": 50},
        ]
        return mock_data 