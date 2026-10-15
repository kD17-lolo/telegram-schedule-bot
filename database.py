import sqlite3

DB_NAME = "storage.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            file_id TEXT NOT NULL,
            file_type TEXT NOT NULL,
            file_name TEXT,
            category TEXT NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_state (
            user_id INTEGER PRIMARY KEY,
            state TEXT,
            temp_file_id TEXT,
            temp_file_type TEXT,
            temp_file_name TEXT
        )
    """)

    conn.commit()
    conn.close()


# === Файлы ===
def add_file(user_id, file_id, file_type, file_name, category):
    conn = get_db()
    conn.execute(
        "INSERT INTO files (user_id, file_id, file_type, file_name, category) VALUES (?, ?, ?, ?, ?)",
        (user_id, file_id, file_type, file_name, category.lower())
    )
    conn.commit()
    conn.close()


def get_user_categories(user_id):
    conn = get_db()
    cursor = conn.execute(
        "SELECT DISTINCT category FROM files WHERE user_id = ? ORDER BY category",
        (user_id,)
    )
    cats = [row["category"] for row in cursor.fetchall()]
    conn.close()
    return cats


def search_files(user_id, category, offset=0, limit=5):
    conn = get_db()
    cursor = conn.execute(
        "SELECT * FROM files WHERE user_id = ? AND category = ? ORDER BY added_at DESC LIMIT ? OFFSET ?",
        (user_id, category.lower(), limit, offset)
    )
    files = [dict(row) for row in cursor.fetchall()]
    count_row = conn.execute(
        "SELECT COUNT(*) as total FROM files WHERE user_id = ? AND category = ?",
        (user_id, category.lower())
    ).fetchone()
    total = count_row["total"] if count_row else 0
    conn.close()
    return files, total


def get_category_file_count(user_id, category):
    conn = get_db()
    row = conn.execute(
        "SELECT COUNT(*) as count FROM files WHERE user_id = ? AND category = ?",
        (user_id, category.lower())
    ).fetchone()
    conn.close()
    return row["count"] if row else 0


def delete_file(file_id, user_id):
    conn = get_db()
    conn.execute("DELETE FROM files WHERE id = ? AND user_id = ?", (file_id, user_id))
    conn.commit()
    conn.close()


def delete_category(user_id, category):
    conn = get_db()
    conn.execute("DELETE FROM files WHERE user_id = ? AND category = ?", (user_id, category.lower()))
    conn.commit()
    conn.close()


# === Состояние ===
def set_user_state(user_id, state, temp_file_id=None, temp_file_type=None, temp_file_name=None):
    conn = get_db()
    conn.execute(
        "INSERT OR REPLACE INTO user_state (user_id, state, temp_file_id, temp_file_type, temp_file_name) VALUES (?, ?, ?, ?, ?)",
        (user_id, state, temp_file_id, temp_file_type, temp_file_name)
    )
    conn.commit()
    conn.close()


def get_user_state(user_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM user_state WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def clear_user_state(user_id):
    conn = get_db()
    conn.execute("DELETE FROM user_state WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()