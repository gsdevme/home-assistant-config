import sqlite3
from datetime import datetime

# Path to the SQLite database
DB_PATH = '/config/home-assistant_v2.db'

def get_energy_usage():
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Define time range for the query (05:30-11:30)
    start_time = datetime.now().replace(hour=5, minute=30, second=0, microsecond=0)
    end_time = datetime.now().replace(hour=11, minute=30, second=0, microsecond=0)

    # Convert time to UNIX timestamp
    start_timestamp = int(start_time.timestamp())
    end_timestamp = int(end_time.timestamp())

    # Example query to get the energy usage between the time range (depends on your DB structure)
    cursor.execute('''
        SELECT SUM(state)
        FROM states
        WHERE entity_id = 'sensor.energy_usage'
        AND last_updated >= ?
        AND last_updated <= ?
    ''', (start_timestamp, end_timestamp))

    # Fetch result
    result = cursor.fetchone()[0]

    conn.close()

    return result if result else 0

if __name__ == '__main__':
    print(get_energy_usage())
