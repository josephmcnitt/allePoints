"""
Data Processor Module

This module handles the retrieval and processing of data from the Alle site.
It extracts member information including phone numbers and available points.
"""

import pandas as pd
from src.api.alle_api import AlleAPI

class DataProcessor:
    """
    Processes data from the Alle API and prepares it for display in the dashboard.
    """
    
    def __init__(self):
        """Initialize the data processor with an API client."""
        self.api_client = AlleAPI()
        self.data = None
    
    def fetch_data(self):
        """
        Fetch data from the Alle API and store it.
        
        Returns:
            pandas.DataFrame: Processed data containing member information.
        """
        # Get raw data from the API
        raw_data = self.api_client.get_members_data()
        
        # Process the data into a pandas DataFrame
        if raw_data:
            self.data = pd.DataFrame(raw_data)
            return self.data
        return pd.DataFrame()
    
    def get_members_with_points(self, min_points=0):
        """
        Filter members who have at least the specified number of points.
        
        Args:
            min_points (int): Minimum number of points to filter by.
            
        Returns:
            pandas.DataFrame: Filtered data containing members with points.
        """
        if self.data is None:
            self.fetch_data()
            
        if self.data is not None and not self.data.empty:
            return self.data[self.data['points'] >= min_points]
        return pd.DataFrame()
    
    def get_summary_stats(self):
        """
        Calculate summary statistics for the member data.
        
        Returns:
            dict: Dictionary containing summary statistics.
        """
        if self.data is None:
            self.fetch_data()
            
        if self.data is not None and not self.data.empty:
            stats = {
                'total_members': len(self.data),
                'members_with_points': len(self.data[self.data['points'] > 0]),
                'total_points': self.data['points'].sum(),
                'avg_points': self.data['points'].mean(),
                'max_points': self.data['points'].max()
            }
            return stats
        return {
            'total_members': 0,
            'members_with_points': 0,
            'total_points': 0,
            'avg_points': 0,
            'max_points': 0
        } 