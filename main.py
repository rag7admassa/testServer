import sqlite3

from fastapi import FastAPI

DB_PATH = "names.db"
PORT = 8002

app = FastAPI(title="FastAPI Training Project")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.on_event("startup")
def setup_database():
    conn = get_db()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS names (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)"
    )
    count = conn.execute("SELECT COUNT(*) FROM names").fetchone()[0]
    if count == 0:
        sample_names = ["Judy", "Raghad", "Amal", "Saad", "Yahya"]
        conn.executemany(
            "INSERT INTO names (name) VALUES (?)", [(n,) for n in sample_names]
        )
        conn.commit()
    conn.close()


@app.get("/hello")
def hello():
    return {"message": "مرحبا"}


@app.get("/names")
def get_names():
    conn = get_db()
    rows = conn.execute("SELECT id, name FROM names").fetchall()
    conn.close()
    return [dict(row) for row in rows]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
