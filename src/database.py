import sqlite3


class DatabaseRepository:
    MAX_NAME_LEN = 256
    MAX_MESSAGE_LEN = 8096

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL CHECK (length(name) <= 256),
                message TEXT NOT NULL CHECK (length(message) <= 8096)
            )
            """
        )
        self._conn.commit()

    @staticmethod
    def _validate_id(comment_id):
        if not isinstance(comment_id, int) or isinstance(comment_id, bool):
            raise TypeError("comment_id must be int")

    @classmethod
    def _validate_name(cls, username):
        if not isinstance(username, str):
            raise TypeError("username must be str")
        if len(username) > cls.MAX_NAME_LEN:
            raise ValueError(f"username length must be <= {cls.MAX_NAME_LEN}")

    @classmethod
    def _validate_message(cls, message):
        if not isinstance(message, str):
            raise TypeError("message must be str")
        if len(message) > cls.MAX_MESSAGE_LEN:
            raise ValueError(f"message length must be <= {cls.MAX_MESSAGE_LEN}")

    def get_by_id(self, comment_id):
        self._validate_id(comment_id)
        row = self._conn.execute(
            "SELECT id, name, message FROM comments WHERE id = ?",
            (comment_id,),
        ).fetchone()
        return dict(row) if row else None

    def get_by_name(self, username):
        self._validate_name(username)
        rows = self._conn.execute(
            "SELECT id, name, message FROM comments WHERE name = ?",
            (username,),
        ).fetchall()
        return [dict(r) for r in rows]

    def add(self, comment_id, username, message):
        self._validate_id(comment_id)
        self._validate_name(username)
        self._validate_message(message)
        try:
            with self._conn:
                self._conn.execute(
                    "INSERT INTO comments (id, name, message) VALUES (?, ?, ?)",
                    (comment_id, username, message),
                )
        except sqlite3.IntegrityError as exc:
            raise ValueError(
                f"comment with id {comment_id} already exists"
            ) from exc
        return True

    def update(self, comment_id, new_message):
        self._validate_id(comment_id)
        self._validate_message(new_message)
        with self._conn:
            cursor = self._conn.execute(
                "UPDATE comments SET message = ? WHERE id = ?",
                (new_message, comment_id),
            )
        return cursor.rowcount > 0

    def delete(self, comment_id):
        self._validate_id(comment_id)
        with self._conn:
            cursor = self._conn.execute(
                "DELETE FROM comments WHERE id = ?",
                (comment_id,),
            )
        return cursor.rowcount > 0

    def close(self):
        self._conn.close()
