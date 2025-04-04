#!/usr/bin/env python3
"""
Example script demonstrating how to use the SSH MCP server.

This script shows how to:
1. Connect to an SSH server
2. Execute commands
3. Upload and download files
4. List files in a directory
5. Disconnect from the server

Note: This script assumes the SSH MCP server is already configured and running.
"""

import json
import os
import sys
import subprocess
import tempfile

# Path to the MCP server executable
MCP_SERVER_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src/ssh_connect")

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
    
    # Write the request to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        json.dump(request, f)
        request_file = f.name
    
    # Call the MCP server with the request
    result = subprocess.run(
        [sys.executable, "-m", "ssh_connect"],
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

def main():
    """Run the SSH example."""
    print("SSH MCP Server Example")
    print("=====================")
    
    # Connect to SSH server
    print("\n1. Connecting to SSH server...")
    result = call_mcp_tool("connect")
    print(result)
    
    # Execute a command
    print("\n2. Executing command 'ls -la'...")
    result = call_mcp_tool("execute", {"command": "ls -la"})
    print(result)
    
    # Create a test file to upload
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("This is a test file for SSH MCP server example.")
        local_file = f.name
    
    # Upload the file
    print(f"\n3. Uploading file {local_file} to remote server...")
    result = call_mcp_tool("upload", {
        "local_path": local_file,
        "remote_path": "test_upload.txt"
    })
    print(result)
    
    # List files to verify upload
    print("\n4. Listing files in current directory...")
    result = call_mcp_tool("list_files", {"path": "."})
    print(result)
    
    # Download the file to a different location
    download_path = local_file + ".downloaded"
    print(f"\n5. Downloading file test_upload.txt to {download_path}...")
    result = call_mcp_tool("download", {
        "remote_path": "test_upload.txt",
        "local_path": download_path
    })
    print(result)
    
    # Verify the downloaded file
    if os.path.exists(download_path):
        with open(download_path, 'r') as f:
            content = f.read()
        print(f"Downloaded file content: {content}")
    
    # Clean up local files
    os.unlink(local_file)
    os.unlink(download_path)
    
    # Execute command to remove the remote file
    print("\n6. Removing remote file...")
    result = call_mcp_tool("execute", {"command": "rm test_upload.txt"})
    print(result)
    
    # Disconnect from SSH server
    print("\n7. Disconnecting from SSH server...")
    result = call_mcp_tool("disconnect")
    print(result)

if __name__ == "__main__":
    main()
