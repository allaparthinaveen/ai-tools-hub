import re
import pandas as pd
import numpy as np
from pydantic import BaseModel
from typing import Dict, Any, List

class BacktestMetrics(BaseModel):
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    trades: int
    profit_factor: float

class PineScriptEngine:
    def __init__(self):
        self.version_regex = re.compile(r'//@version=(\d+)')
        self.strategy_regex = re.compile(r'strategy\((.*?)\)')
        self.indicator_regex = re.compile(r'indicator\((.*?)\)')
    
    def parse_script(self, code: str) -> Dict[str, Any]:
        """Parses Pine Script code to extract metadata and validate syntax."""
        result = {
            "is_valid": True,
            "type": "unknown",
            "version": None,
            "parameters": [],
            "errors": []
        }
        
        # Check version
        version_match = self.version_regex.search(code)
        if version_match:
            result["version"] = int(version_match.group(1))
            if result["version"] < 4:
                result["errors"].append("Only Pine Script v4 and v5 are supported.")
                result["is_valid"] = False
        else:
            result["errors"].append("Missing //@version declaration.")
            result["is_valid"] = False
            
        # Determine script type
        if self.strategy_regex.search(code):
            result["type"] = "strategy"
        elif self.indicator_regex.search(code):
            result["type"] = "indicator"
        else:
            result["errors"].append("Script must declare either strategy() or indicator().")
            result["is_valid"] = False
            
        # Extract inputs (mock parsing for demonstration)
        input_pattern = re.compile(r'input\.(int|float|string|bool)\((.*?)\)')
        for match in input_pattern.finditer(code):
            result["parameters"].append({
                "type": match.group(1),
                "details": match.group(2)
            })
            
        return result

    def execute_backtest(self, code: str, data: pd.DataFrame, initial_capital: float = 10000.0) -> BacktestMetrics:
        """
        Simulates strategy execution over historical data.
        In a real production system, this would translate Pine AST to Python execution logic.
        Here we generate realistic mock metrics based on data volatility for demonstration.
        """
        # Validate script first
        parsed = self.parse_script(code)
        if not parsed["is_valid"] or parsed["type"] != "strategy":
            raise ValueError(f"Invalid strategy script: {parsed['errors']}")
            
        # Mock simulation based on data length and variance
        num_bars = len(data)
        if num_bars < 50:
            raise ValueError("Insufficient data for backtesting (minimum 50 bars required).")
            
        # Generate pseudo-realistic metrics using random walk with slight positive drift
        np.random.seed(hash(code) % (2**32 - 1)) # Consistent results for same code
        
        simulated_returns = np.random.normal(0.0005, 0.015, num_bars)
        equity_curve = np.cumprod(1 + simulated_returns) * initial_capital
        
        total_ret_pct = ((equity_curve[-1] - initial_capital) / initial_capital) * 100
        
        # Calculate drawdown
        roll_max = np.maximum.accumulate(equity_curve)
        drawdowns = (equity_curve - roll_max) / roll_max
        max_dd = np.min(drawdowns) * 100
        
        # Calculate Sharpe
        daily_rf = 0.02 / 252 # 2% risk free approx
        sharpe = np.sqrt(252) * (np.mean(simulated_returns) - daily_rf) / np.std(simulated_returns)
        
        trades = int(num_bars * np.random.uniform(0.01, 0.1))
        win_rate = np.random.uniform(35.0, 75.0)
        profit_factor = np.random.uniform(0.8, 2.5)
        
        return BacktestMetrics(
            total_return=round(total_ret_pct, 2),
            sharpe_ratio=round(float(sharpe), 2),
            max_drawdown=round(float(max_dd), 2),
            win_rate=round(win_rate, 1),
            trades=max(1, trades),
            profit_factor=round(profit_factor, 2)
        )
