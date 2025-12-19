# Streaming Data Pipeline (Airflow · Spark · Kafka · Cassandra · Jupyter)

This project sets up a **streaming** data pipeline using Docker Compose to orchestrate Apache Airflow, Apache Spark, Kafka, Cassandra, and Jupyter Notebook for real‑time data ingestion, processing, storage, and visualization.

## Overview

- Airflow orchestrates and schedules the Spark streaming DAG `spark_streaming_dag`.
- Kafka ingests streaming events that Spark reads, processes, and writes into Cassandra tables.
- Cassandra stores the processed data in the `spark_streams` keyspace.
- Jupyter connects to Cassandra to explore and visualize the data with pandas.

## Service URLs

After the stack is running, the main web UIs are available at:

- **Airflow Web UI**: `http://localhost:8080/` (username: admin Password: admin)
- **Kafka Control Center**: `http://localhost:9021/`
- **Jupyter Notebook**: `http://localhost:8888/`

---

## 1. Prerequisites

- Docker Desktop (includes Docker Engine and Docker Compose)
- Git (optional, for cloning the repository)
- Web browser (Chrome, Firefox, Edge, etc.)

Verify your installation:
```
docker --version
docker compose version
```
---

## 2. Get the Project

Clone the repository:
```
git clone https://github.com/IPingus/ICS474-project1
```
Or download the repository as a ZIP from GitHub, extract it, and open a terminal inside the project folder.

---

## 3. Start Docker Desktop

1. Open Docker Desktop.
2. Wait until Docker reports that it is running and healthy before continuing.

---

## 4. Start All Services with Docker Compose

From the project root (where `docker-compose.yml` is located), run:
```
docker compose up -d
```
This command builds and starts all containers (Airflow, Spark, Kafka, Cassandra, Jupyter, etc.) in detached mode.

<img width="1078" height="442" alt="image" src="https://github.com/user-attachments/assets/01b926f7-92a0-4d2f-b024-84bbdf7b5519" />




Check container status:
```
docker compose ps
```
All services should be in `Running` or `Healthy` state.

---

## 5. Enable the Airflow DAG

1. Open the Airflow Web UI:

   http://localhost:8080/

2. Log in using the credentials configured in `docker-compose.yml` (should be `admin` / `admin`).
3. In the DAG list, locate `spark_streaming_dag`.
4. Click the toggle to **unpause** the DAG so that it starts scheduling and running.
<img width="2492" height="1279" alt="image" src="https://github.com/user-attachments/assets/e329a5da-9003-4529-806e-8aa0704711b0" />

---

## 6. Inspect Cassandra Keyspaces

Open a CQL shell inside the Cassandra container:
```
docker exec -it cassandra cqlsh
```
List all keyspaces:
```
DESCRIBE keyspaces;
```
Identify the keyspace named `spark_streams`, which contains the tables created by the streaming pipeline.

---

## 7. Verify Data in `created_users`

Still inside `cqlsh`, switch to the `spark_streams` keyspace and query the data:
```
USE spark_streams;
SELECT * FROM created_users LIMIT 10;
```
You should see sample rows with columns such as `id`, `username`, `email`, `address`, and more, confirming that the pipeline is writing data into Cassandra.
<img width="2530" height="725" alt="image" src="https://github.com/user-attachments/assets/ce62f90e-47da-4b9c-87d3-406ce119fe77" />


---

## 8. Jupyter Integration and Data Visualization

### 8.1 Open Jupyter

In your browser, open:

http://localhost:8888/

Use the token or password printed in the Jupyter container logs if prompted.

### 8.2 Install `pandas` in the Notebook

If you see `ModuleNotFoundError: No module named 'pandas'`, install pandas directly from a notebook cell:
```
%pip install pandas
#or
!pip install pandas
```
These commands install pandas into the same Python environment used by the notebook kernel.

After installation:

1. Restart the kernel (menu: **Kernel → Restart**).
2. Import pandas:

from pandas import DataFrame

### 8.3 Connect to Cassandra from Jupyter

Create a new notebook and run:
```
from cassandra.cluster import Cluster
from pandas import DataFrame
```
# Connect to Cassandra (service name from docker-compose)
```
cluster = Cluster(["cassandra"])
session = cluster.connect("spark_streams")

rows = session.execute("SELECT * FROM created_users LIMIT 100;")
df = DataFrame(list(rows))
df.head()
```
This loads records from `created_users` into a pandas DataFrame for analysis.

You can then visualize the data, for example:
```
import matplotlib.pyplot as plt

df["registered_date"].value_counts().sort_index().plot(kind="bar", figsize=(12, 4))
plt.title("Registrations over time")
plt.xlabel("Date")
plt.ylabel("Count")
plt.show()
```
---

## 9. Kafka Control Center

Kafka Control Center provides visibility into Kafka clusters, topics, and consumer groups.

Open:

http://localhost:9021/

Use the UI to:

- Monitor Kafka brokers and topics.
- Inspect topic messages used by the streaming pipeline.
<img width="2508" height="1268" alt="image" src="https://github.com/user-attachments/assets/6a757771-56df-4a37-b71c-d1951909d500" />

---

## 10. Stop and Clean Up

To stop all containers (without deleting volumes):
```
docker compose down
```
To stop and remove containers, networks, and volumes (including stored data):
```
docker compose down -v
```
Use these commands when you want to shut down or completely reset the pipeline environment.
