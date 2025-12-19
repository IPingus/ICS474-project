import logging
from pyspark.sql import SparkSession

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# ฟังก์ชันสร้างการเชื่อมต่อกับ Spark
def create_spark_connection():
    s_conn = None

    try:
        s_conn = (SparkSession.builder 
            .appName('SparkDataStreaming') 
            .config('spark.jars.packages', # โหลดแพคเกจสำหรับ Spark
                    "com.datastax.spark:spark-cassandra-connector_2.12:3.5.0," # โหลดแพคเกจสำหรับเชื่อมต่อกับ Cassandra
                    "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") # โหลดแพคเกจสำหรับเชื่อมต่อกับ Kafka 
            .config('spark.cassandra.connection.host', 'localhost') # กำหนดที่อยู่การเชื่อมต่อกับ Cassandra
            .getOrCreate())
        
        s_conn.sparkContext.setLogLevel("ERROR")
        logging.info("Spark connection created successfully!")
    except Exception as e:
        logging.error(f"Couldn't create the spark session due to exception {e}")

    return s_conn


# ฟังก์ชันการเชื่อมต่อกับ Kafka
def connect_to_kafka(spark_conn):
    spark_df = None
    try:
        spark_df = (spark_conn.readStream \
            .format('kafka') \
            .option('kafka.bootstrap.servers', 'broker:29092') # กำหนดที่อยู่การเชื่อมต่อกับ Kafka Broker
            .option('subscribe', 'users_created') # กำหนดชื่อของ Kafka Topic ที่จะดึงข้อมูลมา
            .option('startingOffsets', 'earliest') # กำหนดว่าจะดึงข้อมูลจากเริ่มต้นหรือไม่ earliest (อ่านจากที่เริ่มต้น) หรือ latest (อ่านจากข้อมูลที่เข้ามาล่าสุด)
            .option("maxOffsetsPerTrigger", 50)  # อ่านทีละ 50 records
            .load())
        logging.info("kafka dataframe created successfully")
    except Exception as e:
        logging.warning(f"kafka dataframe could not be created because: {e}")

    return spark_df