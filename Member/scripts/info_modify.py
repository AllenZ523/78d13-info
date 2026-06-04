import sqlite3
import argparse
import os
import json
from datetime import datetime

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


def fetch_member(gaijin_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM members WHERE gaijin_id = ?", (gaijin_id,))
    row = c.fetchone()
    conn.close()
    return row


def update_member(gaijin_id, name=None, state=None, join_date=None, landforce=None, airforce=None, navy=None):
    if name is None and state is None and join_date is None and landforce is None and airforce is None and navy is None:
        print("未提供要更新的字段，请使用 --name 和/或 --state 和/或 --time 和/或 --landforce 和/或 --airforce 和/或 --navy。")
        return False

    conn = get_connection()
    c = conn.cursor()
    fields = []
    params = []


    if name is not None:
        fields.append("name = ?")
        params.append(name)
    if state is not None:
        fields.append("state = ?")
        params.append(state)
    if join_date is not None:
        fields.append("join_date = ?")
        params.append(join_date)
    if landforce is not None:
        if landforce == "C" or landforce == "c":
            landforce = "Certified"
        elif landforce == "U" or landforce == "u":
            landforce = "Uncertified"
        fields.append("landforce = ?")
        params.append(landforce)
    if airforce is not None:
        if airforce == "C" or airforce == "c":
            airforce = "Certified"
        elif airforce == "U" or airforce == "u":
            airforce = "Uncertified"
        fields.append("airforce = ?")
        params.append(airforce)
    if navy is not None:
        if navy == "C" or navy == "c":
            navy = "Certified"
        elif navy == "U" or navy == "u":
            navy = "Uncertified"
        fields.append("navy = ?")
        params.append(navy)

    params.append(gaijin_id)
    sql = f"UPDATE members SET {', '.join(fields)} WHERE gaijin_id = ?"
    try:
        c.execute(sql, tuple(params))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"更新失败：{e}")
        conn.close()
        return False
    changed = c.rowcount
    conn.close()
    if changed == 0:
        print("未找到匹配的 gaijin_id，未做任何修改。")
        return False
    return True


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
    parser = argparse.ArgumentParser(description="按 gaijin_id 修改成员信息（name/state）")
    parser.add_argument('gaijin_id', help='要修改的盖金号（必填）')
    parser.add_argument('--name', help='新的姓名')
    parser.add_argument('--state', help='新的阶段')
    parser.add_argument('--time', help='新的加入日期（格式: YYYY-MM-DD）')
    parser.add_argument('--landforce', help='新的陆军认证状态（Uncertified/Certified）')
    parser.add_argument('--airforce', help='新的空军认证状态（Uncertified/Certified）')
    parser.add_argument('--navy', help='新的海军认证状态（Uncertified/Certified）')

    args = parser.parse_args()

    if not os.path.exists(datapath):
        print(f"数据库文件不存在: {datapath}。请先运行初始化脚本或检查路径。")
        return

    gaijin = args.gaijin_id.strip()
    before = fetch_member(gaijin)

    if before is None:
        print("未找到对应成员，无法修改。")
        return

    print("修改前：")
    print_member()
    print_rows([before])

    ok = update_member(gaijin, name=args.name, state=args.state, join_date=args.time, landforce=args.landforce, airforce=args.airforce, navy=args.navy)
    if not ok:
        print("更新操作未成功。")
        return

    after = fetch_member(gaijin)
    print("修改后：")
    print_member()
    print_rows([after])


if __name__ == '__main__':
    main()
