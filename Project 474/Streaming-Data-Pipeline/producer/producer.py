import uuid
import json
import logging
import time
import requests
from kafka import KafkaProducer

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_data():
    res = requests.get("https://randomuser.me/api/")
    res.raise_for_status()
    return res.json()['results'][0]

def format_data(res):
    location = res['location']
    return {
        'id': str(uuid.uuid4()),
        'first_name': res['name']['first'],
        'last_name': res['name']['last'],
        'gender': res['gender'],
        'address': f"{location['street']['number']} {location['street']['name']}, {location['city']}, {location['state']}, {location['country']}",
        'post_code': location['postcode'],
        'email': res['email'],
        'username': res['login']['username'],
        'dob': res['dob']['date'],
        'registered_date': res['registered']['date'],
        'phone': res['phone'],
        'picture': res['picture']['medium']
    }

def stream_data():
    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
    while True:
        try:
            res = get_data()
            res = format_data(res)
            print(res)
            producer.send('users_created', json.dumps(res).encode('utf-8'))
            time.sleep(1)  # ยิงทุก 1 วิ ปรับได้ตามต้องการ
        except Exception as e:
            logging.error(f'An error occurred: {e}')
            continue

if __name__ == "__main__":
    stream_data()
