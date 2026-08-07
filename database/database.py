import sqlite3
import json

class DatabaseManager:

    def __init__(self,db_path="database/search_engine.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS pages(
            id INTEGER PRIMARY KEY,
            url TEXT UNIQUE,
            title TEXT,
            status INTEGER,
            depth INTEGER,
            timestamp TEXT
            )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS terms(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            term TEXT UNIQUE

        )
    """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS postings(

            term_id INTEGER,

            page_id INTEGER,

            frequency INTEGER,

            positions TEXT,

            PRIMARY KEY(term_id,page_id),

            FOREIGN KEY(term_id) REFERENCES terms(id),

            FOREIGN KEY(page_id) REFERENCES pages(id)

        )
    """)

        self.conn.commit()

    def close(self):
        self.conn.close()

    def get_or_create_term(self,term):

        self.cursor.execute(
            """
            SELECT id from terms where term=?
            """,
            (term,)
        )

        result = self.cursor.fetchone()
        if result:
            return result[0]

        self.cursor.execute(
            """
            INSERT INTO terms(term)
            VALUES(?)
            """,
            (term,)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_posting(self,term_id,page_id,frequency,positions):

        self.cursor.execute(
            """
            INSERT OR REPLACE INTO postings
            (term_id,page_id,frequency,positions)
            VALUES (?,?,?,?)
            """,
            (term_id,page_id,frequency,json.dumps(positions))
        )

    def commit(self):
        self.conn.commit()

    def get_term_id(self,term):
        self.cursor.execute(
            """
            SELECT id FROM terms WHERE term = ?
            """,
            (term,)
        )
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def get_postings(self,term):
        term_id = self.get_term_id(term)
        if term_id is None:
            return []
        self.cursor.execute(
            """
            SELECT p.page_id,pg.title,pg.url,p.frequency,p.positions
            FROM postings p
            JOIN pages pg ON p.page_id=pg.id
            WHERE p.term_id = ?
            """,
            (term_id,)
        )
        results = []
        for page_id,title,url,frequency,positions in self.cursor.fetchall():
            results.append(
                (
                    page_id,title,url,frequency,json.loads(positions)
                )
            )
        return results

    def get_term_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM terms")
        return self.cursor.fetchone()[0]

    def get_posting_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM postings")
        return self.cursor.fetchone()[0]

    def get_page(self,page_id):
        self.cursor.execute(
            """
            SELECT title,url 
            FROM pages 
            WHERE id = ?
            """,
            (page_id,)
        )

        return self.cursor.fetchone()

    def get_total_documents(self):
        self.cursor.execute(
            """
            SELECT COUNT(*) FROM pages
            """
        )
        return self.cursor.fetchone()[0]

    def get_document_frequency(self,term):
        term_id = self.get_term_id(term)
        if term_id is None:
            return 0
        self.cursor.execute(
            """
            SELECT COUNT(*) FROM postings
            WHERE term_id = ?
            """,
            (term_id,)
        )
        return self.cursor.fetchone()[0]

    def get_postings_with_positions(self,term):
        term_id = self.get_term_id(term)

        if term_id is None:
            return []

        self.cursor.execute(
            """
            SELECT page_id,positions
            FROM postings 
            WHERE term_id = ?
            """,
            (term_id,)
        )

        results = []
        for page_id,positions in self.cursor.fetchall():
            results.append(
                (page_id,json.loads(positions))
            )
        return results
