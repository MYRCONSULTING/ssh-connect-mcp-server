#!/usr/bin/env python3
"""
Test script for the SSH MCP server.

This script tests the basic functionality of the SSH MCP server by:
1. Checking if the server can be imported
2. Verifying that the server can list tools
3. Testing that the server can handle tool calls (with mock responses)

Note: This is a basic test and does not actually connect to an SSH server.
"""

import asyncio
import json
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ssh_connect import server

class TestSSHConnect(unittest.TestCase):
    """Test cases for the SSH MCP server."""

    def test_import(self):
        """Test that the server module can be imported."""
        self.assertIsNotNone(server)
        self.assertIsNotNone(server.main)

    async def async_test_list_tools(self):
        """Test that the server can list tools."""
        tools = await server.handle_list_tools()
        self.assertIsNotNone(tools)
        self.assertGreater(len(tools), 0)
        
        # Check that the expected tools are present
        tool_names = [tool.name for tool in tools]
        expected_tools = ["connect", "disconnect", "execute", "upload", "download", "list_files"]
        for tool in expected_tools:
            self.assertIn(tool, tool_names)

    def test_list_tools(self):
        """Run the async test for listing tools."""
        asyncio.run(self.async_test_list_tools())

    @patch('paramiko.SSHClient')
    async def async_test_connect(self, mock_ssh_client):
        """Test that the server can handle connect tool calls."""
        # Mock the SSH client
        mock_instance = MagicMock()
        mock_ssh_client.return_value = mock_instance
        mock_instance.open_sftp.return_value = MagicMock()
        
        # Set environment variables for testing
        os.environ["SSH_HOST"] = "test.example.com"
        os.environ["SSH_USERNAME"] = "testuser"
        os.environ["SSH_PASSWORD"] = "testpass"
        
        # Call the connect tool
        result = await server.handle_call_tool("connect", {})
        
        # Check the result
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, "text")
        self.assertIn("Connected to", result[0].text)
        
        # Verify that the SSH client was called with the correct arguments
        mock_ssh_client.assert_called_once()
        mock_instance.connect.assert_called_once()
        connect_args = mock_instance.connect.call_args[1]
        self.assertEqual(connect_args["hostname"], "test.example.com")
        self.assertEqual(connect_args["username"], "testuser")
        self.assertEqual(connect_args["password"], "testpass")

    @patch('paramiko.SSHClient')
    def test_connect(self, mock_ssh_client):
        """Run the async test for connect tool."""
        asyncio.run(self.async_test_connect(mock_ssh_client))

    @patch('paramiko.SSHClient')
    async def async_test_execute(self, mock_ssh_client):
        """Test that the server can handle execute tool calls."""
        # Mock the SSH client and channel
        mock_instance = MagicMock()
        mock_ssh_client.return_value = mock_instance
        
        # Mock exec_command
        mock_stdin = MagicMock()
        mock_stdout = MagicMock()
        mock_stderr = MagicMock()
        mock_stdout.read.return_value = b"Test output"
        mock_stderr.read.return_value = b""
        mock_stdout.channel.recv_exit_status.return_value = 0
        mock_instance.exec_command.return_value = (mock_stdin, mock_stdout, mock_stderr)
        
        # Set the global ssh_client
        server.ssh_client = mock_instance
        
        # Call the execute tool
        result = await server.handle_call_tool("execute", {"command": "ls -la"})
        
        # Check the result
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, "text")
        self.assertIn("Command: ls -la", result[0].text)
        self.assertIn("Exit status: 0", result[0].text)
        self.assertIn("Test output", result[0].text)
        
        # Verify that exec_command was called with the correct arguments
        mock_instance.exec_command.assert_called_once_with("ls -la", timeout=60)

    @patch('paramiko.SSHClient')
    def test_execute(self, mock_ssh_client):
        """Run the async test for execute tool."""
        asyncio.run(self.async_test_execute(mock_ssh_client))

if __name__ == "__main__":
    unittest.main()
