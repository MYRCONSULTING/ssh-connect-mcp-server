#!/bin/bash
# Install dependencies for SSH MCP server

echo "Installing dependencies for SSH MCP server..."
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed."
    echo "Please install uv first: https://github.com/astral-sh/uv"
    exit 1
fi

# Install paramiko
echo "Installing paramiko..."
uv pip install paramiko

echo ""
echo "Dependencies installed successfully!"
echo "You can now use the SSH MCP server."
echo ""
echo "To install the SSH MCP server in Cline:"
echo "./install_ssh_mcp.py"
echo ""
echo "To install the SSH MCP server in Claude Desktop:"
echo "./install_ssh_mcp_claude.py"
