# AI Quant Agent

AI Quant Agent is a local research prototype that connects two open-source projects:

- [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents): multi-agent market analysis
- [brokermr810/QuantDinger](https://github.com/brokermr810/QuantDinger): strategy development, backtesting, and simulated execution

The goal is to build a bridge between agent-based market reasoning and a quantitative backtesting workflow. TradingAgents is used as the analysis layer, QuantDinger is used as the backtesting and execution research layer, and this repository provides the middle layer that turns analysis output into strategy templates, backtest requests, and review reports.

This project is for research, backtesting, and paper-only experimentation. It is not investment advice and does not connect to real capital accounts.

## What This Repository Does

The current MVP focuses on a complete local workflow that can run without external services:

1. Accept a stock symbol such as `AAPL`.
2. Generate a baseline MA10 / MA30 moving-average crossover strategy.
3. Run a deterministic offline mock backtest.
4. Produce metrics such as total return, max drawdown, win rate, trade count, and stop-loss count.
5. Generate a Chinese Markdown review report.
6. Keep extension points ready for TradingAgents and QuantDinger integration.

The mock backtest is intentionally simple. Its purpose is to make the bridge workflow runnable before connecting external systems.

## Architecture

```text
TradingAgents analysis layer
technical agent / sentiment agent / fundamentals agent / risk agent
        |
        v
AI Quant Agent bridge layer
analysis normalization / strategy template generation / backtest request / report generation
        |
        v
QuantDinger research layer
Python strategy / backtest metrics / simulated execution result
```

## Intended Data Flow

```text
Input symbol
    |
    v
TradingAgents multi-agent analysis
    |
    v
Structured market view
    |
    v
Strategy template selection
    |
    v
QuantDinger backtest request
    |
    v
Backtest metrics
    |
    v
AI-generated review report
```

Example future TradingAgents output:

```json
{
  "symbol": "AAPL",
  "market_view": "bullish",
  "technical_signal": "MA10 above MA30, RSI neutral",
  "risk_level": "medium",
  "suggested_strategy": "trend_following",
  "stop_loss": 0.03,
  "take_profit": 0.06
}
```

The bridge layer can convert that structured output into a QuantDinger-compatible strategy and submit it to the backtest interface.

## Current MVP

The MVP currently includes:

- A baseline MA10 / MA30 crossover strategy generator
- A deterministic mock backtest client
- A placeholder QuantDinger Agent API client
- A Markdown report generator
- Unit tests for the end-to-end MVP flow
- Rendered screenshots for README and sample report previews

## Repository Structure

```text
ai_quant_agent/
  strategies.py      Strategy dataclass and MA crossover strategy generator
  backtests.py       Mock backtest client and QuantDinger client scaffold
  reports.py         Markdown report builder

agents/
  README.md          Planned TradingAgents adapter location

backtests/
  README.md          Planned QuantDinger backtest scripts

strategies/
  README.md          Planned strategy template files

reports/
  AAPL_report.md     Generated sample research report

screenshots/
  readme.png         Rendered README preview
  aapl-report.png    Rendered report preview

scripts/
  render_materials.py  Local renderer for Markdown preview screenshots

tests/
  test_mvp_flow.py   Unit tests for the MVP workflow
```

## Quick Start

```bash
git clone https://github.com/mcchipp/ai-quant-agent.git
cd ai-quant-agent
python3 main.py AAPL
```

The command writes:

```text
reports/AAPL_report.md
```

Run the same workflow with another symbol:

```bash
python3 main.py TSLA
```

## Testing

```bash
python3 -m unittest discover -s tests -v
```

Expected result:

```text
Ran 2 tests ... OK
```

## QuantDinger Integration Plan

The current `MockBacktestClient` validates the bridge flow without external dependencies. The planned QuantDinger mode uses the configuration in `.env.example`:

```text
BACKTEST_MODE=quantdinger
QUANTDINGER_BASE_URL=http://localhost:8888
QUANTDINGER_AGENT_TOKEN=your_agent_token_here
```

Recommended early-stage permissions:

```text
R = read market data
B = backtest / simulation
```

Avoid enabling real trading permissions during MVP research:

```text
T = live trading / real capital
```

## TradingAgents Integration Plan

The planned TradingAgents adapter will normalize multi-agent analysis into a stable bridge format:

```python
{
    "symbol": "AAPL",
    "market_view": "bullish",
    "technical_signal": "MA10 above MA30",
    "risk_level": "medium",
    "suggested_strategy": "trend_following",
    "risk_controls": {
        "stop_loss": 0.03,
        "take_profit": 0.06
    }
}
```

That payload can then be mapped to one of several strategy templates:

- moving-average crossover
- RSI-filtered trend following
- breakout strategy
- pullback strategy
- volatility-filtered strategy

## Roadmap

- Add a TradingAgents adapter that reads structured multi-agent analysis output.
- Add strategy templates beyond MA crossover.
- Add a QuantDinger backtest submission and polling client.
- Store backtest results as JSON artifacts.
- Generate comparative reports across multiple symbols and strategies.
- Keep the project in backtest-only and paper-only mode until the risk model is mature.

## Safety Boundary

This repository is designed for research workflows only:

- No financial advice
- No live trading by default
- No real capital connection
- No guarantee of future performance
- Backtest and mock results are for workflow validation only
