from .backtests import BacktestResult
from .strategies import Strategy


def build_review_report(symbol: str, strategy: Strategy, result: BacktestResult) -> str:
    normalized_symbol = symbol.strip().upper()
    risk_note = (
        "当前最大回撤偏高，下一轮建议加入 ATR 波动率过滤和固定止损。"
        if result.max_drawdown_pct >= 10
        else "当前回撤处于 MVP 可接受范围，下一轮可比较 RSI 过滤后的表现。"
    )

    return f"""# {normalized_symbol} AI 量化研究复盘报告

## 项目说明

本报告由 AI Quant Agent MVP 自动生成，用于验证“AI 分析 -> 策略生成 -> 回测 -> 复盘”的本地工作流。项目仅用于回测和模拟研究，不构成投资建议，也不连接真实资金账户。

## 策略假设

- 策略名称：{strategy.name}
- 股票代码：{normalized_symbol}
- 策略逻辑：MA10 上穿 MA30 买入，MA10 下穿 MA30 卖出。
- 生成原因：{strategy.rationale}

## 回测结果

- 数据来源：{result.source}
- 总收益率：{result.total_return_pct}%
- 最大回撤：{result.max_drawdown_pct}%
- 胜率：{result.win_rate_pct}%
- 交易次数：{result.trade_count}
- 止损次数：{result.stop_loss_count}

## AI 复盘结论

本次 {normalized_symbol} 双均线策略回测显示，该策略适合用于验证趋势跟随类 Agent 工作流。收益率、最大回撤、胜率和交易次数已经形成可解释指标，能够作为后续 MiMo API 生成策略解释、参数优化建议和多轮实验对比的输入。

{risk_note}

## 下一步计划

1. 接入 TradingAgents 输出技术面、情绪面、基本面和风控分析。
2. 将 Agent 分析结果转换为 QuantDinger 可执行策略。
3. 接入 MiMo API 自动生成多策略比较报告。
4. 保持 backtest-only / paper-only 模式，不启用真实资金交易。
"""
