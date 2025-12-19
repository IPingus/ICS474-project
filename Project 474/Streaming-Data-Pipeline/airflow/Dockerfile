FROM apache/airflow:2.7.3-python3.11

USER root

# ติดตั้ง Java + utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jdk \
    vim curl wget \
    && rm -rf /var/lib/apt/lists/*

# ตั้ง JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

USER airflow

# คัดลอก requirements.txt
COPY requirements.txt /opt/airflow/requirements.txt

# ติดตั้ง python dependencies
RUN pip install --upgrade pip && pip install -r /opt/airflow/requirements.txt

WORKDIR /opt/airflow
