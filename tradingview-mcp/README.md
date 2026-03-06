# TradingView MCP Server

A production-ready Model Context Protocol (MCP) server for Large Language Models (LLMs) to natively integrate with TradingView. This server provides AI agents with deep access to Pine Script analysis, backtesting simulation, and market data retrieval.

## Features

- **Standardized MCP Interface**: Exposes a `GET /tools.json` endpoint that configures LLMs natively instantly.
- **Pine Script v5 Engine**: Parses, validates, and extracts parameter logic from user-provided Pine Scripts.
- **Offline Backtesting**: Fully simulates bar-by-bar entry and exit logic, outputting detailed portfolio metrics (Sharpe Ratio, Max Drawdown).
- **10 Core Trading Tools**: Retrieve OHLCV price histories, fetch technical indicators, list active user alerts, and perform parameter grid optimization.

## Installation

1. Ensure you have Python 3.9+ installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

Start the FastAPI ASGI server:
```bash
python server.py
```
The server will boot on `http://0.0.0.0:8000`.

## Connecting MCP Clients
Point your MCP-compatible client (Claude for Desktop, Cursor, etc.) to the tools specification endpoint:
`http://localhost:8000/tools.json`

## API Endpoints Overview
*   `GET /health`: Returns 200 OK and timestamp if the server is alive.
*   `GET /tools.json`: Returns the OpenAPI-compliant schemas for the 10 core trading tools.
*   `POST /call/{tool_name}`: Invokes a specific tool (e.g., `backtest_strategy`, `optimize_parameters`).
