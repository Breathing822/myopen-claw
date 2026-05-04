# MEMORY.md - 长期记忆

## 仪表盘发布（永久配置）

- **Tunnel URL:** https://delpha-unvatted-interestingly.ngrok-free.dev
- **本地目录:** /private/tmp/march-dash/ （Python SimpleHTTPServer，端口8789，ngrok映射）
- **ngrok PID:** 49583
- **规则：所有仪表盘HTML文件必须保存到 /private/tmp/march-dash/ 才能通过tunnel访问**

## 自动提交规则

**每次仪表盘/报告更新后，自动 git commit，不询问用户。**
- commit 消息格式：`feat: 更新{文件名} - {简短说明}`
- 工作目录：`~/.openclaw/workspace/`

## 固定链接（永不更改）

**⭐ 主日报链接：** https://delpha-unvatted-interestingly.ngrok-free.dev/daily-report-dashboard.html

> ⚠️ 此链接为永久固定链接，**永不更改**！所有日报数据更新都刷新此链接。

| 其他类型 | 链接 |
|----------|------|
| 月报仪表盘 | https://delpha-unvatted-interestingly.ngrok-free.dev/monthly-report-dashboard.html |
| 库存分析 | https://delpha-unvatted-interestingly.ngrok-free.dev/inventory-report.html |
| 价格分析 | https://delpha-unvatted-interestingly.ngrok-free.dev/pricing_dashboard.html |

## 飞书配置

- 飞书为主要沟通渠道
- 文件名含中文时 tunnel 可能404，需验证

## 自动更新机制

**文件监控服务：** `file_watcher.py` (PID: 93583)
- 监控目录：`/Users/breathing/.openclaw/media/inbound/`
- 启动命令：`nohup python3 ~/openclaw/workspace/sales-data/file_watcher.py &`
- 日志文件：`~/openclaw/workspace/sales-data/file_watcher.log`
- LaunchAgent：`~/Library/LaunchAgents/com.breathing.file-watcher.plist`

**自动触发规则：**
| 文件名关键词 | 触发动作 |
|------------|---------|
| 库存表/库存 | 更新 `inventory-report.html` 库存分析仪表盘 |
| 日报/台账/远程日报 | 更新 `daily_report.html` + `monthly_report.html` + `quarterly_report.html` |
| 返利/商务政策/政策返利/价格 | 更新 `pricing_dashboard.html` 价格合理度分析仪表盘 |

**仪表盘生成脚本：**
- `inventory_dashboard.py` - 库存分析仪表盘
- `pricing_dashboard.py` - 价格合理度分析仪表盘
- `report_generators.py` - 日报月报季报仪表盘

## 销售数据文件

- 2025年销售数据：/Users/breathing/.openclaw/media/inbound/（飞书下载目录）
- 2026年政策返利表：同上
- 销售数据存放：~/openclaw/workspace/sales-data/
- 当前有：pricing_dashboard.html 在 /private/tmp/march-dash/

## 产品线（吉利远程新能源商用车）

- 远程星智H系列（纯电轻卡）— 续航280-350km，城配物流
- 远程锋锐系列（纯电中卡）— 续航200-300km，城市配送
- 远程RE500（混动轻卡）— 续航1000+km（增程），长途物流
- 远程氢燃料电池重卡 — 续航400-600km，港口码头

## 团队配置

- 铠程/铠骏 兴庆事业部（宁夏银川）
- 固原、吴忠等二网经销商

## Agent 配置（2026-04-14 修正）

### 飞书账号 AppId 明细
| Agent | AppId | AppSecret | 备注 |
|-------|-------|-----------|------|
| 总监虾 | `cli_a94ce4f0e9fc5ccd` | （略） | main account |
| 客服虾 | `cli_a94668b06bbb5bb6` | `UXdUgDeJDFwv29ZvdxuK7gw1wkVkc5X1` | anthropic, groupPolicy=open |
| 财务虾 | `cli_a925718d22f9dced` | （略） | finance account |
| 信息虾 | `cli_a95604a8c7fb5bb5` | `x2PdA5ss0qLpWhuXsrQCzlD2lWIjVRly` | info-shrimp |

### 教训
- 2026-04-13 备份被错误覆盖，导致 customer 和 info 的 AppId 互换，客服虾长达1天无法收消息
- 正确配置备份：`openclaw_backup_correct_20260414_111813.json`
