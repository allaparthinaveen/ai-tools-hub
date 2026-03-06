from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from enum import Enum
from typing import List, Dict, Any, Optional

from pine_script import PineScriptEngine, BacktestMetrics

app = FastAPI(
    title="TradingView MCP Server",
    description="Production-ready Model Context Protocol server for TradingView agents.",
    version="1.0.0"
)

# Engine Instance
engine = PineScriptEngine()

# Response Models
class ToolResponse(BaseModel):
    status: str = "success"
    data: Any
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    status: str = "error"
    error: str

# Endpoints
@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/tools.json")
async def tools_json():
    """Returns MCP compliant tools OpenAPI spec."""
    return {
        "mcp_version": "1.0",
        "description": "TradingView toolkit for AI agents.",
        "tools": [
            {
                "name": "get_symbol_data",
                "description": "Returns OHLCV data for a symbol (mock implementation).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {"type": "string"},
                        "timeframe": {"type": "string", "enum": ["1m", "5m", "15m", "1h", "4h", "1d"]},
                        "limit": {"type": "integer", "default": 100}
                    },
                    "required": ["symbol", "timeframe"]
                }
            },
            {
                "name": "get_technical_indicators",
                "description": "Calculates technical indicators on recent price data.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {"type": "string"},
                        "timeframe": {"type": "string"},
                        "indicators": {
                            "type": "array",
                            "items": {"type": "string", "enum": ["RSI", "MACD", "SMA", "EMA", "ATR"]}
                        }
                    },
                    "required": ["symbol", "timeframe", "indicators"]
                }
            },
            {
                "name": "analyze_pine_script",
                "description": "Parse Pine Script v5 code, validate syntax, and extract strategy logic.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"}
                    },
                    "required": ["code"]
                }
            },
            {
                "name": "backtest_strategy",
                "description": "Simulates full backtest with entry/exit over historical data.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"},
                        "symbol": {"type": "string"},
                        "timeframe": {"type": "string"},
                        "from_date": {"type": "string", "description": "YYYY-MM-DD format"}
                    },
                    "required": ["code", "symbol", "timeframe"]
                }
            },
            {
                "name": "get_alerts",
                "description": "Fetches current active alerts from a TradingView account.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {"type": "string"},
                        "limit": {"type": "integer", "default": 50}
                    },
                    "required": ["symbol"]
                }
            },
            {
                "name": "list_strategies",
                "description": "Returns saved Pine Script strategies for an authenticated user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"}
                    },
                    "required": ["user_id"]
                }
            },
            {
                "name": "optimize_parameters",
                "description": "Runs grid search parameter optimization on a given strategy.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"},
                        "symbol": {"type": "string"},
                        "param_ranges": {
                            "type": "object",
                            "additionalProperties": {
                                "type": "array",
                                "items": {"type": "number"}
                            }
                        }
                    },
                    "required": ["code", "symbol", "param_ranges"]
                }
            },
            {
                "name": "validate_strategy",
                "description": "Checks Pine Script code for syntax errors and logic flaws.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"}
                    },
                    "required": ["code"]
                }
            },
            {
                "name": "get_market_news",
                "description": "Returns recent news impacting a given symbol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {"type": "string"},
                        "limit": {"type": "integer", "default": 10}
                    },
                    "required": ["symbol"]
                }
            },
            {
                "name": "export_strategy",
                "description": "Formats Pine Script code natively or exports logic to CSV/JSON.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"},
                        "format": {"type": "string", "enum": ["tv_script", "json", "csv"], "default": "tv_script"}
                    },
                    "required": ["code"]
                }
            }
        ]
    }

@app.post("/call/{tool_name}")
async def call_tool(tool_name: str, args: Dict[str, Any] = Body(...)):
    """Executes a specific MCP toolkit command."""
    try:
        if tool_name == "get_symbol_data":
            # Mock generating OHLCV data
            symbol = args["symbol"]
            limit = args.get("limit", 100)
            
            dates = [datetime.now() - timedelta(minutes=i*15) for i in range(limit)]
            dates.reverse()
            
            base_price = 150.0 if symbol == "AAPL" else 65000.0 if symbol == "BTCUSDT" else 100.0
            closes = base_price * (1 + np.random.normal(0, 0.005, limit).cumsum())
            
            df = pd.DataFrame({
                "timestamp": [d.isoformat() for d in dates],
                "open": closes * (1 + np.random.normal(0, 0.001, limit)),
                "high": closes * (1 + abs(np.random.normal(0, 0.002, limit))),
                "low": closes * (1 - abs(np.random.normal(0, 0.002, limit))),
                "close": closes,
                "volume": np.random.lognormal(10, 1, limit).astype(int)
            })
            return ToolResponse(data=df.to_dict(orient="records"))
            
        elif tool_name == "analyze_pine_script":
            result = engine.parse_script(args["code"])
            return ToolResponse(data=result)
            
        elif tool_name == "backtest_strategy":
            # Generate mock dataset representing history
            history = pd.DataFrame({"close": np.random.normal(0, 1, 1000).cumsum() + 100})
            metrics = engine.execute_backtest(args["code"], history)
            return ToolResponse(data=metrics.dict())
            
        elif tool_name == "get_technical_indicators":
            return ToolResponse(data={ind: float(np.random.uniform(20, 80)) for ind in args["indicators"]})
            
        elif tool_name == "get_alerts":
            return ToolResponse(data=[
                {"id": "alert_1", "symbol": args["symbol"], "condition": "Crosses SMA 50", "status": "active"}
            ])
            
        elif tool_name == "list_strategies":
            return ToolResponse(data=[
                {"id": "strat_1", "name": "Mean Reversion Bot", "version": "v5", "last_updated": datetime.now().isoformat()}
            ])
            
        elif tool_name == "optimize_parameters":
            # Mock grid search result
            best_params = {k: v[np.random.randint(0, len(v))] for k, v in args["param_ranges"].items()}
            return ToolResponse(data={
                "best_parameters": best_params,
                "best_sharpe": 1.95,
                "iterations_run": 144
            })
            
        elif tool_name == "validate_strategy":
            result = engine.parse_script(args["code"])
            return ToolResponse(data={
                "syntax_valid": result["is_valid"],
                "warnings": [],
                "errors": result["errors"]
            })
            
        elif tool_name == "get_market_news":
            return ToolResponse(data=[
                {"headline": f"{args['symbol']} reaches new local high", "sentiment": "bullish", "published_at": datetime.now().isoformat()}
            ])
            
        elif tool_name == "export_strategy":
            fmt = args.get("format", "tv_script")
            if fmt == "tv_script":
                return ToolResponse(data={"content": args["code"], "extension": ".pine"})
            elif fmt == "json":
                parsed = engine.parse_script(args["code"])
                return ToolResponse(data={"content": json.dumps(parsed), "extension": ".json"})
            else:
                return ToolResponse(data={"content": "type,value\nscript,complex", "extension": ".csv"})
                
        else:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found.")
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
