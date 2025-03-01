"""
Tests for the DataProcessor module.
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.data.data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
    """Test cases for the DataProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_data = [
            {"id": "1001", "name": "John Doe", "phone": "555-123-4567", "points": 150},
            {"id": "1002", "name": "Jane Smith", "phone": "555-234-5678", "points": 75},
            {"id": "1003", "name": "Bob Johnson", "phone": "555-345-6789", "points": 0},
            {"id": "1004", "name": "Alice Brown", "phone": "555-456-7890", "points": 200},
            {"id": "1005", "name": "Charlie Davis", "phone": "555-567-8901", "points": 50},
        ]
    
    @patch('src.api.alle_api.AlleAPI')
    def test_fetch_data(self, mock_api_class):
        """Test fetching data from the API."""
        # Set up the mock
        mock_api = mock_api_class.return_value
        mock_api.get_members_data.return_value = self.mock_data
        
        # Create the data processor with the mock API
        processor = DataProcessor()
        processor.api_client = mock_api
        
        # Call the method under test
        result = processor.fetch_data()
        
        # Verify the result
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 5)
        self.assertEqual(result.iloc[0]['name'], 'John Doe')
        self.assertEqual(result.iloc[0]['points'], 150)
    
    @patch('src.api.alle_api.AlleAPI')
    def test_get_members_with_points(self, mock_api_class):
        """Test filtering members with points."""
        # Set up the mock
        mock_api = mock_api_class.return_value
        mock_api.get_members_data.return_value = self.mock_data
        
        # Create the data processor with the mock API
        processor = DataProcessor()
        processor.api_client = mock_api
        
        # Call the method under test
        result = processor.get_members_with_points(min_points=50)
        
        # Verify the result
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 4)  # Should exclude Bob Johnson with 0 points
        
        # Test with higher threshold
        result = processor.get_members_with_points(min_points=100)
        self.assertEqual(len(result), 2)  # Should only include John Doe and Alice Brown
    
    @patch('src.api.alle_api.AlleAPI')
    def test_get_summary_stats(self, mock_api_class):
        """Test calculating summary statistics."""
        # Set up the mock
        mock_api = mock_api_class.return_value
        mock_api.get_members_data.return_value = self.mock_data
        
        # Create the data processor with the mock API
        processor = DataProcessor()
        processor.api_client = mock_api
        
        # Call the method under test
        stats = processor.get_summary_stats()
        
        # Verify the result
        self.assertEqual(stats['total_members'], 5)
        self.assertEqual(stats['members_with_points'], 4)
        self.assertEqual(stats['total_points'], 475)
        self.assertEqual(stats['avg_points'], 95.0)
        self.assertEqual(stats['max_points'], 200)

if __name__ == '__main__':
    unittest.main() 