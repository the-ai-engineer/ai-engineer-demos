# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI Engineer Demos repository containing Python code examples for working with AI APIs. 

## Environment Setup

- **Python Version**: Requires Python >=3.13
- **Package Manager**: Uses `uv` (uv.lock present)
- **Required Environment**: Set `OPENAI_API_KEY` environment variable

## Key Dependencies

- `aiohttp` - Async HTTP client for API calls
- `aiofiles` - Async file I/O operations  
- `ipykernel` - Jupyter notebook support

## Common Commands

```bash
# Install dependencies
uv sync

# Run the image generation example
cd src/parallel-images && python example.py

# Run with custom API key
OPENAI_API_KEY=your_key python src/parallel-images/example.py
```