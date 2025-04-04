#!/bin/bash
# Setup and test SSH MCP server

echo "SSH MCP Server Setup and Test"
echo "============================"
echo ""

# Step 1: Install dependencies
echo "Step 1: Installing dependencies..."
./install_dependencies.sh

# Step 2: Install SSH MCP server
echo ""
echo "Step 2: Installing SSH MCP server..."
echo ""
echo "Choose where to install the SSH MCP server:"
echo "1. Cline"
echo "2. Claude Desktop"
echo "3. Both"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        ./install_ssh_mcp.py
        ;;
    2)
        ./install_ssh_mcp_claude.py
        ;;
    3)
        ./install_ssh_mcp.py
        ./install_ssh_mcp_claude.py
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

# Step 3: Test SSH MCP server
echo ""
echo "Step 3: Testing SSH MCP server..."
echo ""
echo "Choose how to test the SSH MCP server:"
echo "1. Run test script (test_ssh_mcp.sh)"
echo "2. Run Python test script (test_ssh_mcp.py)"
echo "3. Skip testing"
echo ""
read -p "Enter your choice (1-3): " test_choice

case $test_choice in
    1)
        ./test_ssh_mcp.sh
        ;;
    2)
        ./test_ssh_mcp.py
        ;;
    3)
        echo "Skipping testing."
        ;;
    *)
        echo "Invalid choice. Skipping testing."
        ;;
esac

echo ""
echo "Setup and test completed!"
echo "You can now use the SSH MCP server with Cline or Claude Desktop."
echo ""
echo "For more information, see the README.md file or the SSH MCP guide:"
echo "open ssh_mcp_guide.html"
