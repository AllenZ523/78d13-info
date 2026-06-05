import sqlite3
import os
import json
import argparse
import sys
from datetime import datetime
import logging

# 基目录
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# 全局变量
DATA_DIR = None
datapath = None
config_path = None
log_path = None


def set_data_dir(path: str = None):
    """根据传入或默认路径设置 DATA_DIR、datapath、config_path 和 log_path。"""
    global DATA_DIR, datapath, config_path, log_path
    if path:
        DATA_DIR = os.path.abspath(path)
    else:
        DATA_DIR = os.path.join(BASE_DIR, 'data')
    os.makedirs(DATA_DIR, exist_ok=True)
    datapath = os.path.join(DATA_DIR, 'MemberList.db')
    config_path = os.path.join(BASE_DIR, 'scripts', 'config.json')
    log_path = os.path.join(BASE_DIR, 'data', 'run.log')
    logging.basicConfig(
        level=logging.INFO,
        handlers=[logging.FileHandler(log_path, encoding='utf-8')],
        format='%(asctime)s - [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S'
    )


def save_config(path: str = None):
    cfg = {
        'datapath': path or datapath,
        'logpath': log_path,
        "log_level": "INFO",
        "log_format": "%(asctime)s - [%(levelname)s] %(message)s",
        "date_fmt": "%Y-%m-%dT%H:%M:%S",
        "log_path": "./app.log",
        "encoding": "utf-8"
    }
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)



def init_members():
    conn = sqlite3.connect(datapath)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS members
                 (gaijin_id TEXT PRIMARY KEY,
                  name TEXT NOT NULL,
                  state TEXT NOT NULL DEFAULT 'N' CHECK(state IN('N','F','C')),
                  join_date TEXT NOT NULL,
                  landforce TEXT NOT NULL DEFAULT 'Uncertified' CHECK(landforce IN('Uncertified','Certified')),
                  airforce TEXT NOT NULL DEFAULT 'Uncertified' CHECK(airforce IN('Uncertified','Certified')),
                  navy TEXT NOT NULL DEFAULT 'Uncertified' CHECK(navy IN('Uncertified','Certified'))
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
    logging.info(f"数据库已在{datapath}初始化完成，配置已保存到{config_path}")