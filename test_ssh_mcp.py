#!/usr/bin/env python3
"""
Test script for SSH MCP server.

This script demonstrates how to use the SSH MCP server directly from Python,
without using Cline. It performs a series of operations:
1. Connect to the SSH server
2. Execute a command
3. Upload a file
4. List files
5. Download a file
6. Disconnect from the SSH server
"""

import json
import os
import subprocess
import sys
import tempfile

def call_mcp_tool(tool_name, arguments=None):
    """Call an MCP tool and return the result."""
    if arguments is None:
        arguments = {}
    
    # Create a request to call the tool
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "callTool",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    # Call the MCP server with the request
    cmd = [
        "uv",
        "--directory",
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "run",
        "ssh-connect"
    ]
    
    result = subprocess.run(
        cmd,
        input=json.dumps(request).encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Parse the response
    try:
        response = json.loads(result.stdout)
        if "error" in response:
            print(f"Error: {response['error']['message']}")
            return None
        return response["result"]["content"][0]["text"]
    except Exception as e:
        print(f"Failed to parse response: {e}")
        print(f"Response: {result.stdout.decode()}")
        return None

def create_test_file():
    """Create a test file for upload."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("This is a test file for SSH MCP server testing.")
        return f.name

def main():
    """Run the SSH MCP server test."""
    print("SSH MCP Server Test")
    print("==================")
    
    # 1. Connect to SSH server
    print("\n1. Connecting to SSH server...")
    result = call_mcp_tool("connect")
    print(result)
    
    # 2. Execute a command
    print("\n2. Executing command 'ls -la'...")
    result = call_mcp_tool("execute", {"command": "ls -la"})
    print(result)
    
    # 3. Create and upload a test file
    print("\n3. Creating test file...")
    local_file = create_test_file()
    print(f"Test file created: {local_file}")
    
    print("\n4. Uploading test file...")
    result = call_mcp_tool("upload", {
        "local_path": local_file,
        "remote_path": "/home/lanuser/test_file.txt"
    })
    print(result)
    
    # 4. List files to verify upload
    print("\n5. Listing files in /home/lanuser...")
    result = call_mcp_tool("list_files", {"path": "/home/lanuser"})
    print(result)
    
    # 5. Download the file to a different location
    download_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloaded_test_file.txt")
    print(f"\n6. Downloading file to {download_path}...")
    result = call_mcp_tool("download", {
        "remote_path": "/home/lanuser/test_file.txt",
        "local_path": download_path
    })
    print(result)
    
    # 6. Disconnect from SSH server
    print("\n7. Disconnecting from SSH server...")
    result = call_mcp_tool("disconnect")
    print(result)
    
    # Clean up
    os.unlink(local_file)
    print(f"\nTest completed. Downloaded file is at: {download_path}")

if __name__ == "__main__":
    main()
