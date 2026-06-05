# 78D13 联队成员管理工具

简体中文说明。该仓库包含用于维护、导入、导出和备份成员信息的脚本，数据存储为 SQLite，日志写入 `Member/data/run.log`。

## 目录结构（简要）

- Member/
  - data/                # 数据文件（MemberList.db、run.log 等）
  - scripts/             # 可执行脚本
    - init.py            # 初始化数据库与配置
    - info_enter.py      # 插入新成员
    - info_lookup.py     # 查询成员
    - info_modify.py     # 更新成员
    - xlsx2db.py         # 从 xlsx 批量导入（逐行查->新增->修改）
    - db2xlsx.py         # 导出 sqlite 表到 xlsx（备份）
    - dbformat2xlsx.py   # 生成 Excel 表头模板
    - requirements.txt   # 依赖
  - show_C.md
  - config.json

其他文档：Promotion/、RegimentStandards/ 等为说明文档。

## 环境依赖

- Python 3.8+
- 推荐创建虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt  # 如果需要
```

（本仓库使用的依赖主要是 `openpyxl`，如无 requirements.txt，请 `pip install openpyxl`。）

## 初始化

1. 在 `Member/scripts` 目录下运行初始化（会在 `Member/data/` 生成数据库和 `run.log`）：

```powershell
python Member/scripts/init.py
```

2. 该脚本会在 `Member/scripts/config.json` 中写入 `datapath` 和 `logpath`，后续脚本会优先读取该配置。

## 脚本说明与示例

- `Member/scripts/init.py`
  - 用途：创建 `members` 表并初始化触发器、默认 `Member/data/MemberList.db`。
  - 示例：`python Member/scripts/init.py --data-dir Member/data`

- `Member/scripts/info_enter.py`
  - 用途：插入单条成员记录（`gaijin_id`, `name`）。
  - 退出码：0 成功，1 失败（便于批量脚本判断）。
  - 示例：`python Member/scripts/info_enter.py 12345 游戏名`

- `Member/scripts/info_lookup.py`
  - 用途：按 `--gaijin` 或 `--name` 查询成员，未找到时会输出 `未找到记录` 并以非零退出码退出（便于批量判断）。
  - 示例：`python Member/scripts/info_lookup.py --gaijin 12345`

- `Member/scripts/info_modify.py`
  - 用途：按 `gaijin_id` 修改字段（`--name`, `--state`, `--time`, `--landforce`, `--airforce`, `--navy`）。
  - 退出码：成功返回 0，错误返回非零。
  - 示例：`python Member/scripts/info_modify.py 12345 --state F --time 2026-06-01`

- `Member/scripts/xlsx2db.py`
  - 用途：批量读取 Excel（默认 `Member/MemberList.db 输入模板.xlsx`），逐行处理：查询→若未找到则新增→对有值的列执行修改。
  - 日志：每行只输出一条结构化中文日志（示例：`行=2 id=123 操作=已创建、已修改 结果=成功`）。
  - 使用示例：`python Member/scripts/xlsx2db.py --xlsx path\to\file.xlsx`

- `Member/scripts/db2xlsx.py`
  - 用途：导出 sqlite 表为 xlsx（用于可视化备份），会记录导出日志。
  - 使用示例：`python Member/scripts/db2xlsx.py --db Member/data/MemberList.db --table members`。

## 日志

- 日志文件位置：`Member/data/run.log`（由各脚本通过 `logging` 写入）。
- 日志格式统一为 `时间 - [等级] 消息`，批量导入脚本使用中文结构化字段，便于 grep/分析。

## 常见问题

- 配置未找到或脚本报错：检查 `Member/scripts/config.json` 中 `datapath` 是否正确，查看 `Member/data/run.log` 获取详细堆栈信息。
- Excel 导入列缺失：确定表头包含 `gaijin_id`, `name`, `state`, `join_date`, `landforce`, `airforce`, `navy`。


---

文件位置：`Member/scripts` 下的脚本为主要入口。
