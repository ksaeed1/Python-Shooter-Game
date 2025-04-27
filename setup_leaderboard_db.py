import sqlite3
import os

db_path = os.path.join("assets", "data", "leaderboard.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT NOT NULL,
        score INTEGER NOT NULL,
        language TEXT,
        timestamp TEXT
    )
''')

conn.commit()
conn.close()

print("Leaderboard database setup complete.")
