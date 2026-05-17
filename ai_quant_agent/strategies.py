from dataclasses import dataclass


@dataclass(frozen=True)
class Strategy:
    name: str
    symbol: str
    code: str
    rationale: str


def generate_ma_cross_strategy(symbol: str) -> Strategy:
    normalized_symbol = symbol.strip().upper()
    code = """# Double moving average baseline strategy
# Buy when MA10 crosses above MA30; sell when MA10 crosses below MA30.
fast = SMA(close, 10)  # MA10
slow = SMA(close, 30)  # MA30

df["buy"] = CROSSOVER(fast, slow).fillna(False).astype(bool)
df["sell"] = CROSSUNDER(fast, slow).fillna(False).astype(bool)
"""
    return Strategy(
        name="MA10_MA30_CROSS",
        symbol=normalized_symbol,
        code=code,
        rationale=(
            "使用 MA10 与 MA30 的双均线交叉作为 MVP 基准策略，"
            "便于验证 AI 策略生成、回测调用和复盘报告链路。"
        ),
    )
