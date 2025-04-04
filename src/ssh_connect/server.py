import os
from typing import Any, Dict, Optional

import mcp.server.stdio
import mcp.types as types
import paramiko
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# SSH connection state
ssh_client: Optional[paramiko.SSHClient] = None
sftp_client: Optional[paramiko.SFTPClient] = None

# Get SSH configuration from environment variables
SSH_HOST = os.environ.get("SSH_HOST", "")
SSH_PORT = int(os.environ.get("SSH_PORT", "22"))
SSH_USERNAME = os.environ.get("SSH_USERNAME", "")
SSH_PASSWORD = os.environ.get("SSH_PASSWORD", "")
SSH_KEY_PATH = os.environ.get("SSH_KEY_PATH", "")
SSH_KEY_PASSPHRASE = os.environ.get("SSH_KEY_PASSPHRASE", "")

server = Server("ssh-connect")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available SSH tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="connect",
            description="Connect to SSH server",
            inputSchema={
                "type": "object",
                "properties": {
                    "host": {
                        "type": "string",
                        "description": "SSH host (overrides environment variable)",
                    },
                    "port": {
                        "type": "integer",
                        "description": "SSH port (overrides environment variable)",
                    },
                    "username": {
                        "type": "string",
                        "description": "SSH username (overrides environment variable)",
                    },
                    "password": {
                        "type": "string",
                        "description": "SSH password (overrides environment variable)",
                    },
                    "key_path": {
                        "type": "string",
                        "description": "Path to SSH key file (overrides environment variable)",
                    },
                    "key_passphrase": {
                        "type": "string",
                        "description": "Passphrase for SSH key (overrides environment variable)",
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="disconnect",
            description="Disconnect from SSH server",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="execute",
            description="Execute command on SSH server",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Command to execute"},
                    "timeout": {
                        "type": "integer",
                        "description": "Command timeout in seconds (default: 60)",
                    },
                },
                "required": ["command"],
            },
        ),
        types.Tool(
            name="upload",
            description="Upload file to SSH server",
            inputSchema={
                "type": "object",
                "properties": {
                    "local_path": {"type": "string", "description": "Local file path"},
                    "remote_path": {
                        "type": "string",
                        "description": "Remote file path",
                    },
                },
                "required": ["local_path", "remote_path"],
            },
        ),
        types.Tool(
            name="download",
            description="Download file from SSH server",
            inputSchema={
                "type": "object",
                "properties": {
                    "remote_path": {
                        "type": "string",
                        "description": "Remote file path",
                    },
                    "local_path": {"type": "string", "description": "Local file path"},
                },
                "required": ["remote_path", "local_path"],
            },
        ),
        types.Tool(
            name="list_files",
            description="List files in directory on SSH server",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path"},
                },
                "required": ["path"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle SSH tool execution requests.
    """
    global ssh_client, sftp_client

    if arguments is None:
        arguments = {}

    try:
        if name == "connect":
            return await handle_connect(arguments)
        elif name == "disconnect":
            return await handle_disconnect()
        elif name == "execute":
            return await handle_execute(arguments)
        elif name == "upload":
            return await handle_upload(arguments)
        elif name == "download":
            return await handle_download(arguments)
        elif name == "list_files":
            return await handle_list_files(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        return [
            types.TextContent(
                type="text",
                text=f"Error: {str(e)}",
            )
        ]


async def handle_connect(arguments: Dict[str, Any]) -> list[types.TextContent]:
    """Connect to SSH server"""
    global ssh_client, sftp_client

    # Close existing connection if any
    if ssh_client:
        ssh_client.close()
        ssh_client = None
    if sftp_client:
        sftp_client.close()
        sftp_client = None

    # Get connection parameters (override env vars with arguments if provided)
    host = arguments.get("host", SSH_HOST)
    port = arguments.get("port", SSH_PORT)
    username = arguments.get("username", SSH_USERNAME)
    password = arguments.get("password", SSH_PASSWORD)
    key_path = arguments.get("key_path", SSH_KEY_PATH)
    key_passphrase = arguments.get("key_passphrase", SSH_KEY_PASSPHRASE)

    if not host:
        raise ValueError("SSH host is required")
    if not username:
        raise ValueError("SSH username is required")
    if not password and not key_path:
        raise ValueError("Either SSH password or key path is required")

    # Create SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if key_path:
            # Connect with key authentication
            key = paramiko.RSAKey.from_private_key_file(
                key_path, password=key_passphrase if key_passphrase else None
            )
            ssh_client.connect(
                hostname=host, port=port, username=username, pkey=key, timeout=10
            )
        else:
            # Connect with password authentication
            ssh_client.connect(
                hostname=host,
                port=port,
                username=username,
                password=password,
                timeout=10,
            )

        # Create SFTP client
        sftp_client = ssh_client.open_sftp()

        return [
            types.TextContent(
                type="text",
                text=f"Connected to {username}@{host}:{port}",
            )
        ]
    except Exception as e:
        if ssh_client:
            ssh_client.close()
            ssh_client = None
        raise ValueError(f"Failed to connect: {str(e)}")


async def handle_disconnect() -> list[types.TextContent]:
    """Disconnect from SSH server"""
    global ssh_client, sftp_client

    if sftp_client:
        sftp_client.close()
        sftp_client = None

    if ssh_client:
        ssh_client.close()
        ssh_client = None
        return [
            types.TextContent(
                type="text",
                text="Disconnected from SSH server",
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text="Not connected to any SSH server",
            )
        ]


async def handle_execute(arguments: Dict[str, Any]) -> list[types.TextContent]:
    """Execute command on SSH server"""
    global ssh_client

    if not ssh_client:
        raise ValueError("Not connected to SSH server")

    command = arguments.get("command")
    if not command:
        raise ValueError("Command is required")

    timeout = arguments.get("timeout", 60)

    stdin, stdout, stderr = ssh_client.exec_command(command, timeout=timeout)

    stdout_data = stdout.read().decode("utf-8")
    stderr_data = stderr.read().decode("utf-8")
    exit_status = stdout.channel.recv_exit_status()

    result = f"Command: {command}\n"
    result += f"Exit status: {exit_status}\n\n"

    if stdout_data:
        result += f"STDOUT:\n{stdout_data}\n"

    if stderr_data:
        result += f"STDERR:\n{stderr_data}\n"

    return [
        types.TextContent(
            type="text",
            text=result,
        )
    ]


async def handle_upload(arguments: Dict[str, Any]) -> list[types.TextContent]:
    """Upload file to SSH server"""
    global sftp_client

    if not sftp_client:
        raise ValueError("Not connected to SSH server")

    local_path = arguments.get("local_path")
    remote_path = arguments.get("remote_path")

    if not local_path or not remote_path:
        raise ValueError("Local and remote paths are required")

    try:
        sftp_client.put(local_path, remote_path)
        return [
            types.TextContent(
                type="text",
                text=f"Uploaded {local_path} to {remote_path}",
            )
        ]
    except Exception as e:
        raise ValueError(f"Failed to upload file: {str(e)}")


async def handle_download(arguments: Dict[str, Any]) -> list[types.TextContent]:
    """Download file from SSH server"""
    global sftp_client

    if not sftp_client:
        raise ValueError("Not connected to SSH server")

    remote_path = arguments.get("remote_path")
    local_path = arguments.get("local_path")

    if not remote_path or not local_path:
        raise ValueError("Remote and local paths are required")

    try:
        sftp_client.get(remote_path, local_path)
        return [
            types.TextContent(
                type="text",
                text=f"Downloaded {remote_path} to {local_path}",
            )
        ]
    except Exception as e:
        raise ValueError(f"Failed to download file: {str(e)}")


async def handle_list_files(arguments: Dict[str, Any]) -> list[types.TextContent]:
    """List files in directory on SSH server"""
    global sftp_client

    if not sftp_client:
        raise ValueError("Not connected to SSH server")

    path = arguments.get("path")
    if not path:
        raise ValueError("Path is required")

    try:
        file_list = sftp_client.listdir(path)
        file_info = []

        for filename in file_list:
            full_path = f"{path}/{filename}"
            try:
                stat = sftp_client.stat(full_path)
                is_dir = stat.st_mode & 0o40000 != 0  # Check if it's a directory
                size = stat.st_size
                file_type = "directory" if is_dir else "file"
                file_info.append(f"{filename} ({file_type}, {size} bytes)")
            except:
                file_info.append(f"{filename}")

        result = f"Files in {path}:\n" + "\n".join(file_info)
        return [
            types.TextContent(
                type="text",
                text=result,
            )
        ]
    except Exception as e:
        raise ValueError(f"Failed to list files: {str(e)}")


async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ssh-connect",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
