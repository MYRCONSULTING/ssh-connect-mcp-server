#!/usr/bin/env python3
"""
Install SSH MCP server in Claude Desktop configuration.

This script installs the SSH MCP server in the Claude Desktop configuration file.
It prompts the user for SSH connection parameters and updates the configuration file.
"""

import json
import os
import sys
from pathlib import Path

def get_claude_config_path():
    """Get the path to the Claude Desktop configuration file."""
    home = Path.home()
    
    # Check for macOS
    if sys.platform == "darwin":
        config_path = home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        if config_path.exists():
            return config_path
    
    # Check for Windows
    elif sys.platform == "win32":
        config_path = home / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
        if config_path.exists():
            return config_path
    
    # Check for Linux
    elif sys.platform.startswith("linux"):
        config_path = home / ".config" / "Claude" / "claude_desktop_config.json"
        if config_path.exists():
            return config_path
    
    return None

def get_ssh_params():
    """Prompt the user for SSH connection parameters."""
    print("Enter SSH connection parameters:")
    host = input("SSH host: ")
    port = input("SSH port [22]: ") or "22"
    username = input("SSH username: ")
    
    auth_type = input("Authentication type (password/key) [password]: ") or "password"
    
    if auth_type.lower() == "password":
        password = input("SSH password: ")
        key_path = ""
        key_passphrase = ""
    else:
        password = ""
        key_path = input("SSH key path: ")
        key_passphrase = input("SSH key passphrase (leave empty if none): ")
    
    return {
        "SSH_HOST": host,
        "SSH_PORT": port,
        "SSH_USERNAME": username,
        "SSH_PASSWORD": password,
        "SSH_KEY_PATH": key_path,
        "SSH_KEY_PASSPHRASE": key_passphrase
    }

def install_ssh_mcp():
    """Install SSH MCP server in Claude Desktop configuration."""
    # Get the path to the Claude Desktop configuration file
    config_path = get_claude_config_path()
    if not config_path:
        print("Error: Could not find Claude Desktop configuration file.")
        print("Please make sure Claude Desktop is installed and has been run at least once.")
        return False
    
    # Get SSH connection parameters
    ssh_params = get_ssh_params()
    
    # Clean up empty parameters
    ssh_params = {k: v for k, v in ssh_params.items() if v}
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Read the current configuration
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        config = {}
    
    # Initialize mcpServers if it doesn't exist
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    # Add or update the SSH MCP server
    config["mcpServers"]["ssh-connect"] = {
        "command": "uv",
        "args": [
            "--directory",
            current_dir,
            "run",
            "ssh-connect"
        ],
        "env": ssh_params,
        "disabled": False,
        "autoApprove": []
    }
    
    # Write the updated configuration
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"SSH MCP server installed in {config_path}")
        return True
    except Exception as e:
        print(f"Error writing configuration file: {e}")
        return False

if __name__ == "__main__":
    print("SSH MCP Server Installer for Claude Desktop")
    print("=========================================")
    print()
    
    if install_ssh_mcp():
        print()
        print("Installation successful!")
        print("You can now use the SSH MCP server with Claude Desktop.")
        print("Please restart Claude Desktop to apply the changes.")
    else:
        print()
        print("Installation failed.")
        print("Please check the error message and try again.")
