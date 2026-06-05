import os
import json
import sqlite3
import argparse
from openpyxl import Workbook

def _load_config():
    cfg_file = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(cfg_file):
        try:
            with open(cfg_file, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
                return cfg.get('datapath')
        except Exception:
            return None
    return None

_cfg_datapath = _load_config()
if _cfg_datapath:
    datapath = _cfg_datapath
else:
    datapath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'MemberList.db'))


def db_to_excel_header(db_path: str, table_name: str, save_xlsx: str = None):
    """
    从sqlite表提取字段生成xlsx表头
    :param db_path: sqlite库路径
    :param table_name: 目标数据表名
    :param save_xlsx: excel保存路径
    """
    if not os.path.exists(db_path):
        print(f"数据库不存在：{db_path}")
        return

    # 默认输出xlsx路径：脚本同级目录
    if save_xlsx is None:
        save_xlsx = os.path.join(os.path.dirname(__file__),'..','data', f"MemberList.db 输入模板.xlsx")

    # 连接sqlite查字段
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # PRAGMA查表字段
    cur.execute(f"PRAGMA table_info({table_name});")
    res = cur.fetchall()
    # 第二列：字段名称
    header = [col[1] for col in res]
    cur.close()
    conn.close()

    # 写入Excel表头
    wb = Workbook()
    ws = wb.active
    ws.append(header)
    wb.save(save_xlsx)
    print(f"生成完成：{save_xlsx}")
    print("表头字段：", header)


def main():
    parser = argparse.ArgumentParser(description="从sqlite表提取字段生成xlsx表头")
    parser.add_argument('--db', help='sqlite数据库路径，默认为config.json中datapath', default=datapath)
    parser.add_argument('--table', help='目标数据表名，默认为members', default='members')
    parser.add_argument('--output', help='xlsx保存路径，默认为脚本同级目录下的data文件夹', default=None)
    args = parser.parse_args()
    db_to_excel_header(args.db, args.table, args.output)

if __name__ == "__main__":
    main()