#!/usr/bin/env python3
"""
AllePoints Dashboard Runner

This script serves as the entry point for running the AllePoints dashboard application.
"""

import os
import sys
import signal
import atexit
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global variables for cleanup
data_processor = None

def cleanup():
    """Clean up resources before exiting."""
    print("Cleaning up resources...")
    if data_processor:
        data_processor.close()

def signal_handler(sig, frame):
    """Handle signals to ensure proper cleanup."""
    print("Received signal to terminate. Cleaning up...")
    cleanup()
    sys.exit(0)

def run_prototype():
    """Run the prototype script."""
    print("Running AllePoints prototype...")
    from src.prototype import main
    main()

def run_dashboard():
    """Run the dashboard application."""
    global data_processor
    
    print("Running AllePoints dashboard...")
    from src.app import app
    from src.data.data_processor import DataProcessor
    
    # Initialize data processor
    data_processor = DataProcessor()
    
    # Get port from environment or use default
    port = int(os.environ.get("PORT", 8050))
    
    # Register cleanup handlers
    atexit.register(cleanup)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
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
    
    try:
        # Run the appropriate function
        if command == "prototype":
            run_prototype()
        elif command == "dashboard":
            run_dashboard()
        else:
            print(f"Unknown command: {command}")
            print_usage()
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nApplication terminated by user")
        cleanup()
    except Exception as e:
        print(f"Error: {e}")
        cleanup()
        sys.exit(1) 