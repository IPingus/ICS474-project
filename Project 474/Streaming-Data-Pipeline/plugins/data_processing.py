import logging
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# ฟังก์ชันประมวลผลข้อมูลด้วย Spark และ Data Quality Checks
def create_selection_df_from_kafka(spark_df):
    """
    แปลงข้อมูลจาก Kafka เป็น Spark DataFrame และทำ Data Quality Checks
    - Schema Enforcement
    - Missing Value Check
    - Business Rule Validation (regex, allowed values)
    - Deduplication
    - ส่งข้อมูลไม่ผ่าน validation ไป Dead-letter topic (optional)
    
    Args:
        spark_df: input streaming DataFrame จาก Kafka
        kafka_producer_invalid: KafkaProducer สำหรับส่งข้อมูล invalid (optional)
    
    Returns:
        validated_df: Spark DataFrame พร้อมส่งต่อ (validated)
    """
    # -------------------- 1. Define Schema --------------------
    # กำหนดโครงสร้างข้อมูลที่จะนำเข้า
    schema = StructType([
        StructField("id", StringType(), False),
        StructField("first_name", StringType(), False),
        StructField("last_name", StringType(), False),
        StructField("gender", StringType(), False),
        StructField("address", StringType(), False),
        StructField("post_code", StringType(), False),
        StructField("email", StringType(), False),
        StructField("username", StringType(), False),
        StructField("registered_date", StringType(), False),
        StructField("phone", StringType(), False),
        StructField("picture", StringType(), False)
    ])

    # -------------------- 2. Parse JSON and Enforce Schema --------------------
    # ดึงและแปลงข้อมูลจาก kafka เป็น Spark DataFrame 
    df = (spark_df.selectExpr("CAST(value AS STRING)") # เลือกเฉพาะคอลัมน์ value แปลงเป็น String 
        .select(from_json(col('value'), schema).alias('data')).select("data.*")) # อ่านข้อมูลจาก json ที่เป็น value และจัดข้อมูลตาม schema
    logging.info("Schema applied and JSON parsed.")

    # -------------------- 3. Missing Value Check --------------------
    df_non_null = df.dropna(subset=["id", "email", "registered_date"]) # ลบตัวที่มีค่าเป็น null ใน col พวกนี้
    logging.info("Dropped records with null id, email, or registered_date.")

    # -------------------- 4. Business Rule Validation --------------------
    df_valid = df_non_null.filter( # filter แค่ค่าที่ตรงตาม regex ตามแบบนี้
        col("email").rlike(r".+@.+\..+") & # รูปแบบของ email pattern
        col("gender").isin("male", "female") & # จะมีแค่ 2 ค่านี้เท่านั้น
        col("id").rlike("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
    )
    logging.info("Applied business rule validation.")

    # -------------------- 5. Deduplicate --------------------
    df_deduped = df_valid.dropDuplicates(["id"]) # ลบแถวที่มี id ซ้ำกัน
    logging.info("Deduplicated based on id.")

    return df_deduped