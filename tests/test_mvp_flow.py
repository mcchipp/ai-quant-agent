import unittest

from ai_quant_agent.backtests import MockBacktestClient
from ai_quant_agent.reports import build_review_report
from ai_quant_agent.strategies import generate_ma_cross_strategy


class MvpFlowTest(unittest.TestCase):
    def test_full_mvp_flow_creates_strategy_result_and_report(self):
        strategy = generate_ma_cross_strategy("AAPL")
        result = MockBacktestClient().run("AAPL", strategy)
        report = build_review_report("AAPL", strategy, result)

        self.assertIn("MA10", strategy.code)
        self.assertEqual(result.symbol, "AAPL")
        self.assertGreater(result.total_return_pct, 0)
        self.assertIn("最大回撤", report)
        self.assertIn("AAPL", report)

    def test_mock_backtest_is_deterministic_for_same_symbol(self):
        strategy = generate_ma_cross_strategy("TSLA")
        first = MockBacktestClient().run("TSLA", strategy)
        second = MockBacktestClient().run("TSLA", strategy)

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
