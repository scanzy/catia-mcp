# CATIA 3D MCP Server

This project aims to let AI control CATIA 3D software through MCP (Model Context Protocol).

Available tools:
- `search`: searches for a part/product by name
- `info`: gets info about a part/product by name
- `show`: shows or hides a part/product by name


## Installation

Add the following to your MCP configuration file:

```json
{
  "mcpServers": {
    "catia-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--with", "fastmcp",
        "--with", "pycatia",
        "/path/to/server.py"
      ]
    },
    // other servers
  }
}
```
