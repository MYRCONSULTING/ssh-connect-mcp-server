# ClineでのSSH MCPサーバーの使用方法

このドキュメントでは、ClineでSSH MCPサーバーを使用するための簡単な例を提供します。

## 利用可能なツール

SSH MCPサーバーは以下のツールを提供しています：

1. **connect**: SSHサーバーに接続
2. **disconnect**: SSHサーバーから切断
3. **execute**: SSHサーバーでコマンドを実行
4. **upload**: ファイルをSSHサーバーにアップロード
5. **download**: SSHサーバーからファイルをダウンロード
6. **list_files**: SSHサーバー上のディレクトリ内のファイルを一覧表示

## 使用例

### SSHサーバーに接続

```
use_mcp_tool(server_name="ssh-connect", tool_name="connect", arguments={})
```

### コマンドを実行

```
use_mcp_tool(server_name="ssh-connect", tool_name="execute", arguments={"command": "ls -la"})
```

### ディレクトリ内のファイルを一覧表示

```
use_mcp_tool(server_name="ssh-connect", tool_name="list_files", arguments={"path": "/home/user"})
```

### ファイルをアップロード

```
use_mcp_tool(server_name="ssh-connect", tool_name="upload", arguments={"local_path": "/path/to/local/file", "remote_path": "/path/to/remote/file"})
```

### ファイルをダウンロード

```
use_mcp_tool(server_name="ssh-connect", tool_name="download", arguments={"remote_path": "/path/to/remote/file", "local_path": "/path/to/local/file"})
```

### SSHサーバーから切断

```
use_mcp_tool(server_name="ssh-connect", tool_name="disconnect", arguments={})
```

## 完全なワークフロー例

以下は完全なワークフロー例です：

1. SSHサーバーに接続：
   ```
   use_mcp_tool(server_name="ssh-connect", tool_name="connect", arguments={})
   ```

2. コマンドを実行：
   ```
   use_mcp_tool(server_name="ssh-connect", tool_name="execute", arguments={"command": "ls -la"})
   ```

3. ファイルをアップロード：
   ```
   use_mcp_tool(server_name="ssh-connect", tool_name="upload", arguments={"local_path": "example.txt", "remote_path": "/home/user/example.txt"})
   ```

4. アップロードを確認するためにファイルを一覧表示：
   ```
   use_mcp_tool(server_name="ssh-connect", tool_name="list_files", arguments={"path": "/home/user"})
   ```

5. ファイルをダウンロード：
   ```
   use_mcp_tool(server_name="ssh-connect", tool_name="download", arguments={"remote_path": "/home/user/example.txt", "local_path": "downloaded_example.txt"})
   ```

6. SSHサーバーから切断：
   ```
   use_mcp_tool(server_name="ssh-connect", tool_name="disconnect", arguments={})
   ```
