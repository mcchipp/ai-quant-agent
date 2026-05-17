import argparse
from pathlib import Path

from ai_quant_agent.backtests import MockBacktestClient
from ai_quant_agent.reports import build_review_report
from ai_quant_agent.strategies import generate_ma_cross_strategy


def run(symbol: str, output_dir: Path) -> Path:
    normalized_symbol = symbol.strip().upper()
    strategy = generate_ma_cross_strategy(normalized_symbol)
    result = MockBacktestClient().run(normalized_symbol, strategy)
    report = build_review_report(normalized_symbol, strategy, result)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{normalized_symbol}_report.md"
    output_path.write_text(report, encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run AI Quant Agent MVP flow.")
    parser.add_argument("symbol", nargs="?", default="AAPL", help="Stock symbol, e.g. AAPL or TSLA.")
    parser.add_argument("--output-dir", default="reports", help="Directory for generated Markdown reports.")
    args = parser.parse_args()

    output_path = run(args.symbol, Path(args.output_dir))
    print(f"Report written to {output_path}")


if __name__ == "__main__":
    main()
