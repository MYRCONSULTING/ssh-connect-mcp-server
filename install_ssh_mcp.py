#!/usr/bin/env python3
"""
Install SSH MCP server in Cline MCP settings.

This script installs the SSH MCP server in the Cline MCP settings file.
It prompts the user for SSH connection parameters and updates the settings file.
"""

import json
import os
import sys
from pathlib import Path

def get_cline_settings_path():
    """Get the path to the Cline MCP settings file."""
    home = Path.home()
    
    # Check for macOS
    if sys.platform == "darwin":
        settings_path = home / "Library" / "Application Support" / "Code" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"
        if settings_path.exists():
            return settings_path
    
    # Check for Windows
    elif sys.platform == "win32":
        settings_path = home / "AppData" / "Roaming" / "Code" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"
        if settings_path.exists():
            return settings_path
    
    # Check for Linux
    elif sys.platform.startswith("linux"):
        settings_path = home / ".config" / "Code" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"
        if settings_path.exists():
            return settings_path
    
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
    """Install SSH MCP server in Cline MCP settings."""
    # Get the path to the Cline MCP settings file
    settings_path = get_cline_settings_path()
    if not settings_path:
        print("Error: Could not find Cline MCP settings file.")
        return False
    
    # Get SSH connection parameters
    ssh_params = get_ssh_params()
    
    # Clean up empty parameters
    ssh_params = {k: v for k, v in ssh_params.items() if v}
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Read the current settings
    try:
        with open(settings_path, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {"mcpServers": {}}
    
    # Add or update the SSH MCP server
    settings["mcpServers"]["ssh-connect"] = {
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
    
    # Write the updated settings
    try:
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=2)
        print(f"SSH MCP server installed in {settings_path}")
        return True
    except Exception as e:
        print(f"Error writing settings file: {e}")
        return False

if __name__ == "__main__":
    print("SSH MCP Server Installer")
    print("=======================")
    print()
    
    if install_ssh_mcp():
        print()
        print("Installation successful!")
        print("You can now use the SSH MCP server with Cline.")
        print("Run ./test_ssh_mcp.sh to test the SSH MCP server.")
    else:
        print()
        print("Installation failed.")
        print("Please check the error message and try again.")
