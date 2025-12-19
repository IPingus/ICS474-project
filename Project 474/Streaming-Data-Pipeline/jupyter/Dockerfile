# ใช้ jupyter/base-notebook ที่มีแค่ Python และ Jupyter เป็นพื้นฐาน
FROM jupyter/base-notebook:python-3.11

# สลับเป็น root เพื่อติดตั้งโปรแกรม
USER root

# ติดตั้ง Java (Spark 3.5.1 ต้องการ Java 11) และเครื่องมืออื่นๆ
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jre-headless \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# กำหนดเวอร์ชันของ Spark และ Hadoop เพื่อให้แก้ไขง่าย
ENV SPARK_VERSION=3.5.1
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/usr/local/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
# บอก PySpark ให้ใช้ Python ที่อยู่ใน environment นี้
ENV PYSPARK_DRIVER_PYTHON=python
ENV PYSPARK_PYTHON=python

# ดาวน์โหลดและติดตั้ง Spark 3.4.0
RUN curl -sSL https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    | tar -xz -C /usr/local/ \
    && mv /usr/local/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} ${SPARK_HOME}

# สลับกลับไปเป็น user ปกติของ Jupyter
USER ${NB_UID}

# (ถ้ามี) ติดตั้งไลบรารี Python ที่ต้องการ
COPY --chown=${NB_UID}:${NB_GID} requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy spark-defaults.conf (if any)
COPY spark-defaults.conf $SPARK_HOME/conf/



