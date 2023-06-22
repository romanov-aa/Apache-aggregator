import re
from datetime import datetime
import mysql.connector
import json


def parse_access_log(log_file):
    pattern = r'(\d+\.\d+\.\d+\.\d+)\s.*?\[(.*?)\].*?"GET\s(.*?)\sHTTP'
    results = []

    with open(log_file, 'r') as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                ip_address = match.group(1)
                date_str = match.group(2)
                url = match.group(3)

                date = datetime.strptime(date_str, '%d/%b/%Y:%H:%M:%S %z')

                results.append((ip_address, date, url))
    
    return results


def save_to_database(data):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='PASSWORD',
        database='db'
    )

    cursor = connection.cursor()

    query_check_duplicate = "SELECT COUNT(*) FROM access_logs WHERE ip_address = %s AND access_date = %s AND url = %s"
    query_insert = "INSERT INTO access_logs (ip_address, access_date, url) VALUES (%s, %s, %s)"

    for ip_address, date, url in data:
        values = (ip_address, date, url)

        cursor.execute(query_check_duplicate, values)
        result = cursor.fetchone()
        if result[0] > 0:
            continue

        cursor.execute(query_insert, values)

    connection.commit()

    cursor.close()
    connection.close()


with open('config.json', 'r') as file:
    config = json.load(file)   
log_path = config['log_path']

parsed_data = parse_access_log(log_path)
save_to_database(parsed_data)
