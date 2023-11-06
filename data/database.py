import sqlite3 as sq

db = sq.connect('schedule.db')
cur = db.cursor()


async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS schedule("
                "id INTEGER PRIMAL KEY,"
                "mon TEXT DEFAULT NULL, "
                "tue TEXT DEFAULT NULL, "
                "wed TEXT DEFAULT NULL, "
                "thu TEXT DEFAULT NULL, "
                "fri TEXT DEFAULT NULL, "
                "sat TEXT DEFAULT NULL, "
                "sun TEXT DEFAULT NULL)")

db.commit()