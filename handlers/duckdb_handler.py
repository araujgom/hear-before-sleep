import duckdb
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class DuckDBHandler:
    def __init__(self, db_path='playlist_history.db'):
        try:
            self.conn = duckdb.connect(database=db_path)
            self.table_name = "playlist_history"
            self._ensure_table_exists()
        except Exception as e:
            logger.error(f"Failed to initialize DuckDB: {str(e)}")
            raise

    def _ensure_table_exists(self):
        self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                event_timestamp TIMESTAMP,
                event_date DATE,
                playlist_name VARCHAR
            )
        """)

    def log_playlist(self, playlist_name: str):
        now = datetime.now()
        self.conn.execute(f"""
            INSERT INTO {self.table_name} (event_timestamp, event_date, playlist_name)
            VALUES (?, ?, ?)
        """, (now, now.date(), playlist_name))

    def is_playlist_recent(self, playlist_name: str, days: int = 90) -> bool:
        cutoff_date = datetime.now() - timedelta(days=days)
        result = self.conn.execute(f"""
            SELECT COUNT(*) FROM {self.table_name}
            WHERE event_timestamp >= ? AND playlist_name = ?
        """, (cutoff_date, playlist_name)).fetchone()
        return result[0] > 0