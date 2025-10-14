# GitHub MCP Server

A Model Context Protocol (MCP) server for interacting with GitHub repositories through the GitHub REST API.

## Features

- **get_file_contents**: Get the contents of files or directories in GitHub repositories
- Support for specific branches, tags, or commits
- Clean, minimal implementation following MCP standards

## Setup

### Environment Variables

- `GITHUB_TOKEN`: GitHub personal access token (optional, but recommended for higher rate limits)
- `MCP_TRANSPORT`: Transport method (default: "sse")
- `MCP_HOST`: Host to bind to (default: "0.0.0.0")
- `MCP_PORT`: Port to bind to (default: 3001)
- `LOG_LEVEL`: Log level (default: "info")

### Running with Docker

```bash
# Build and run with docker-compose
docker-compose up --build

# Or run directly
docker build -t github-mcp .
docker run -p 3001:3001 -e GITHUB_TOKEN=your_token_here github-mcp
```

### Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GITHUB_TOKEN=your_token_here

# Run the server
python server.py
```

## API Reference

### get_file_contents

Get the contents of a file or directory in a GitHub repository.

**Parameters:**
- `owner` (string, required): The account owner of the repository
- `repo` (string, required): The name of the repository without the .git extension
- `path` (string, optional): The path to the file or directory (defaults to repository root)
- `ref` (string, optional): The name of the commit/branch/tag (defaults to repository's default branch)

**Returns:**
- Content tree object with file/directory information including:
  - `type`: "file" or "dir"
  - `name`: File/directory name
  - `path`: Full path
  - `sha`: Git SHA
  - `content`: Base64 encoded content (for files)
  - `download_url`: Direct download URL
  - `html_url`: GitHub web URL
  - And more...

## Example Usage

```python
# Get repository root contents
await get_file_contents_tool(owner="octocat", repo="Hello-World")

# Get specific file
await get_file_contents_tool(owner="octocat", repo="Hello-World", path="README.md")

# Get file from specific branch
await get_file_contents_tool(owner="octocat", repo="Hello-World", path="README.md", ref="develop")
```

## Architecture

The server follows the same patterns as the airflow-mcp server:

- `server.py`: Main server entry point
- `tools/`: Tool implementations
- `schema/`: JSON schemas for API responses
- `http_utils.py`: HTTP client utilities
- `requirements.txt`: Python dependencies
- `Dockerfile`: Container configuration
- `docker-compose.yaml`: Multi-container setup

## GitHub API Reference

This server uses the GitHub REST API v3. For more information, see:
https://docs.github.com/en/rest/repos/contents
