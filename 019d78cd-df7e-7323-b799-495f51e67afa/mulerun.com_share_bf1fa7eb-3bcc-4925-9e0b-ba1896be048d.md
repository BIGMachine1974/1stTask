---
url: "https://mulerun.com/share/bf1fa7eb-3bcc-4925-9e0b-ba1896be048d"
title: "MuleRun — The AI Agent That Gets Work Done"
---

舆情项目管理文档与进度计划

Share

帮我写一个项目管理的文档，解决以下背景的问题：
背景：foxdata签约了一个舆情的项目，但是进展有点慢，且卡住了，客户有流失风险。目前核心问题，定义为 1. 爬取哪些平台，舆情的规模比较大（youtube、X、facebook、raddit、tiktok） 2. 如何有效的爬取，现在品牌词、关键词、排除词如何设置规则可以更有效的爬取到需要的负面舆情的内容 3. 视频内容爬取后的解析问题。我需要在下周1-3确认掉这些事宜，并做多次验证，请帮我排一个项目表

1:24 AM

5 Actions

Now let me create the document. I'll write it in parts to avoid size limits.

7 Actions

舆情项目攻坚计划.docx

Document

文档已生成，包含以下完整内容：

**一、项目背景与现状** — 签约背景、三大卡点说明、客户流失风险分析

**二、核心问题拆解**

- •平台选择与覆盖策略：5大平台（X/YouTube/Reddit/Facebook/TikTok）的优先级、数据量级、爬取难度对比表
- •关键词规则优化：品牌词 \+ 负面词 \+ 排除词三层体系，含布尔组合搜索策略
- •视频内容解析方案：ASR语音转文字、CC字幕提取、OCR、LLM摘要生成、多语言支持

**三、攻坚排期表（4/13-4/15）** — 三天共9个时段的详细任务分配，每项标注负责角色、产出物和验证标准

**四、验证计划** — 三大问题的验证方法、验收标准、通过条件

**五、风险与应对** — 5项风险点及对应措施

**六、下一步行动** — 周四客户汇报 → 方案微调 → 正式开发 → UAT验收的后续路线图

Copy

交易所名字：
负面关键词：
帮我做一个爬取X、youtube的搜索策略，可以出三种爬取策略供我选择。这个是供应商给的交易所名字和关键词，如何可以高效的组合，降低脏数据比例，实现精准爬取当周的数据。

1:40 AM

2 Actions

我已看到供应商提供的数据。让我整理一下，然后输出三种爬取策略方案。

**交易所清单（9家）：** XM、Exness、AVATRADE（爱华）、EC markets、IC Markets Global、FXCM（福汇）、TMGM、FXTM（富拓）、FOREX.com（嘉盛集团）

**负面关键词（资金封锁与跑路征兆类）：** 限制提现、暂停提币、提币手续费暴涨、提币审核、人工审核、挤兑风险、挤兑潮、热钱包归零、老板失联、团队解散

Copy

Skill

I'll create the crawling strategy document now. Due to the document's complexity, I'll build it in a structured JavaScript file.

2 Actions

舆情爬取策略方案.docx

Document

文档已生成，核心内容如下：

### 三种策略概览

| 策略 | 召回率 | 精准率 | 脏数据 | 适用场景 |
| --- | --- | --- | --- | --- |
| **策略一：宽口径** | 90%+ | ~60% | 30-40% | 初期摸底，了解舆情全貌 |
| **策略二：精准匹配** | ~50% | 90%+ | <10% | 快速出结果，给客户演示 |
| **策略三：分层漏斗** (推荐) | ~85% | 85%+ | 10-15% | 长期生产方案，持续迭代 |

### 文档包含

1. 1.**数据源概览** \-\- X 和 YouTube 的 API 能力、搜索语法对比
2. 2.**关键词工程** \-\- 9家交易所品牌词变体矩阵、10个负面词中英双语对照、排除词库
3. 3.**三种策略详细方案** \-\- 每种都给出了 X 和 YouTube 的实际搜索语句示例（可直接复制使用）
4. 4.**策略对比表** \-\- 7个维度横向对比
5. 5.**实施建议** \-\- 推荐执行路径：周一用策略一摸底 → 周二用策略二快速出Demo → 周三部署策略三

Copy

Viewing shared sessionYou are viewing a shared session

Files

Use this oneUse

舆情爬取策略方案.docx

Loading document...