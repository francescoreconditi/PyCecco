import logging
import sqlite3
import sys
import traceback
from contextlib import contextmanager


@contextmanager
def open_db(db_file: str):
    """Connessione con il DB

    Args:
        db_file (str): Path del DB

    Yields:
        'cursore sqlite': Cursore creato dalla Connessione
    """
    conn = sqlite3.connect(db_file)

    try:
        logging.info("Creazione Connessione ...")
        yield conn.cursor()

    except sqlite3.Error as err_sql:
        logging.error(('SQLite error: %s' % (' '.join(err_sql.args))))
        logging.error(f"Exception class is: {err_sql.__class__}")
        logging.error('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        logging.error(traceback.format_exception(exc_type, exc_value, exc_tb))

    finally:
        logging.info("Chiusura Connessione ...")
        conn.commit()
        conn.close()


def main():
    logging.basicConfig(level=logging.INFO)
    with open_db(db_file="application.db") as cursor:
        cursor.execute("SELECT * FROM blogs")
        logging.info(cursor.fetchall())


if __name__ == "__main__":
    main()
