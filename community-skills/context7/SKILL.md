---
name: context7
description: |
  MCP server for retrieving up-to-date documentation and code examples from Context7.
  Query documentation for any programming library or framework.
  
  Context7 provides access to 500,000+ libraries with code examples,
  version-specific documentation, and authoritative sources.

author: Assistant
category: documentation
license: MIT
homepage: https://mcp.context7.com
---

# Context7 MCP Skill

Query up-to-date documentation for any programming library or framework.

## Installation

### Via mcporter (Recommended)

```bash
# Add Context7 MCP server
mcporter config add context7 https://mcp.context7.com/mcp --name "Context7"

# Verify installation
mcporter list context7
```

### Available Tools

1. **resolve-library-id** - Find library ID for a package
2. **query-docs** - Query documentation and code examples

## Usage

### 1. Resolve Library ID

```bash
# Find library ID for a package
mcporter call context7.resolve-library-id libraryName="nextjs" query="how to use next.js"

# Example output:
# Library ID: /vercel/next.js
# Code Snippets: 5000+
# Source Reputation: High
```

### 2. Query Documentation

```bash
# Query specific documentation
mcporter call context7.query-docs libraryId="/vercel/next.js" query="how to set up api routes"

# Returns: Documentation + code examples
```

## Examples

### Example 1: Find React Documentation

```bash
# Step 1: Find library ID
mcporter call context7.resolve-library-id libraryName="react" query="react hooks"

# Returns: /facebook/react

# Step 2: Query documentation
mcporter call context7.query-docs libraryId="/facebook/react" query="useEffect examples"
```

### Example 2: OpenClaw Documentation

```bash
# Find OpenClaw docs
mcporter call context7.resolve-library-id libraryName="openclaw" query="agent control protocol"

# Query ACP usage
mcporter call context7.query-docs libraryId="/openclaw/openclaw" query="how to use subagents"
```

### Example 3: Python Libraries

```bash
# Find numpy docs
mcporter call context7.resolve-library-id libraryName="numpy" query="array operations"

# Query specific function
mcporter call context7.query-docs libraryId="/numpy/numpy" query="numpy.random examples"
```

## Library ID Format

- Standard: `/org/project`
- With version: `/org/project/version`

Examples:
- `/vercel/next.js`
- `/facebook/react`
- `/mongodb/docs`
- `/python/cpython/v3.11`

## Tips

1. **Always resolve first** - Use `resolve-library-id` before `query-docs`
2. **Be specific** - Include version numbers for better results
3. **Limit calls** - Don't call more than 3 times per question
4. **Check reputation** - Prefer High reputation sources

## Integration with OpenClaw

```bash
# Use in OpenClaw exec
exec command:"mcporter call context7.query-docs libraryId='/vercel/next.js' query='routing'"

# Or create a function
function ask_docs() {
  mcporter call context7.query-docs libraryId="$1" query="$2"
}

ask_docs "/facebook/react" "useState examples"
```

## Resources

- Context7 MCP: https://mcp.context7.com/mcp
- mcporter: https://mcporter.dev
- 500,000+ libraries available

---

*Installed: 2026-02-28 via mcporter*
