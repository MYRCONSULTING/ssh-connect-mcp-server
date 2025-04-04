# ssh-connect MCP server

** **All of the code in this project was created by a generative AI.** **

An MCP server for SSH connections and file operations.

## Components

### Tools

The server implements several SSH-related tools:

- **connect**: Connect to an SSH server
  - Optional parameters to override environment variables: host, port, username, password, key_path, key_passphrase
  - Returns connection status

- **disconnect**: Disconnect from the SSH server
  - No parameters required
  - Returns disconnection status

- **execute**: Execute a command on the SSH server
  - Required parameter: command (string)
  - Optional parameter: timeout (integer, seconds, default: 60)
  - Returns command output (stdout and stderr) and exit status

- **upload**: Upload a file to the SSH server
  - Required parameters: local_path, remote_path
  - Returns upload status

- **download**: Download a file from the SSH server
  - Required parameters: remote_path, local_path
  - Returns download status

- **list_files**: List files in a directory on the SSH server
  - Required parameter: path
  - Returns list of files with type and size information

## Configuration

The SSH connection parameters can be configured using environment variables in the MCP settings:

- `SSH_HOST`: SSH server hostname or IP address
- `SSH_PORT`: SSH server port (default: 22)
- `SSH_USERNAME`: SSH username
- `SSH_PASSWORD`: SSH password (if using password authentication)
- `SSH_KEY_PATH`: Path to SSH private key file (if using key authentication)
- `SSH_KEY_PASSPHRASE`: Passphrase for SSH private key (if required)

You must provide either `SSH_PASSWORD` or `SSH_KEY_PATH` for authentication.

### Example Configuration

An example MCP configuration file is provided in `mcp-config-example.json`. You can use this as a template for configuring the SSH MCP server:

```json
{
  "mcpServers": {
    "ssh-connect": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/ssh-connect",
        "run",
        "ssh-connect"
      ],
      "env": {
        "SSH_HOST": "example.com",
        "SSH_PORT": "22",
        "SSH_USERNAME": "username",
        "SSH_PASSWORD": "password",
        "SSH_KEY_PATH": "/path/to/private_key",
        "SSH_KEY_PASSPHRASE": "key_passphrase"
      }
    }
  }
}
```

Note: You typically only need to provide either `SSH_PASSWORD` or `SSH_KEY_PATH` (with optional `SSH_KEY_PASSPHRASE`), not both.

## Examples

An example Python script is provided in the `examples` directory to demonstrate how to use the SSH MCP server:

- `ssh_example.py`: Shows how to connect to an SSH server, execute commands, upload/download files, list directory contents, and disconnect.

To run the example:

```bash
python examples/ssh_example.py
```

This example assumes the SSH MCP server is already configured and running.

### Using with Cline

To help Cline understand how to use the SSH MCP server without reading the README.md file, the following files are provided:

- `cline_ssh_usage_example.md`: A quick reference guide for using the SSH MCP server with Cline, including example commands and a complete workflow.
- `create_test_file.py`: A script to create a test file for upload/download testing.
- `test_ssh_mcp.sh`: A shell script that creates a test file and provides step-by-step instructions for testing the SSH MCP server with Cline.
- `test_ssh_mcp.py`: A Python script that demonstrates how to use the SSH MCP server directly from Python, without using Cline.
- `ssh_mcp_guide.html`: An HTML guide with examples and a complete workflow for using the SSH MCP server with Cline.

To test the SSH MCP server with Cline:

```bash
./test_ssh_mcp.sh
```

This will create a test file and display instructions for testing the SSH MCP server with Cline.

To test the SSH MCP server directly from Python:

```bash
./test_ssh_mcp.py
```

This will perform a complete test of the SSH MCP server, including connecting, executing commands, uploading/downloading files, and disconnecting.

## Quickstart

### Install

#### All-in-One Setup

For a complete setup and test of the SSH MCP server, you can use the all-in-one setup script:

```bash
./setup_and_test.sh
```

This script will:
1. Install the required dependencies
2. Install the SSH MCP server in Cline or Claude Desktop (or both)
3. Test the SSH MCP server

#### Manual Setup

##### Dependencies

Before using the SSH MCP server, you need to install the required dependencies:

```bash
./install_dependencies.sh
```

This script will install the paramiko Python package, which is required for SSH connections.

##### Automatic Installation

Two Python scripts are provided to automatically install the SSH MCP server:

1. For Cline:
```bash
./install_ssh_mcp.py
```

2. For Claude Desktop:
```bash
./install_ssh_mcp_claude.py
```

These scripts will:
1. Detect the location of the configuration file
2. Prompt you for SSH connection parameters
3. Update the configuration file with the SSH MCP server configuration

#### Manual Installation

##### Claude Desktop

An example Claude Desktop configuration file is provided in `claude-desktop-config-example.json`. This shows how to configure the SSH MCP server in Claude Desktop.

To install the SSH MCP server in Claude Desktop:

1. Locate your Claude Desktop configuration file:
   - On macOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
   - On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

2. Add the SSH MCP server configuration to the `mcpServers` object in the configuration file:

```json
{
  "mcpServers": {
    "ssh-connect": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/ssh-connect",
        "run",
        "ssh-connect"
      ],
      "env": {
        "SSH_HOST": "example.com",
        "SSH_PORT": "22",
        "SSH_USERNAME": "username",
        "SSH_PASSWORD": "password",
        "SSH_KEY_PATH": "/path/to/private_key",
        "SSH_KEY_PASSPHRASE": "key_passphrase"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

3. Restart Claude Desktop to apply the changes.

Note: Make sure to replace the placeholder values with your actual SSH connection details.

## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

### Testing

A test script is provided in the `tests` directory to verify that the SSH MCP server is working correctly:

```bash
python tests/test_ssh_connect.py
```

This test script uses unittest and mocking to test the basic functionality of the SSH MCP server without actually connecting to an SSH server.

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).

You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory /path/to/ssh-connect run ssh-connect
```

Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.
