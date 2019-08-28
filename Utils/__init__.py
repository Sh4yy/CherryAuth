from .OrangeDB import Orange
from peewee import PostgresqlDatabase


config = Orange(file_path='config.json', auto_dump=False, load=True)
db = PostgresqlDatabase(
    config['database']['name'],
    user=config['database']['user'],
    host=config['database']['host'],
    port=config['database']['port']
)


