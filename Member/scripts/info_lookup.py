import sqlite3
import argparse
import os
import json
import sys

def _load_config():
    cfg_file = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(cfg_file):
        try:
            with open(cfg_file, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
                return cfg
        except Exception:
            return {}
    return {}

cfg_dict = _load_config()


if cfg_dict.get("datapath"):
    datapath = cfg_dict["datapath"]
else:
    datapath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'MemberList.db'))


if cfg_dict.get("logpath"):
    log_path = cfg_dict["logpath"]
else:
    log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'run.log'))


def get_connection():
	return sqlite3.connect(datapath)


def query_by_gaijin(gaijin_id):
	conn = get_connection()
	c = conn.cursor()
	c.execute("SELECT * FROM members WHERE gaijin_id = ?", (gaijin_id,))
	rows = c.fetchall()
	conn.close()
	return rows


def query_by_name(name):
	conn = get_connection()
	c = conn.cursor()
	c.execute("SELECT * FROM members WHERE name LIKE ?", ('%'+name+'%',))
	rows = c.fetchall()
	conn.close()
	return rows


def query_all():
	conn = get_connection()
	c = conn.cursor()
	c.execute("SELECT * FROM members")
	rows = c.fetchall()
	conn.close()
	return rows


def print_member():
	conn = get_connection()
	c = conn.cursor()
	c.execute("PRAGMA table_info(members);")
	header = [col[1] for col in c.fetchall()]
	print(" | ".join(header))


def print_rows(rows):
	if not rows:
		print("未找到记录")
		# 对于查询单条记录的场景，返回非零以便调用者判断未找到
		sys.exit(1)
	for r in rows:
		print(" | ".join(str(x) for x in r))


def main():
	parser = argparse.ArgumentParser(description="查询成员信息（按 name 或 gaijin_id）")
	parser.add_argument("--gaijin", help="按 gaijin_id 查询")
	parser.add_argument("--name", help="按 name 查询（支持模糊匹配）")
	parser.add_argument("--all", action="store_true", help="列出所有成员")
	args = parser.parse_args()

	if not os.path.exists(datapath):
		print(f"数据库文件不存在: {datapath}")
		return

	print_member()
	
	if args.gaijin:
		rows = query_by_gaijin(args.gaijin)
		if not rows:
			print("未找到记录")
			sys.exit(1)
		print_rows(rows)
	elif args.name:
		rows = query_by_name(args.name)
		if not rows:
			print("未找到记录")
			sys.exit(1)
		print_rows(rows)
	elif args.all:
		rows = query_all()
		print_rows(rows)
		print(f"总记录数: {len(rows)}")
	else:
		parser.print_help()


if __name__ == "__main__":
	main()

