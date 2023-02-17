import sqlite3

connection = sqlite3.connect("bot.sqlite")
cursor = connection.cursor()

cursor.execute(
    """CREATE TABLE bgm (
        member_id TEXT,
        track_url TEXT
    )"""
)

cursor.execute(
    """CREATE TABLE favs (
        role_id TEXT,
        list_data TEXT
    )"""
)

connection.commit()
connection.close()
