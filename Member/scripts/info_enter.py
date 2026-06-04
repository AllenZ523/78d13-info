import sqlite3
import argparse
from datetime import datetime, timedelta, UTC
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


def add_member(gaijin_id: str, name: str) -> bool:
	"""Insert a new member. Returns True on success, False on failure."""
	join_date = (datetime.now(UTC) + timedelta(hours=8)).strftime("%Y-%m-%d")
	state = 'N'
	conn = get_connection()
	c = conn.cursor()
	try:
		c.execute("INSERT INTO members (gaijin_id, name, state, join_date) VALUES (?,?,?,?)",
				  (gaijin_id, name, state, join_date))
		conn.commit()
	except sqlite3.IntegrityError as e:
		print(f"插入失败：{e}")
		conn.close()
		return False
	conn.close()
	print(f"已添加：gaijin_id={gaijin_id}, name={name}, state={state}, join_date={join_date}")
	return True


def main():
	parser = argparse.ArgumentParser(description="向成员数据库插入记录：gaijin_id, name")
	parser.add_argument('gaijin_id', help='盖金号（唯一且必填）')
	parser.add_argument('name', help='游戏名称（必填）')
	args = parser.parse_args()

	if not os.path.exists(datapath):
		print(f"数据库文件不存在: {datapath}。请先运行初始化脚本。")
		return

	if not args.gaijin_id or not args.name:
		print("gaijin_id 和 name 都为必填字段。")
		return

	add_member(args.gaijin_id.strip(), args.name.strip())


if __name__ == '__main__':
	main()
