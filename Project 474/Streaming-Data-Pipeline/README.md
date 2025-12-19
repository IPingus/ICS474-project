
# 📡 Streaming Data Engineering Project

> Real-time data engineering project using Docker, Kafka, Spark Structured Streaming, Cassandra and Airflow

## 🧾 Project Overview

This project demonstrates a real-time data pipeline for streaming ingestion, processing, and storage.
It covers orchestration (Airflow), streaming processing (Spark Structured Streaming), real-time messaging (Kafka), scalable storage (Cassandra), and analytics (Jupyter).

## ⚙️ Architecture Diagram
![Arch_Diagram](images/Architecture_Diagram.png)

## 💡 Technology Stack

**Programming Languages :**
- Python
- SQL

**Data Streaming & Orchestration :**
- Apache Kafka
- Apache Airflow
- Apache Spark (Structured Streaming)

**Infrastructure & Storage  :**
- Docker
- Cassandra

**Visualization :**
- Jupyter Notebook

## 🐳 Docker / Infrastructure Setup

![Docker_Setup](images/Docker_Service.png)

**Services included :**
- `zookeeper`, `broker`, `schema-registry`, `control-center`
- `airflow-webserver`, `airflow-scheduler`, `postgres`
- `spark-master`, `spark-worker`
- `cassandra_db`
- `jupyter`
- `producer` *(running inside container)*

## 💾 Real-time Storage (Cassandra)

![Cassandra_Storage](images/Database_Cassandra.png)

**Key Features :**
- Uses **Cassandra** for scalable, fault-tolerant storage.
- Processed streaming data from Spark is written into Cassandra.
- Supports CQL queries for downstream analytics.

## ⚡ Spark Cluster (Master/Workers)

![Spark_Cluster](images/Spark_Cluster.png)

**This cluster runs in standalone mode with :**
- 1 Spark Master
- 1 Spark Workers
- Deployed inside Docker containers

## 📂 Data Ingestion

### 1. Kafka Producer
```json
{
  "id": "8e7fce72-89bc-4685-a747-b0f8624e020d",
  "first_name": "Elaine",
  "last_name": "Harvey",
  "gender": "female",
  "address": "353 Blossom Hill Rd, Dayton, Vermont, United States",
  "post_code": 18511,
  "email": "elaine.harvey@example.com",
  "username": "smallcat386",
  "dob": "1999-04-02T12:55:47.460Z",
  "registered_date": "2019-10-19T01:25:43.507Z",
  "phone": "(456) 390-1836",
  "picture": "https://randomuser.me/api/portraits/med/women/0.jpg"
}
```
- Custom producer generates real-time events.
- Data is published to Kafka topics, consumed by Spark.
- Producer runs inside container.
- Kafka Control Center available at http://localhost:9021.

### 2. Kafka Control Center Overview

**Kafka Brokers :**

  Shows the Kafka brokers managing the streaming data.

![Streaming_Broker](images/Streaming_Broker.png)
*Shows the active Kafka brokers handling the streaming data.*

**Kafka Topics :**
    
  Shows the active Kafka topics where events are published.

![Streaming_Topics](images/Streaming_Topics.png)
*Shows the Kafka topics where the real-time events are published.*

## 🔄 Streaming ETL Workflow Diagram
![Streaming_Dags](images/Streaming_Dags.png)

#### Spark ETL Components / Airflow Tasks

1. **Ingestion Stage:**
   - `kafka_producer` → send events into Kafka topics

2. **Transform & Load Stage:**
   - `run_streaming` task → reads Kafka streams using Spark Structured Streaming
   - Performs transformations, filtering, and parsing
   - Writes processed results into Cassandra tables

  
3. **Orchestration:**
   - Airflow DAG schedules and monitors the `run_streaming` task
   - DAG runs every 1 minute (`schedule_interval='*/1 * * * *'`)
   - Limits concurrency and active runs to avoid overlapping tasks

## ✅ Final Output

* The primary **real-time output** of this streaming pipeline is stored in **Cassandra**.  
  Processed data written into Cassandra can be queried directly using **CQL** for analytics or integrated into downstream systems.

* For visualization and exploration, data from Cassandra can be accessed via tools such as:
  - **Jupyter Notebook** (interactive analysis)
  - **Looker Studio** (optional dashboard, currently using exported data for demo purposes)


## 🚀 Setup & Execution

1. Clone this repository :

```bash
git clone https://github.com/supakunz/Streaming-Data-Pipeline.git
```

2. Start the services :
```bash
docker compose up -d
```

3. Start the services :

- Airflow: http://localhost:8080
- Kafka Control Center: http://localhost:9021
- Jupyter: http://localhost:8888
- Cassandra (CQL): `localhost:9042`

## 🙋‍♂️ Contact

Developed by **Supakun Thata**  
📧 Email: supakunt.thata@gmail.com  
🔗 GitHub: [SupakunZ](https://github.com/SupakunZ)

