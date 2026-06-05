import os
import json
import sqlite3
import argparse
import logging
from datetime import datetime
from openpyxl import Workbook


def _load_config():
    cfg_file = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(cfg_file):
        try:
            with open(cfg_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


cfg = _load_config()

# 数据库与日志路径
datapath_default = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'MemberList.db'))
log_path_default = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'run.log'))

datapath_cfg = cfg.get('datapath') or datapath_default
log_path = cfg.get('logpath') or log_path_default


def export_table(db_path: str, table_name: str, output_xlsx: str):
    """从 sqlite 表导出为 xlsx（包含表头），并返回导出行数。"""
    if not os.path.exists(db_path):
        logging.error(f"数据库文件不存在：{db_path}")
        return 1

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    try:
        cur.execute(f"PRAGMA table_info({table_name});")
        cols = cur.fetchall()
        if not cols:
            logging.error(f"表不存在或没有字段：{table_name}")
            return 1
        headers = [c[1] for c in cols]

        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()

        wb = Workbook()
        ws = wb.active
        ws.append(headers)
        for r in rows:
            ws.append(list(r))

        os.makedirs(os.path.dirname(output_xlsx), exist_ok=True)
        wb.save(output_xlsx)

        logging.info(f"导出表 {table_name} 到 {output_xlsx}，记录数={len(rows)}")
        return 0

    except Exception as e:
        logging.exception(f"导出失败：{e}")
        return 1
    finally:
        cur.close()
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="将 sqlite 表导出为 xlsx，用于可视化备份并记录日志")
    parser.add_argument('--db', help='sqlite 数据库路径（默认使用 config.json 中 datapath 或 Member/data/MemberList.db）', default=datapath_cfg)
    parser.add_argument('--table', help='要导出的表名（默认: members）', default='members')
    parser.add_argument('--output', help='输出 xlsx 路径（默认: data/{table}_backup_YYYYmmdd_HHMMSS.xlsx）', default=None)
    args = parser.parse_args()

    # 配置 logging
    logging.basicConfig(
        level=logging.INFO,
        handlers=[logging.FileHandler(log_path, encoding='utf-8')],
        format='%(asctime)s - [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S'
    )

    db = args.db
    table = args.table
    if args.output:
        out = args.output
    else:
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        out = os.path.join(out_dir, f"{table}_backup_{ts}.xlsx")

    logging.info(f"开始导出：db={db}, table={table}, output={out}")
    code = export_table(db, table, out)
    if code == 0:
        logging.info("导出完成")
    else:
        logging.error("导出未成功，请查看前面的错误日志")
    raise SystemExit(code)


if __name__ == '__main__':
    main()
