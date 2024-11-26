import sqlite3
from datetime import datetime, timedelta 
import logging

# Database file path
DB_FILE = './database/borhan_telegram.db'

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    """Establish a database connection."""
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to database: {e}")
        return None

# User operations
def get_user_count():
    """Get the total number of users."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM users')
            count = cursor.fetchone()[0]
            return count
        except Exception as e:
            logging.error(f"Failed to get user count: {e}")
            return 0
        finally:
            conn.close()

# Group operations
def get_group_count():
    """Get the total number of groups."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM groups')
            count = cursor.fetchone()[0]
            return count
        except Exception as e:
            logging.error(f"Failed to get group count: {e}")
            return 0
        finally:
            conn.close()

# Message operations
def get_message_count_today():
    """Get the total number of messages sent today."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute('SELECT COUNT(*) FROM messages WHERE message_date = ?', (today,))
            count = cursor.fetchone()[0]
            return count
        except Exception as e:
            logging.error(f"Failed to get today's message count: {e}")
            return 0
        finally:
            conn.close()
# def get_message_count_yesterday():
#     """Get the total number of messages sent yesterday."""
#     conn = get_db_connection()
#     if conn:
#         try:
#             cursor = conn.cursor()
#             # Calculate yesterday's date
#             yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
#             cursor.execute('SELECT COUNT(*) FROM messages WHERE message_date = ?', (yesterday,))
#             count = cursor.fetchone()[0]
#             return count
#         except Exception as e:
#             logging.error(f"Failed to get yesterday's message count: {e}")
#             return 0
#         finally:
#             conn.close()

