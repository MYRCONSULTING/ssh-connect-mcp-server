# SSH MCP Server Usage with Cline

This document provides quick examples of how to use the SSH MCP server with Cline.

## Available Tools

The SSH MCP server provides the following tools:

1. **connect**: Connect to an SSH server
2. **disconnect**: Disconnect from the SSH server
3. **execute**: Execute a command on the SSH server
4. **upload**: Upload a file to the SSH server
5. **download**: Download a file from the SSH server
6. **list_files**: List files in a directory on the SSH server

## Example Usage

### Connect to SSH Server

```
use_mcp_tool(server_name="ssh-connect", tool_name="connect", arguments={})
```

### Execute a Command

```
use_mcp_tool(server_name="ssh-connect", tool_name="execute", arguments={"command": "ls -la"})
```

### List Files in a Directory

```
use_mcp_tool(server_name="ssh-connect", tool_name="list_files", arguments={"path": "/home/user"})
```

### Upload a File

```
use_mcp_tool(server_name="ssh-connect", tool_name="upload", arguments={"local_path": "/path/to/local/file", "remote_path": "/path/to/remote/file"})
```

### Download a File

```
use_mcp_tool(server_name="ssh-connect", tool_name="download", arguments={"remote_path": "/path/to/remote/file", "local_path": "/path/to/local/file"})
```

### Disconnect from SSH Server

```
use_mcp_tool(server_name="ssh-connect", tool_name="disconnect", arguments={})
```

## Complete Example Workflow

Here's a complete example workflow:

1. Connect to the SSH server:
   ```
   use_mcp_tool(server_name="ssh-connect", tool_name="connect", arguments={})
   ```

2. Execute a command:
   ```
   use_mcp_tool(server_name="ssh-connect", tool_name="execute", arguments={"command": "ls -la"})
   ```

3. Upload a file:
   ```
   use_mcp_tool(server_name="ssh-connect", tool_name="upload", arguments={"local_path": "example.txt", "remote_path": "/home/user/example.txt"})
   ```

4. List files to verify upload:
   ```
   use_mcp_tool(server_name="ssh-connect", tool_name="list_files", arguments={"path": "/home/user"})
   ```

5. Download a file:
   ```
   use_mcp_tool(server_name="ssh-connect", tool_name="download", arguments={"remote_path": "/home/user/example.txt", "local_path": "downloaded_example.txt"})
   ```

6. Disconnect from the SSH server:
   ```
   use_mcp_tool(server_name="ssh-connect", tool_name="disconnect", arguments={})
   ```
