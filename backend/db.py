import os
import pymysql

from dotenv import load_dotenv
from urlextract import URLExtract

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PSWD = os.getenv("DB_PSWD")
DATABASE_NAME = os.getenv("DATABASE_NAME")
RES_TABLE_NAME = os.getenv("RES_TABLE_NAME")
METADATA_TABLE_NAME = os.getenv("METADATA_TABLE_NAME")
QUERY_TABLE_NAME = os.getenv("QUERY_TABLE_NAME")
QUERY_ID_START = os.getenv("QUERY_ID_START")
QUERY_ID_END = os.getenv("QUERY_ID_END")


def connect():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PSWD,
        database=DATABASE_NAME,
        charset="utf8",
    )


def fetch_as_object(query: str):
    db = connect()
    try:
        cursor = db.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in results]
    finally:
        db.close()


def fetch_all_qd_pair(amount: int):
    return fetch_as_object(
        f"SELECT DISTINCT dataset_id, query_id FROM {RES_TABLE_NAME} "
        f"WHERE query_id >= {QUERY_ID_START} AND query_id <= {QUERY_ID_END} "
        f"ORDER BY query_id {f'LIMIT {amount}' if amount > 0 else ''}"
    )


def fetch_unranked_qd_pair(amount: int, cond: str = ""):
    return fetch_as_object(
        f"SELECT DISTINCT dataset_id, query_id FROM {RES_TABLE_NAME} "
        f"WHERE `rank` < 0 AND query_id >= {QUERY_ID_START} AND query_id <= {QUERY_ID_END} "
        f"{f'AND {cond}' if len(cond) > 0 else ''} "
        f"ORDER BY query_id {f'LIMIT {amount}' if amount > 0 else ''}"
    )


def fetch_query(query_id: int):
    return fetch_as_object(
        f"SELECT * FROM {QUERY_TABLE_NAME} WHERE query_id = {query_id}"
    )[0]


def fetch_metadata(dataset_id: int):
    metadata = fetch_as_object(
        f"SELECT * FROM {METADATA_TABLE_NAME} WHERE dataset_id = {dataset_id}"
    )[0]
    metadata["url"] = URLExtract().find_urls(metadata["origin_metadata"])[0]
    return metadata


def update_ranking(dataset_id: int, query_id: int, rank: int):
    db = connect()
    try:
        cursor = db.cursor()
        cursor.execute(
            f"UPDATE {RES_TABLE_NAME} SET `rank` = {rank} "
            f"WHERE dataset_id = {dataset_id} AND query_id = {query_id}"
        )
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
