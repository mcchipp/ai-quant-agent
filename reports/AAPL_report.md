# AAPL AI 量化研究复盘报告

## 项目说明

本报告由 AI Quant Agent MVP 自动生成，用于验证“TradingAgents 多智能体分析 -> 策略生成 -> QuantDinger 回测 -> AI 复盘”的本地工作流。项目仅用于回测和模拟研究，不构成投资建议，也不连接真实资金账户。

## 策略假设

- 策略名称：MA10_MA30_CROSS
- 股票代码：AAPL
- 策略逻辑：MA10 上穿 MA30 买入，MA10 下穿 MA30 卖出。
- 生成原因：使用 MA10 与 MA30 的双均线交叉作为 MVP 基准策略，便于验证 AI 策略生成、回测调用和复盘报告链路。

## 回测结果

- 数据来源：mock
- 总收益率：22.52%
- 最大回撤：5.61%
- 胜率：56.84%
- 交易次数：35
- 止损次数：3

## AI 复盘结论

本次 AAPL 双均线策略回测显示，该策略适合用于验证 TradingAgents 分析结果到 QuantDinger 回测任务的转换流程。收益率、最大回撤、胜率和交易次数已经形成可解释指标，能够作为后续 MiMo API 生成策略解释、参数优化建议和多轮实验对比的输入。

当前回撤处于 MVP 可接受范围，下一轮可比较 RSI 过滤后的表现。

## 下一步计划

1. 接入 TauricResearch/TradingAgents 输出技术面、情绪面、基本面和风控分析。
2. 将 TradingAgents 分析结果转换为 QuantDinger 可执行策略。
3. 接入 MiMo API 自动生成多策略比较报告。
4. 保持 backtest-only / paper-only 模式，不启用真实资金交易。
