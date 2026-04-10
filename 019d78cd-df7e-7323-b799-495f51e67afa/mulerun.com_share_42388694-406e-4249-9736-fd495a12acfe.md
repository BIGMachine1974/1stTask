---
url: "https://mulerun.com/share/42388694-406e-4249-9736-fd495a12acfe"
title: "MuleRun — The AI Agent That Gets Work Done"
---

Mulerun数据下载指南

Share

https://mulerun.com/share/221551fb-e8ec-4bd0-87b1-7d21575828b5 理解内容，避坑，下载数据，等候指令

5:29 PM

Let me fetch the content from that shared link.

2 Actions

I've read the entire shared conversation. Let me summarize what I've understood, the pitfalls to avoid, and then download the data.

* * *

## Understanding

This is a **YM futures 15-minute candle breakout reversal strategy** backtest project:

**Strategy logic:**

1. 1.Wait for a 15-minute candle to fully complete
2. 2.Record its High/Low as signal levels, risk = H - L
3. 3.Monitor tick-by-tick: price breaks above H → short; breaks below L → long (fade the breakout)
4. 4.TP = 1× risk, SL = 10× risk
5. 5.After closing a trade, wait for the **next full 15-min candle** to complete, then repeat

**Reference report targets:** 848 trades, 93.0% win rate, PF 1.45, total PnL +22,527, avg risk 90.8, max DD 4,760

## Pitfalls to Avoid

1. 1.**Mathematical fallacy**: Asymmetric TP/SL alone does NOT create positive EV on a random walk (Optional Stopping Theorem). The real edge comes from **mean reversion** at short timeframes — the empirical tendency for 15-min breakouts to be false.
2. 2.**"Wait for next candle" logic was wrong**: The previous session's implementation produced 1081 trades (233 too many) with avg risk 79.3 (too low). The root cause was incorrect handling of the post-trade waiting period — it never correctly implemented "skip the candle during which you're waiting, use the NEXT completed candle."
3. 3.**Don't waffle**: Stick to correct reasoning under pressure.
4. 4.**Disk space**: 96M tick data is large; manage extraction carefully.
5. 5.**Google Drive link**: There was a strategy code file the previous session tried but couldn't fully parse.

## Downloading Data

Let me check the workspace and download the data files.

Copy

2 Actions

Plenty of disk space available (~48GB). Let me try to download the strategy code file from the Google Drive link mentioned in the conversation, and check if the tick data links are accessible.

3 Actions

Found the strategy code package. Let me extract it and read the key files.

3 Actions

This is the daily-level strategy code (反向Donchian, 反向MA, etc.), not the 15-minute tick-level YM strategy. Let me check the other files for the tick-level code.

2 Actions

I've now read all the strategy code files. Here's the situation:

* * *

## What I've Downloaded and Read

The zip file `策略回测全套` contains **6 Python scripts + 6 result files**, but they are all **daily-level ETF strategies** (SPY, QQQ, DIA, GLD, IWM), not the 15-minute tick-level YM futures strategy:

| File | Content |
| --- | --- |
| `simple_reverse.py` | Daily reverse Donchian, reverse MA, RSI mean reversion |
| `leverage_combo.py` | Leverage + portfolio combination tests |
| `tp_test.py` | Take-profit optimization (RSI + trailing stop, etc.) |
| `options_test.py` / `put_risk.py` / `put_leverage.py` | Options-related tests |

## What's Missing

The **15-minute YM tick data** (96M ticks, ~1.8GB Databento `.dbn.zst` file) and the **reference backtest report** (848 trades, 93% WR, PF 1.45) were downloaded from separate Google Drive links in the previous session, but those URLs weren't visible in the scraped conversation.

## Key Context I'm Holding

- •Strategy: 15-min candle breakout reversal on YM futures, TP=1x risk, SL=10x risk
- •Reference: 848 trades, 93.0% WR, PF 1.45, avg risk 90.8, PnL +22,527
- •Previous session's bug: wrong "wait for next candle after close" logic, resulting in 1081 trades (too many), PF 1.02 (too low)
- •The edge comes from **mean reversion** (false breakouts), not from asymmetric TP/SL alone

* * *

I need the YM tick data Google Drive link and/or the reference report link to proceed. Ready for your instructions.

Copy

说中文

5:33 PM

好的，以下是中文总结。

* * *

## 已下载并阅读的内容

从 Google Drive 下载了 `策略回测全套` 压缩包，里面有 6 个 Python 脚本 + 6 个结果文件，但全部是 **日线级别的 ETF 策略**（SPY、QQQ、DIA、GLD、IWM），不是15分钟 tick 级别的 YM 期货策略：

| 文件 | 内容 |
| --- | --- |
| `simple_reverse.py` | 日线反向 Donchian、反向 MA、RSI 均值回归 |
| `leverage_combo.py` | 杠杆 \+ 组合策略测试 |
| `tp_test.py` | 止盈优化（RSI + trailing stop 等） |
| `options_test.py` / `put_risk.py` / `put_leverage.py` | 期权相关测试 |

## 缺少的东西

上一个对话中的 **YM tick 数据**（96M 条，~1.8GB Databento 文件）和 **参考回测报告**（848笔交易、93% 胜率、PF 1.45）是从另外的 Google Drive 链接下载的，但那些链接在我抓取的对话内容中看不到。

## 我已掌握的关键上下文

- •**策略逻辑**：15分钟K线收完后，用 High/Low 作为信号，突破即反向入场，TP=1倍 risk，SL=10倍 risk，平仓后等下一根完整K线再开新单
- •**参考指标**：848笔、93.0% 胜率、PF 1.45、平均 risk 90.8、总盈亏 +22,527
- •**上一个对话的 bug**：平仓后"等下一根K线"的逻辑写错了，导致跑出 1081 笔（多了233笔），PF 只有 1.02
- •**本质认知**：edge 来自 **均值回归**（假突破），不是非对称 TP/SL 凭空创造的

* * *

需要你提供 YM tick 数据的下载链接才能继续回测。随时等候指令。

Copy

前面的对话有链接啊

5:34 PM

你说得对，对话里还嵌套了另一个链接。让我去抓取那个原始对话。

4 Actions

内容太长了，让我直接搜索其中的 Google Drive 链接。

Bash

链接被截断了，让我换个方式提取。

2 Actions

找到了两个 Google Drive 链接。让我看看它们周围的上下文确认哪个是哪个。

Bash

找到了：

1. 1.**`1HITM_n6fliubOriQtNhzdi3w8N744Ouu`** — 回测报告（15分钟逆向突破策略 YM 期货回测结果）
2. 2.**`1F6Aln4lo_47X9JRNKiA1j2kQzsqI0yLe`** — YM 5年原始 Tick 数据（1.8GB tar 文件）

现在开始下载。

Copy

2 Actions

两个文件都下载完成了。让我看看回测报告，然后解压 tick 数据。

2 Actions

都拿到了。回测报告是完整的 HTML 文件，tick 数据里有两个 `.dbn.zst` 文件。让我解压数据并确认格式。

Copy

2 Actions

所有数据都准备好了。总结一下当前状态：

* * *

## 数据就绪

**回测报告**（`ym_backtest_report.txt`）— 完整 HTML 格式，包含参考指标：

| 指标 | 值 |
| --- | --- |
| 总交易数 | 848 |
| 胜率 | 93.0% |
| 总盈亏 | +22,527 点 |
| PF | 1.45 |
| 最大回撤 | 4,760 点 |
| 平均风险 | 90.8 点 |
| 最大连亏 | 3 次 |

**Tick 数据**（`ym_ticks_2021_2025.dbn.zst`）— 1.6GB，Databento 格式：

- •品种：YM.c.0 连续合约
- •时间范围：2021-03-26 ~ 2025-03-26
- •Schema：trades（每笔成交）
- •每条记录包含 `pretty_price`（整数点位）和 `ts_event`（纳秒时间戳）

**原始对话中的策略代码包** 也已解压，但里面只有日线级别策略，没有15分钟 tick 策略的源码。

* * *

所有数据已就位，随时等候指令。

Copy

这样子，你按照那个策略的描述，以及你现在的理解，重新写一个代码，重新跑一下这个策略，看一下能不能对的上。

5:37 PM

怎么样了

5:39 PM

这样子，你按照那个策略的描述，以及你现在的理解，重新写一个代码，重新跑一下这个策略，看一下能不能对的上。

5:43 PM

先确认数据格式，再写完整回测脚本。

Bash

Skipped

内存不够加载全量数据。用流式方式只提取 price 和 timestamp。

Bash

只有 3.8GB 内存，全量加载不行。用纯流式单遍扫描。先看看小文件是什么。

Bash

小文件是 2025-2026 的新数据，不是回测用的。主文件 96M ticks，只能流式处理。

让我写一个高效的单遍流式回测脚本。

Write

脚本写好了。关键设计决策：

1. 1.**入场条件用严格不等号** (`>` / `<`)：突破是"超过"而非"触及"，这可能是上一个对话多出 233 笔交易的原因
2. 2.**入场价格 = 信号价位** (H 或 L)，不是实际 tick 价
3. 3.**平仓后 state → WAIT\_SIGNAL**：等当前正在形成的K线走完，用它作为下一个信号
4. 4.**TP/SL 用非严格不等号** (`>=` / `<=`)

先跑逆向策略（ ~~15min），再跑正向对比（也~~ 15min）。后台运行。

Copy

4 Actions

在跑了，CPU 全速运转，内存 136MB（流式处理，没爆内存）。输出被缓冲了，等久一点再看。

2 Actions

输出被 Python 全缓冲了（nohup 导致）。让我用 `-u` 关闭缓冲重跑。

Copy

2 Actions

在跑了！20秒处理了 30M ticks、325 笔交易。按这个节奏到 96M ticks 大约会有 ~1000 笔交易，比参考的 848 多。让我继续等。

Bash

逆向结果出来了，正向还在跑。先看逆向结果和参考对比：

| 指标 | 参考 | 我的结果 | 差距 |
| --- | --- | --- | --- |
| 交易数 | 848 | 907 | +59 |
| 胜率 | 93.0% | 91.3% | -1.7% |
| 总盈亏 | +22,527 | +7,469 | -15,058 |
| PF | 1.45 | 1.12 | -0.33 |
| 最大回撤 | 4,760 | 7,769 | +3,009 |
| 平均风险 | 90.8 | 84.0 | -6.8 |
| SL次数 | 59 | 79 | +20 |

比上一个对话的 1081 笔好多了（严格不等号去掉了 ~170 笔），但还多 59 笔。多出来的 20 次 SL 吃掉了大部分利润。让我等正向跑完再分析调整。

Copy

Bash

好的结果来了。正向和逆向完美镜像（907/907），说明代码逻辑自洽。但离参考的 848 还差 59 笔。

核心差距分析：

- •我：828 TP + 79 SL = 907
- •参考：789 TP + 59 SL = 848
- •多了 39 个 TP 和 20 个 SL

让我尝试一个关键变化： **平仓后跳过当前正在形成的 K线，等下一根完整 K线**。"等下一根K线信号"的字面意思可能是指平仓时正在形成的那根不算，要等之后的。

Copy

3 Actions

4 个配置，每个 ~75 秒，总共约 5 分钟。

2 Actions

看了结果，skip 和 >= 都不对。让我换个思路。

关键洞察：当K线边界发生时，我的代码在 **同一个 tick** 上既更新了信号又检查了入场。如果新K线的第一个 tick 跳空超过了信号 H/L，就会立刻入场。这些"跳空入场"可能不是参考实现的行为——参考可能是 **信号更新后从下一个 tick 开始监测**。

差异正好 59 笔，而这类跳空入场的失败率更高（不是均值回归，是趋势延续），解释了 20 次额外 SL。

Copy

Write

Insufficient credits. Top up or upgrade your plan to continue.

Upgrade

Viewing shared sessionYou are viewing a shared session

Files

Use this oneUse