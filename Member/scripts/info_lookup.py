import sqlite3
import argparse
import os
import json

# 加载数据路径配置
def _load_datapath_from_script_config():
	cfg_file = os.path.join(os.path.dirname(__file__), 'config.json')
	if os.path.exists(cfg_file):
		try:
			with open(cfg_file, 'r', encoding='utf-8') as f:
				cfg = json.load(f)
				return cfg.get('datapath')
		except Exception:
			return None
	return None


_cfg_datapath = _load_datapath_from_script_config()
if _cfg_datapath:
	datapath = _cfg_datapath
else:
	datapath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'MemberList.db'))


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
		print("未找到记录。")
		return
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
		print_rows(rows)
	elif args.name:
		rows = query_by_name(args.name)
		print_rows(rows)
	elif args.all:
		rows = query_all()
		print_rows(rows)
	else:
		parser.print_help()


if __name__ == "__main__":
	main()

