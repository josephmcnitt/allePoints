"""
Test script for the Alle scraper.

This script tests the functionality of the Alle scraper by searching for a phone number
and verifying that the expected data is returned.
"""

import os
import sys
import unittest
from dotenv import load_dotenv

# Add the parent directory to the path so we can import the src modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.alle_scraper import AlleScraper

# Load environment variables
load_dotenv()

class TestAlleScraper(unittest.TestCase):
    """Test cases for the Alle scraper."""
    
    def setUp(self):
        """Set up the test environment."""
        self.scraper = AlleScraper()
    
    def tearDown(self):
        """Clean up after the test."""
        if self.scraper:
            self.scraper.close()
    
    def test_login(self):
        """Test that the scraper can log in to the Alle business site."""
        result = self.scraper.login()
        self.assertTrue(result, "Failed to log in to Alle business site")
    
    def test_search_by_phone(self):
        """Test searching for a member by phone number."""
        # Use a test phone number - this should be a valid phone number in your Alle account
        test_phone = "555-123-4567"  # Replace with a valid test phone number
        
        # Search for the member
        member_data = self.scraper.search_by_phone(test_phone)
        
        # Check that we got some data back
        self.assertIsNotNone(member_data, "No member data returned")
        self.assertIsInstance(member_data, dict, "Member data should be a dictionary")
        
        # Check that the data contains the expected fields
        expected_fields = ["name", "phone", "email", "points", "id"]
        for field in expected_fields:
            self.assertIn(field, member_data, f"Member data missing field: {field}")
        
        # Check that the phone number matches what we searched for
        # Note: The format might be different, so we just check that the digits match
        search_digits = ''.join(filter(str.isdigit, test_phone))
        result_digits = ''.join(filter(str.isdigit, member_data.get("phone", "")))
        self.assertEqual(search_digits, result_digits, "Phone number in result doesn't match search")

if __name__ == "__main__":
    unittest.main() 