import hashlib
from typing import Optional, Dict, Any
import pymysql
from pymysql.cursors import DictCursor

DB_CONFIG = {
    'host': 'becog.iptime.org',
    'port': 3306,
    'user': 'hsptuser001',
    'password': 'Core2026^^',
    'database': 'hspt_ai1',
    'charset': 'utf8mb4',
    'connect_timeout': 5,
}


def hash_mysql_password(password: str) -> str:
    step1 = hashlib.sha1(password.encode('utf-8')).digest()
    step2 = hashlib.sha1(step1).hexdigest().upper()
    return f'*{step2}'


def verify_password(plain_password: str, stored_hash: Optional[str]) -> bool:
    if not stored_hash:
        return False
    if stored_hash.startswith('*') and len(stored_hash) == 41:
        return hash_mysql_password(plain_password) == stored_hash.upper()
    return plain_password == stored_hash


def get_db_connection():
    return pymysql.connect(
        **DB_CONFIG,
        cursorclass=DictCursor,
    )


def authenticate_user(user_id: str, plain_password: str) -> Optional[Dict[str, Any]]:
    if not user_id or not plain_password:
        return None

    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            sql = 'SELECT userNo, userName, userId, userPasswd FROM hsptUser WHERE userId = %s LIMIT 1'
            cur.execute(sql, (user_id.strip(),))
            user = cur.fetchone()
            if not user:
                return None

            stored_hash = user.get('userPasswd', '')
            if verify_password(plain_password, stored_hash):
                return {
                    'userNo': user['userNo'],
                    'userName': user['userName'],
                    'userId': user['userId'],
                }
            return None
    finally:
        if conn:
            conn.close()
