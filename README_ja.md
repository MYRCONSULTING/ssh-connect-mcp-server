# ssh-connect MCPサーバー

** **このプロジェクトのコードは全て生成AIによって作られたものです。** **

SSH接続とファイル操作のためのMCPサーバー。

## コンポーネント

### ツール

サーバーは以下のSSH関連ツールを実装しています：

- **connect**: SSHサーバーに接続
  - 環境変数を上書きするためのオプションパラメータ: host, port, username, password, key_path, key_passphrase
  - 接続ステータスを返します

- **disconnect**: SSHサーバーから切断
  - パラメータは不要
  - 切断ステータスを返します

- **execute**: SSHサーバーでコマンドを実行
  - 必須パラメータ: command (文字列)
  - オプションパラメータ: timeout (整数、秒単位、デフォルト: 60)
  - コマンド出力 (stdout と stderr) と終了ステータスを返します

- **upload**: ファイルをSSHサーバーにアップロード
  - 必須パラメータ: local_path, remote_path
  - アップロードステータスを返します

- **download**: SSHサーバーからファイルをダウンロード
  - 必須パラメータ: remote_path, local_path
  - ダウンロードステータスを返します

- **list_files**: SSHサーバー上のディレクトリ内のファイルを一覧表示
  - 必須パラメータ: path
  - ファイルの種類とサイズ情報を含むファイルリストを返します

## 設定

SSH接続パラメータはMCP設定の環境変数を使用して設定できます：

- `SSH_HOST`: SSHサーバーのホスト名またはIPアドレス
- `SSH_PORT`: SSHサーバーのポート (デフォルト: 22)
- `SSH_USERNAME`: SSHユーザー名
- `SSH_PASSWORD`: SSHパスワード (パスワード認証を使用する場合)
- `SSH_KEY_PATH`: SSH秘密鍵ファイルへのパス (鍵認証を使用する場合)
- `SSH_KEY_PASSPHRASE`: SSH秘密鍵のパスフレーズ (必要な場合)

認証には `SSH_PASSWORD` または `SSH_KEY_PATH` のいずれかを提供する必要があります。

### 設定例

SSH MCPサーバーを設定するためのテンプレートとして使用できる例のMCP設定ファイルが `mcp-config-example.json` に提供されています：

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

注意: 通常は `SSH_PASSWORD` または `SSH_KEY_PATH` (オプションで `SSH_KEY_PASSPHRASE`) のいずれかを提供するだけで十分です。両方を提供する必要はありません。

## 例

SSH MCPサーバーの使用方法を示す例のPythonスクリプトが `examples` ディレクトリに提供されています：

- `ssh_example.py`: SSHサーバーへの接続、コマンドの実行、ファイルのアップロード/ダウンロード、ディレクトリ内容の一覧表示、切断の方法を示します。

例を実行するには：

```bash
python examples/ssh_example.py
```

この例では、SSH MCPサーバーが既に設定され実行されていることを前提としています。

### Clineでの使用

README.mdファイルを読まなくてもClineがSSH MCPサーバーの使用方法を理解できるように、以下のファイルが提供されています：

- `cline_ssh_usage_example.md`: 例のコマンドと完全なワークフローを含む、ClineでのSSH MCPサーバーの使用に関するクイックリファレンスガイド。
- `create_test_file.py`: アップロード/ダウンロードテスト用のテストファイルを作成するスクリプト。
- `test_ssh_mcp.sh`: テストファイルを作成し、ClineでSSH MCPサーバーをテストするためのステップバイステップの手順を提供するシェルスクリプト。
- `test_ssh_mcp.py`: Clineを使用せずに、直接PythonからSSH MCPサーバーを使用する方法を示すPythonスクリプト。
- `ssh_mcp_guide.html`: ClineでのSSH MCPサーバーの使用に関する例と完全なワークフローを含むHTMLガイド。

ClineでSSH MCPサーバーをテストするには：

```bash
./test_ssh_mcp.sh
```

これにより、テストファイルが作成され、ClineでSSH MCPサーバーをテストするための手順が表示されます。

PythonからSSH MCPサーバーを直接テストするには：

```bash
./test_ssh_mcp.py
```

これにより、接続、コマンドの実行、ファイルのアップロード/ダウンロード、切断を含む、SSH MCPサーバーの完全なテストが実行されます。

## クイックスタート

### インストール

#### オールインワンセットアップ

SSH MCPサーバーの完全なセットアップとテストには、オールインワンセットアップスクリプトを使用できます：

```bash
./setup_and_test.sh
```

このスクリプトは以下を行います：
1. 必要な依存関係をインストール
2. SSH MCPサーバーをClineまたはClaude Desktop（あるいは両方）にインストール
3. SSH MCPサーバーをテスト

#### 手動セットアップ

##### 依存関係

SSH MCPサーバーを使用する前に、必要な依存関係をインストールする必要があります：

```bash
./install_dependencies.sh
```

このスクリプトは、SSH接続に必要なparamiko Pythonパッケージをインストールします。

##### 自動インストール

SSH MCPサーバーを自動的にインストールするための2つのPythonスクリプトが提供されています：

1. Cline用：
```bash
./install_ssh_mcp.py
```

2. Claude Desktop用：
```bash
./install_ssh_mcp_claude.py
```

これらのスクリプトは以下を行います：
1. 設定ファイルの場所を検出
2. SSH接続パラメータの入力を求める
3. SSH MCPサーバー設定で設定ファイルを更新

#### 手動インストール

##### Claude Desktop

Claude DesktopでのSSH MCPサーバーの設定方法を示す例の設定ファイルが `claude-desktop-config-example.json` に提供されています。

Claude DesktopにSSH MCPサーバーをインストールするには：

1. Claude Desktop設定ファイルを見つけます：
   - macOSの場合: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
   - Windowsの場合: `%APPDATA%/Claude/claude_desktop_config.json`

2. 設定ファイルの `mcpServers` オブジェクトにSSH MCPサーバー設定を追加します：

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

3. 変更を適用するためにClaude Desktopを再起動します。

注意: プレースホルダーの値を実際のSSH接続詳細に置き換えてください。

## 開発

### ビルドと公開

パッケージを配布用に準備するには：

1. 依存関係を同期してロックファイルを更新：
```bash
uv sync
```

2. パッケージディストリビューションをビルド：
```bash
uv build
```

これにより、`dist/` ディレクトリにソースとホイールのディストリビューションが作成されます。

3. PyPIに公開：
```bash
uv publish
```

注意: 環境変数またはコマンドフラグを介してPyPI認証情報を設定する必要があります：
- トークン: `--token` または `UV_PUBLISH_TOKEN`
- またはユーザー名/パスワード: `--username`/`UV_PUBLISH_USERNAME` と `--password`/`UV_PUBLISH_PASSWORD`

### テスト

SSH MCPサーバーが正しく動作することを確認するためのテストスクリプトが `tests` ディレクトリに提供されています：

```bash
python tests/test_ssh_connect.py
```

このテストスクリプトは、実際にSSHサーバーに接続することなく、SSH MCPサーバーの基本機能をテストするためにunittestとモッキングを使用します。

### デバッグ

MCPサーバーはstdioを介して実行されるため、デバッグが難しい場合があります。最適なデバッグ体験のために、[MCP Inspector](https://github.com/modelcontextprotocol/inspector)の使用を強くお勧めします。

[`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)を介してMCP Inspectorを起動するには、次のコマンドを使用します：

```bash
npx @modelcontextprotocol/inspector uv --directory /path/to/ssh-connect run ssh-connect
```

起動すると、InspectorはブラウザでアクセスできるURLを表示し、デバッグを開始できます。
