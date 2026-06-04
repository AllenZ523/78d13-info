import sqlite3
import os
import json
import argparse

# 基目录
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# 全局变量
DATA_DIR = None
datapath = None
config_path = None


def set_data_dir(path: str = None):
    """根据传入或默认路径设置 DATA_DIR、datapath 和 config_path。"""
    global DATA_DIR, datapath, config_path
    if path:
        DATA_DIR = os.path.abspath(path)
    else:
        DATA_DIR = os.path.join(BASE_DIR, 'data')
    os.makedirs(DATA_DIR, exist_ok=True)
    datapath = os.path.join(DATA_DIR, 'MemberList.db')
    config_path = os.path.join(BASE_DIR, 'scripts', 'config.json')


def save_config(path: str = None):
    cfg = {
        'datapath': path or datapath
    }
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def load_config():
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    return None

def init_members():
    conn = sqlite3.connect(datapath)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS members
                 (gaijin_id TEXT PRIMARY KEY,
                  name TEXT NOT NULL,
                  state TEXT NOT NULL,
                  join_date TEXT NOT NULL
                 )''')
    c.execute('DROP TRIGGER IF EXISTS prevent_gaijin_id_update')
    c.execute('''CREATE TRIGGER prevent_gaijin_id_update
                 BEFORE UPDATE ON members
                 FOR EACH ROW
                 WHEN NEW.gaijin_id <> OLD.gaijin_id
                 BEGIN
                     SELECT RAISE(ABORT, 'gaijin_id is immutable');
                 END;''')
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='初始化成员数据库，并保存 data 目录到 config.json')
    parser.add_argument('--data-dir', '-d', help='数据目录路径（默认: Member/data）')
    args = parser.parse_args()

    # 设置路径并初始化
    set_data_dir(args.data_dir)
    init_members()
    # 保存配置
    save_config(datapath)
    print(f"=78D13= 联队成员数据库已在 {datapath} 初始化，并已保存配置到 {config_path}。")