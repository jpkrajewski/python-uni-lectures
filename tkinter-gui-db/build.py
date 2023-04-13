from conn import Database
from config import Config

config = Config('config.ini')
conn = Database()
conn.db = None
DBNAME = config.get_param('database')
MEASUREMENT_TIME = config.get_param('measurement_time')
INSERT_TIME = config.get_param('database_insert_time')
DEVICE_ID = config.get_param('id')

conn.exec(f'DROP DATABASE IF EXISTS {DBNAME}')
conn.exec(f'CREATE DATABASE {DBNAME}')
conn.db = config.get_param('database')

conn.exec("""
CREATE TABLE `devices` (
    id INT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    uid CHAR(24) NOT NULL,
    name VARCHAR(255),
    measurement_interval INT UNSIGNED NOT NULL DEFAULT 5,
    transceive_interval INT UNSIGNED NOT NULL DEFAULT 60,
    PRIMARY KEY(id)
);
""")

conn.exec("""
CREATE TABLE `data` (
    id INT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    device_id INT UNSIGNED NOT NULL,
    time DATETIME NOT NULL,
    temperature FLOAT,
    humidity FLOAT,
    voltage FLOAT,
    PRIMARY KEY (id),
    FOREIGN KEY (device_id) REFERENCES devices(id),
    INDEX device_time (device_id, time)
);
""")

conn.exec(f"""
INSERT INTO devices
VALUES (
    {DEVICE_ID},
    "000000000000000000000000",
    "Test device",
    {MEASUREMENT_TIME},
    {INSERT_TIME}
);
""")

print("Database and tables successfully created.")
