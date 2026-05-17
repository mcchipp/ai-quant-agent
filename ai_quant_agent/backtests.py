from dataclasses import dataclass
from hashlib import sha256
from typing import Any, Dict, Optional

from .strategies import Strategy


@dataclass(frozen=True)
class BacktestResult:
    symbol: str
    strategy_name: str
    total_return_pct: float
    max_drawdown_pct: float
    win_rate_pct: float
    trade_count: int
    stop_loss_count: int
    source: str


class MockBacktestClient:
    """Deterministic offline client for screenshots and token application proof."""

    def run(self, symbol: str, strategy: Strategy) -> BacktestResult:
        normalized_symbol = symbol.strip().upper()
        digest = sha256(f"{normalized_symbol}:{strategy.name}".encode("utf-8")).digest()

        total_return_pct = round(6.0 + digest[0] / 255 * 18.0, 2)
        max_drawdown_pct = round(4.0 + digest[1] / 255 * 10.0, 2)
        win_rate_pct = round(42.0 + digest[2] / 255 * 22.0, 2)
        trade_count = 12 + digest[3] % 30
        stop_loss_count = 1 + digest[4] % 6

        return BacktestResult(
            symbol=normalized_symbol,
            strategy_name=strategy.name,
            total_return_pct=total_return_pct,
            max_drawdown_pct=max_drawdown_pct,
            win_rate_pct=win_rate_pct,
            trade_count=trade_count,
            stop_loss_count=stop_loss_count,
            source="mock",
        )


class QuantDingerClient:
    def __init__(self, base_url: str, agent_token: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.agent_token = agent_token
        self.timeout = timeout

    def submit_backtest(self, symbol: str, strategy: Strategy) -> Dict[str, Any]:
        try:
            import requests
        except ImportError as exc:
            raise RuntimeError("QuantDinger API mode requires `pip install requests`.") from exc

        url = f"{self.base_url}/api/agent/v1/backtests"
        payload = {
            "code": strategy.code,
            "market": "USStock",
            "symbol": symbol.strip().upper(),
            "timeframe": "1D",
            "initial_capital": 10000,
        }
        headers = {
            "Authorization": f"Bearer {self.agent_token}",
            "Content-Type": "application/json",
            "Idempotency-Key": f"backtest-{symbol.strip().upper()}-{strategy.name}",
        }
        response = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()


def client_from_env(env: Optional[Dict[str, str]] = None):
    import os

    values = env if env is not None else os.environ
    mode = values.get("BACKTEST_MODE", "mock").strip().lower()
    if mode == "quantdinger":
        base_url = values.get("QUANTDINGER_BASE_URL", "http://localhost:8888")
        token = values.get("QUANTDINGER_AGENT_TOKEN", "")
        if not token:
            raise RuntimeError("QUANTDINGER_AGENT_TOKEN is required when BACKTEST_MODE=quantdinger.")
        return QuantDingerClient(base_url=base_url, agent_token=token)
    return MockBacktestClient()
