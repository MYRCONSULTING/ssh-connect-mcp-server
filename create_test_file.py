#!/usr/bin/env python3
"""
Create a test file for SSH MCP server testing.

This script creates a simple text file that can be used to test the upload
and download functionality of the SSH MCP server.
"""

import os
import sys

def create_test_file(filename="test_file.txt", content=None):
    """Create a test file with the given filename and content."""
    if content is None:
        content = """This is a test file for the SSH MCP server.
It can be used to test the upload and download functionality.
Feel free to modify this file as needed.
"""
    
    try:
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Test file '{filename}' created successfully.")
        print(f"Full path: {os.path.abspath(filename)}")
        return True
    except Exception as e:
        print(f"Error creating test file: {e}")
        return False

if __name__ == "__main__":
    # Get filename from command line arguments if provided
    filename = "test_file.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    # Create the test file
    create_test_file(filename)
