# database.py
import psycopg2


# Подключение к базе данных
def connect_to_database():
    connection = psycopg2.connect(
        database='Kaluga_Signal',
        user='ilyamanzurov01',
        password='0xeELBp3Omqh',
        host='ep-lucky-wood-40926738-pooler.eu-central-1.aws.neon.tech',
        port='5432'
    )
    return connection
