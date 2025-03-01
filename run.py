#!/usr/bin/env python3
"""
AllePoints Dashboard Runner

This script serves as the entry point for running the AllePoints dashboard application.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_prototype():
    """Run the prototype script."""
    print("Running AllePoints prototype...")
    from src.prototype import main
    main()

def run_dashboard():
    """Run the dashboard application."""
    print("Running AllePoints dashboard...")
    from src.app import app
    
    # Get port from environment or use default
    port = int(os.environ.get("PORT", 8050))
    
    # Run the app
    app.run_server(debug=True, port=port)

def print_usage():
    """Print usage information."""
    print("Usage: python run.py [prototype|dashboard]")
    print("  prototype: Run the prototype script")
    print("  dashboard: Run the dashboard application")

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    # Get the command
    command = sys.argv[1].lower()
    
    # Run the appropriate function
    if command == "prototype":
        run_prototype()
    elif command == "dashboard":
        run_dashboard()
    else:
        print(f"Unknown command: {command}")
        print_usage()
        sys.exit(1) 