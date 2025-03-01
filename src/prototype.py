#!/usr/bin/env python3
"""
AllePoints Prototype Script

This is a simple prototype script that demonstrates pulling data from the Alle system.
It retrieves member information including phone numbers and available points.
"""

import os
import json
import requests
from dotenv import load_dotenv
import pandas as pd
from tabulate import tabulate

# Load environment variables
load_dotenv()

def get_api_key():
    """Get the API key from environment variables."""
    api_key = os.environ.get('ALLE_API_KEY')
    if not api_key:
        print("Warning: No API key found. Using mock data.")
    return api_key

def get_base_url():
    """Get the base URL from environment variables."""
    return os.environ.get('ALLE_API_BASE_URL', 'https://api.alle.com')

def get_headers(api_key):
    """Create headers for API requests."""
    if api_key:
        return {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    return {'Content-Type': 'application/json'}

def get_members_data(api_key, base_url):
    """
    Retrieve member data from the Alle API.
    
    Args:
        api_key (str): The API key for authentication.
        base_url (str): The base URL for the API.
        
    Returns:
        list: List of dictionaries containing member data.
    """
    # If no API key, use mock data
    if not api_key:
        return get_mock_data()
    
    try:
        headers = get_headers(api_key)
        endpoint = '/api/v1/members'
        response = requests.get(f"{base_url}{endpoint}", headers=headers)
        
        if response.status_code == 200:
            return response.json().get('members', [])
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            print(f"Response: {response.text}")
            return get_mock_data()
            
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return get_mock_data()

def get_member_points(member_id, api_key, base_url):
    """
    Retrieve points for a specific member.
    
    Args:
        member_id (str): The ID of the member to retrieve points for.
        api_key (str): The API key for authentication.
        base_url (str): The base URL for the API.
        
    Returns:
        dict: Dictionary containing member points information.
    """
    # If no API key, use mock data
    if not api_key:
        return get_mock_points(member_id)
    
    try:
        headers = get_headers(api_key)
        endpoint = f'/api/v1/members/{member_id}/points'
        response = requests.get(f"{base_url}{endpoint}", headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            print(f"Response: {response.text}")
            return get_mock_points(member_id)
            
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return get_mock_points(member_id)

def get_mock_data():
    """
    Generate mock data for development and testing.
    
    Returns:
        list: List of dictionaries containing mock member data.
    """
    print("Using mock member data...")
    mock_data = [
        {"id": "1001", "name": "John Doe", "phone": "555-123-4567", "email": "john.doe@example.com"},
        {"id": "1002", "name": "Jane Smith", "phone": "555-234-5678", "email": "jane.smith@example.com"},
        {"id": "1003", "name": "Bob Johnson", "phone": "555-345-6789", "email": "bob.johnson@example.com"},
        {"id": "1004", "name": "Alice Brown", "phone": "555-456-7890", "email": "alice.brown@example.com"},
        {"id": "1005", "name": "Charlie Davis", "phone": "555-567-8901", "email": "charlie.davis@example.com"},
    ]
    return mock_data

def get_mock_points(member_id):
    """
    Generate mock points data for a specific member.
    
    Args:
        member_id (str): The ID of the member.
        
    Returns:
        dict: Dictionary containing mock points data.
    """
    print(f"Using mock points data for member {member_id}...")
    mock_points = {
        "1001": {"member_id": "1001", "points": 150, "last_updated": "2025-02-15T10:30:00Z", "expiration_date": "2025-12-31T23:59:59Z"},
        "1002": {"member_id": "1002", "points": 75, "last_updated": "2025-02-20T14:45:00Z", "expiration_date": "2025-12-31T23:59:59Z"},
        "1003": {"member_id": "1003", "points": 0, "last_updated": "2025-01-10T09:15:00Z", "expiration_date": "2025-12-31T23:59:59Z"},
        "1004": {"member_id": "1004", "points": 200, "last_updated": "2025-02-25T16:20:00Z", "expiration_date": "2025-12-31T23:59:59Z"},
        "1005": {"member_id": "1005", "points": 50, "last_updated": "2025-02-18T11:10:00Z", "expiration_date": "2025-12-31T23:59:59Z"},
    }
    return mock_points.get(member_id, {"member_id": member_id, "points": 0, "last_updated": "2025-01-01T00:00:00Z", "expiration_date": "2025-12-31T23:59:59Z"})

def combine_member_and_points_data(members, api_key, base_url):
    """
    Combine member data with their points information.
    
    Args:
        members (list): List of member dictionaries.
        api_key (str): The API key for authentication.
        base_url (str): The base URL for the API.
        
    Returns:
        list: List of dictionaries with combined member and points data.
    """
    combined_data = []
    
    for member in members:
        member_id = member['id']
        points_data = get_member_points(member_id, api_key, base_url)
        
        combined_member = {
            "id": member['id'],
            "name": member['name'],
            "phone": member['phone'],
            "email": member.get('email', ''),
            "points": points_data.get('points', 0),
            "last_updated": points_data.get('last_updated', ''),
            "expiration_date": points_data.get('expiration_date', '')
        }
        
        combined_data.append(combined_member)
    
    return combined_data

def display_members_with_points(members_data, min_points=0):
    """
    Display members who have at least the specified number of points.
    
    Args:
        members_data (list): List of dictionaries with member and points data.
        min_points (int): Minimum number of points to filter by.
    """
    # Filter members with points
    members_with_points = [m for m in members_data if m['points'] >= min_points]
    
    if not members_with_points:
        print(f"No members found with {min_points} or more points.")
        return
    
    # Convert to DataFrame for easier display
    df = pd.DataFrame(members_with_points)
    
    # Sort by points (descending)
    df = df.sort_values('points', ascending=False)
    
    # Display the results
    print(f"\nMembers with {min_points} or more points:")
    print(tabulate(df[['name', 'phone', 'points']], headers='keys', tablefmt='pretty'))
    
    # Display summary statistics
    total_members = len(members_data)
    members_with_points_count = len(members_with_points)
    total_points = sum(m['points'] for m in members_data)
    avg_points = total_points / total_members if total_members > 0 else 0
    
    print("\nSummary Statistics:")
    print(f"Total Members: {total_members}")
    print(f"Members with Points: {members_with_points_count}")
    print(f"Total Points: {total_points}")
    print(f"Average Points: {avg_points:.1f}")

def main():
    """Main function to run the prototype."""
    print("AllePoints Prototype")
    print("===================")
    
    # Get API credentials
    api_key = get_api_key()
    base_url = get_base_url()
    
    # Get member data
    print("\nRetrieving member data...")
    members = get_members_data(api_key, base_url)
    
    if not members:
        print("No members found.")
        return
    
    print(f"Retrieved {len(members)} members.")
    
    # Combine member data with points
    print("\nRetrieving points data for each member...")
    combined_data = combine_member_and_points_data(members, api_key, base_url)
    
    # Display members with points
    display_members_with_points(combined_data, min_points=0)
    
    # Allow filtering by minimum points
    try:
        min_points = int(input("\nEnter minimum points to filter by (or press Enter to exit): "))
        display_members_with_points(combined_data, min_points=min_points)
    except ValueError:
        pass
    
    print("\nPrototype completed.")

if __name__ == "__main__":
    main() 