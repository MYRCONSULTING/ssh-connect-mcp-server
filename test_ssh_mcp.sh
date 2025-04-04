#!/bin/bash
# Test script for SSH MCP server with Cline

# Create a test file
echo "Creating test file..."
python create_test_file.py

# Display instructions
echo ""
echo "=== SSH MCP Server Test Instructions ==="
echo ""
echo "1. Open Cline and run the following commands to test the SSH MCP server:"
echo ""
echo "   a. Connect to the SSH server:"
echo "      use_mcp_tool(server_name=\"ssh-connect\", tool_name=\"connect\", arguments={})"
echo ""
echo "   b. Execute a command to list files:"
echo "      use_mcp_tool(server_name=\"ssh-connect\", tool_name=\"execute\", arguments={\"command\": \"ls -la\"})"
echo ""
echo "   c. Upload the test file:"
echo "      use_mcp_tool(server_name=\"ssh-connect\", tool_name=\"upload\", arguments={\"local_path\": \"$(pwd)/test_file.txt\", \"remote_path\": \"/home/lanuser/test_file.txt\"})"
echo ""
echo "   d. List files to verify upload:"
echo "      use_mcp_tool(server_name=\"ssh-connect\", tool_name=\"list_files\", arguments={\"path\": \"/home/lanuser\"})"
echo ""
echo "   e. Download the file to a different location:"
echo "      use_mcp_tool(server_name=\"ssh-connect\", tool_name=\"download\", arguments={\"remote_path\": \"/home/lanuser/test_file.txt\", \"local_path\": \"$(pwd)/downloaded_test_file.txt\"})"
echo ""
echo "   f. Disconnect from the SSH server:"
echo "      use_mcp_tool(server_name=\"ssh-connect\", tool_name=\"disconnect\", arguments={})"
echo ""
echo "2. After testing, you can verify that the file was downloaded by checking for 'downloaded_test_file.txt' in the current directory."
echo ""
echo "For more examples and usage information, see the 'cline_ssh_usage_example.md' file."
echo ""
echo "Opening the SSH MCP guide in your browser..."
open ssh_mcp_guide.html
