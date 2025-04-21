import sqlite3, pathlib, json
import sqlite_vec
from sqlite_vec import serialize_float32

DIM = 3072  # Only works for text-embedding-3-large
TABLE = "doc_vectors"


def get_conn(db_path: str) -> sqlite3.Connection:
    path = pathlib.Path(db_path).expanduser()
    conn = sqlite3.connect(path)
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)

    conn.execute(
        f"""
        create virtual table if not exists {TABLE}
        using vec0(
            embedding float[{DIM}],
            content text,
            metadata text
        )
        """
    )
    return conn


def insert_nodes(conn: sqlite3.Connection, nodes):
    cur = conn.cursor()
    for n in nodes:
        cur.execute(
            f"insert into {TABLE}(embedding, content, metadata) values (?,?,?)",
            (
                serialize_float32(n.embedding),
                n.text,
                json.dumps(n.metadata),
            ),
        )
    conn.commit()
    return cur.rowcount
