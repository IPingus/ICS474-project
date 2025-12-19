import sys
sys.path.append("/opt/airflow/plugins")  # บังคับ Python ให้เห็น folder plugins
import logging

from spark_utils import create_spark_connection, connect_to_kafka
from cassandra_utils import create_cassandra_connection, create_table, create_keyspace
from data_processing import create_selection_df_from_kafka

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_streaming():
   try : 
   # create spark connection
    spark_conn = create_spark_connection() # สร้างการเชื่อมต่อกับ Spark

    if spark_conn is not None:
            # connect to kafka with spark connection
            spark_df = connect_to_kafka(spark_conn) # สร้างการเชื่อมต่อกับ Kafka
            selection_df = create_selection_df_from_kafka(spark_df) # ดึงข้อมูลจาก Kafka
            session = create_cassandra_connection() # สร้างการเชื่อมต่อกับ Cassandra

            if session is not None:
                create_keyspace(session) # สร้าง Database / Schema บน Cassandra เรียกว่า Keyspace
                create_table(session) # สร้าง Table

                logging.info("Streaming is being started...")

                # เขียนข้อมูลลง Database
                streaming_query = (selection_df.writeStream
                                .format("org.apache.spark.sql.cassandra")
                                .option('checkpointLocation', '/tmp/checkpoint')
                                .option('keyspace', 'spark_streams')
                                .option('table', 'created_users')
                                .option("spark.cassandra.connection.host", "cassandra")
                                .option("spark.cassandra.connection.port", "9042")
                                .option("spark.cassandra.connection.local_dc", "datacenter1")
                                .trigger(processingTime="10 seconds") # เขียนค่าทุกๆ 10 วินาที
                                .start())

                # รอ mini-batch 30 วินาที
                streaming_query.awaitTermination(30)
                # จบ streaming
                streaming_query.stop()
                logging.info("Mini-batch streaming finished")

   except Exception as e:
       logging.exception("Streaming job failed: %s", e)

