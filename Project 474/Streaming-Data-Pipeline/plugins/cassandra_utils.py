import logging
from cassandra.cluster import Cluster

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# ฟังก์ชันสร้างการเชื่อมต่อกับ Cassandra
def create_cassandra_connection():
    try:
        # connecting to the cassandra cluster
        cluster = Cluster(contact_points=['cassandra'], port=9042) # กำหนดที่อยู่ hostname การเชื่อมต่อกับ Cassandra
        cas_session = cluster.connect() # สร้างการเชื่อมต่อ

        logging.info("Connected to Cassandra!")
        return cas_session
    except Exception as e:
        logging.error(f"Could not create cassandra connection due to {e}")
        return None

def create_keyspace(session):
    # สร้าง Database / Schema บน Cassandra เรียกว่า Keyspace
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS spark_streams
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
    """)

    print("Keyspace created successfully!")

def create_table(session):
    # สร้าง Table
    session.execute("""
    CREATE TABLE IF NOT EXISTS spark_streams.created_users (
        id UUID PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        gender TEXT,
        address TEXT,
        post_code TEXT,
        email TEXT,
        username TEXT,
        registered_date TEXT,
        phone TEXT,
        picture TEXT) WITH default_time_to_live = 600;
    """)

    print("Table created successfully!")