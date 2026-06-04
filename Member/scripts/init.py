import sqlite3

datapath = "Member/data/MemberList.db"

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
    init_members()
    print("=78D13= Regiment Member List database initialized successfully.")