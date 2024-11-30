import sqlite3
from datetime import datetime, timedelta 
import logging
from helpers import compute_running_total

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

def get_total_users_by_date():
    """Fetch the cumulative total number of users by date."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DATE(join_date) AS date, COUNT(*) 
                FROM users 
                GROUP BY DATE(join_date) 
                ORDER BY DATE(join_date)
            ''')
            results = [{'date': row[0], 'count': row[1]} for row in cursor.fetchall()]
            return compute_running_total(results)
        except Exception as e:
            logging.error(f"Failed to fetch total users by date: {e}")
            return []
        finally:
            conn.close()

def get_daily_new_users():
    """Fetch daily new user registrations grouped by date (date only)."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DATE(join_date) AS date, COUNT(*) 
                FROM users 
                GROUP BY DATE(join_date) 
                ORDER BY DATE(join_date)
            ''')
            results = cursor.fetchall()
            return [{'date': row[0], 'count': row[1]} for row in results]
        except Exception as e:
            logging.error(f"Failed to fetch daily new users: {e}")
            return []
        finally:
            conn.close()

def get_total_groups_by_date():
    """Fetch the cumulative total number of groups by date."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DATE(join_date) AS date, COUNT(*) 
                FROM groups 
                GROUP BY DATE(join_date) 
                ORDER BY DATE(join_date)
            ''')
            results = [{'date': row[0], 'count': row[1]} for row in cursor.fetchall()]
            return compute_running_total(results)
        except Exception as e:
            logging.error(f"Failed to fetch total groups by date: {e}")
            return []
        finally:
            conn.close()

def get_daily_new_groups():
    """Fetch daily new group registrations grouped by date (date only)."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DATE(join_date) AS date, COUNT(*) 
                FROM groups 
                GROUP BY DATE(join_date) 
                ORDER BY DATE(join_date)
            ''')
            results = cursor.fetchall()
            return [{'date': row[0], 'count': row[1]} for row in results]
        except Exception as e:
            logging.error(f"Failed to fetch daily new groups: {e}")
            return []
        finally:
            conn.close()

def get_total_messages_by_date():
    """Fetch the cumulative total messages sent by date."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DATE(message_date) AS date, COUNT(*) 
                FROM messages 
                GROUP BY DATE(message_date) 
                ORDER BY DATE(message_date)
            ''')
            results = [{'date': row[0], 'count': row[1]} for row in cursor.fetchall()]
            return compute_running_total(results)
        except Exception as e:
            logging.error(f"Failed to fetch total messages by date: {e}")
            return []
        finally:
            conn.close()

def get_daily_new_messages():
    """Fetch daily new messages sent grouped by date (date only)."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DATE(message_date) AS date, COUNT(*) 
                FROM messages 
                GROUP BY DATE(message_date) 
                ORDER BY DATE(message_date)
            ''')
            results = cursor.fetchall()
            return [{'date': row[0], 'count': row[1]} for row in results]
        except Exception as e:
            logging.error(f"Failed to fetch daily new messages: {e}")
            return []
        finally:
            conn.close()

def calculate_weekly_growth(table_name, date_column):
    """Calculate weekly growth percentage."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f'''
                SELECT DATE({date_column}) AS date, COUNT(*) AS count
                FROM {table_name}
                GROUP BY DATE({date_column})
                ORDER BY DATE({date_column})
            ''')
            data = cursor.fetchall()

            # logging.info(f"Raw data for {table_name}: {data}")

            growth_data = []
            for i in range(1, len(data)):
                previous_count = sum(row[1] for row in data[:i])
                current_count = sum(row[1] for row in data[:i+1])
                growth_percentage = ((current_count - previous_count) / previous_count) * 100 if previous_count > 0 else 0
                growth_data.append({'date': data[i][0], 'growth': growth_percentage})

            # logging.info(f"Growth data for {table_name}: {growth_data}")
            return growth_data
        except Exception as e:
            logging.error(f"Failed to calculate weekly growth for {table_name}: {e}")
            return []
        finally:
            conn.close()
