from conn import Database
from config import Config
from time import sleep
from datetime import datetime
import random


class Write:
    def __init__(self):
        config = Config('config.ini')
        self.conn = Database()
        self.id = int(config.get_param('id'))
        self.measurement_time = int(config.get_param('measurement_time'))
        self.insert_time = int(config.get_param('database_insert_time'))

    def transmit_data(self):
        voltage = random.uniform(3.0, 5.0)
        temperature = random.uniform(19.0, 25.0)
        humidity = random.uniform(50, 70)

        if 0 < self.measurement_time <= self.insert_time and self.insert_time > 0:
            n = int(self.insert_time / self.measurement_time)
            i = 0
            sql = 'INSERT INTO data VALUES '

            while True:
                dt = datetime.now()
                now = dt.strftime('%Y-%m-%d %H:%M:%S')

                voltage += random.uniform(-0.01, 0)
                temperature += random.uniform(-0.5, 0.5)
                humidity += random.uniform(-1.0, 1.0)

                sql += f'(NULL, {self.id}, "{now}", {temperature}, {humidity}, {voltage}),'
                print(f"Time: {now}, Voltage: {voltage}, Temperature: {temperature}, Humidity: {humidity}")

                i += 1
                if i >= n:
                    i = 0
                    self.conn.exec(sql.rstrip(','))
                    print('Added data to the database')
                    sql = 'INSERT INTO data VALUES '

                sleep(self.measurement_time)


Write().transmit_data()
