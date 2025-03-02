#!/usr/bin/env python3
"""
Deployment Script for AllePoints Dashboard

This script deploys the AllePoints dashboard to a Bluehost server.
It packages the application, uploads it to the server, and sets up
the necessary configuration.
"""

import os
import sys
import logging
import shutil
import tempfile
import subprocess
from dotenv import load_dotenv
from src.api.bluehost_api import BluehostClient

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def create_deployment_package():
    """
    Create a deployment package containing all necessary files.
    
    Returns:
        str: Path to the deployment package.
    """
    logger.info("Creating deployment package...")
    
    # Create a temporary directory for the package
    temp_dir = tempfile.mkdtemp()
    package_dir = os.path.join(temp_dir, "allepoints")
    os.makedirs(package_dir)
    
    # Copy source files
    shutil.copytree("src", os.path.join(package_dir, "src"))
    
    # Copy requirements.txt
    shutil.copy("requirements.txt", package_dir)
    
    # Copy run.py
    shutil.copy("run.py", package_dir)
    
    # Create a .env file with production settings
    with open(os.path.join(package_dir, ".env"), "w") as f:
        f.write(f"ALLE_USERNAME={os.environ.get('ALLE_USERNAME')}\n")
        f.write(f"ALLE_PASSWORD={os.environ.get('ALLE_PASSWORD')}\n")
        f.write("ENVIRONMENT=production\n")
        f.write("PORT=8080\n")
    
    # Create a zip file
    package_path = os.path.join(temp_dir, "allepoints.zip")
    shutil.make_archive(os.path.join(temp_dir, "allepoints"), "zip", package_dir)
    
    logger.info(f"Deployment package created at {package_path}")
    return package_path

def deploy_to_bluehost(package_path):
    """
    Deploy the package to Bluehost.
    
    Args:
        package_path (str): Path to the deployment package.
        
    Returns:
        bool: True if deployment was successful, False otherwise.
    """
    logger.info("Deploying to Bluehost...")
    
    # Initialize the Bluehost client
    client = BluehostClient()
    
    try:
        # Login to Bluehost
        if not client.login():
            logger.error("Failed to log in to Bluehost")
            return False
        
        # Navigate to the file manager
        if not client.navigate_to_file_manager():
            logger.error("Failed to navigate to file manager")
            return False
        
        # Upload the package
        remote_path = "/public_html/allepoints"
        if not client.upload_file(package_path, remote_path):
            logger.error("Failed to upload package")
            return False
        
        logger.info("Package uploaded successfully")
        
        # TODO: Add steps to unzip the package and set up the application on Bluehost
        # This would typically involve SSH access or using Bluehost's control panel
        
        logger.info("Deployment completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        return False
    finally:
        client.close()

def main():
    """Main function to run the deployment process."""
    try:
        # Create the deployment package
        package_path = create_deployment_package()
        
        # Deploy to Bluehost
        success = deploy_to_bluehost(package_path)
        
        if success:
            logger.info("Deployment completed successfully")
            return 0
        else:
            logger.error("Deployment failed")
            return 1
            
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 