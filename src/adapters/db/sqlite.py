import sqlite3
from datetime import datetime
from typing import Dict, Any, List, Self

from src.adapters.db.base import BaseDBAdapter
from src.schemas.common import TableName

# Register datetime adapter for Python 3.12+
sqlite3.register_adapter(datetime, lambda val: val.isoformat())
sqlite3.register_converter("DATETIME", lambda val: datetime.fromisoformat(val.decode()))
sqlite3.register_converter(
    "TIMESTAMP", lambda val: datetime.fromisoformat(val.decode())
)


class SQLiteDBAdapter(BaseDBAdapter):
    table: str

    def __init__(self, logger, db_path: str = "db/local.sqlite3"):
        self.logger = logger
        self.db_path = db_path
        self.conn = sqlite3.connect(
            db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        self.cursor = self.conn.cursor()

    def use_db(self, db_name: str) -> Self:
        # SQLite doesn't really have multiple DBs in the same connection like Postgres
        # For simplicity, we just return self
        return self

    def use_table(self, table_name: TableName) -> Self:
        self.table = table_name
        return self

    def create_one(self, data: Dict[str, Any]) -> str:
        data = data.copy()
        if "id" in data and "_id" not in data:
            data["_id"] = data.pop("id")

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in range(len(data))])
        values = tuple(data.values())
        query = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.conn.commit()
        return data.get("_id") or str(self.cursor.lastrowid)

    def create_many(self, data: List[Dict[str, Any]]) -> List[str]:
        ids = []
        for row in data:
            ids.append(self.create_one(row))
        return ids

    def create_or_update_one(self, data: Dict[str, Any]) -> bool:
        _id = data.get("_id")
        if not _id:
            return bool(self.create_one(data))

        if self.read_one(_id):
            return self.update_one(_id, data)
        else:
            return bool(self.create_one(data))

    def read_one(self, _id: str, **kwargs) -> Dict[str, Any] | None:
        query = f"SELECT * FROM {self.table} WHERE _id=?"
        self.cursor.execute(query, (_id,))
        result = self.cursor.fetchone()
        if not result:
            return None
        columns = [col[0] for col in self.cursor.description]
        return dict(zip(columns, result))

    def read_many(
        self, where: Dict[str, Any] | None = None, limit: int | None = None, **kwargs
    ) -> List[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table}"
        values = ()
        if where:
            query_string = " AND ".join([f"{k}=?" for k in where.keys()])
            values = tuple(where.values())
            query += f" WHERE {query_string}"

        if limit:
            query += f" LIMIT {limit}"

        self.cursor.execute(query, values)
        results = self.cursor.fetchall()
        columns = [col[0] for col in self.cursor.description]
        return [dict(zip(columns, row)) for row in results]

    def update_one(self, _id: str, data: Dict[str, Any]) -> bool:
        columns = ", ".join([f"{k}=?" for k in data.keys()])
        values = tuple(data.values())
        query = f"UPDATE {self.table} SET {columns} WHERE _id=?"
        self.cursor.execute(query, values + (_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def update_many(self, query: Dict[str, Any], data: Dict[str, Any]) -> int:
        columns = ", ".join([f"{k}=?" for k in data.keys()])
        values = tuple(data.values()) + tuple(query.values())
        query_string = " AND ".join([f"{k}=?" for k in query.keys()])
        query = f"UPDATE {self.table} SET {columns} WHERE {query_string}"
        self.cursor.execute(query, values)
        self.conn.commit()
        return self.cursor.rowcount

    def delete_one(self, _id: str, **kwargs) -> bool:
        query = f"DELETE FROM {self.table} WHERE _id=?"
        self.cursor.execute(query, (_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_many(self, query: Dict[str, Any]) -> int:
        query_string = " AND ".join([f"{k}=?" for k in query.keys()])
        values = tuple(query.values())
        query = f"DELETE FROM {self.table} WHERE {query_string}"
        self.cursor.execute(query, values)
        self.conn.commit()
        return self.cursor.rowcount

    def create_table(self, table_name: TableName, **kwargs) -> Self:
        # SQLite needs a schema.
        self.table = table_name
        return self

    def drop_table(self, table_name: TableName) -> None:
        query = f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(query)
        self.conn.commit()
