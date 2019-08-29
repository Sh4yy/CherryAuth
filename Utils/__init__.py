from .OrangeDB import Orange
from peewee import PostgresqlDatabase
from redis import Redis

config = Orange(file_path='config.json', auto_dump=False, load=True)
db = PostgresqlDatabase(
    config['database']['name'],
    user=config['database']['user'],
    host=config['database']['host'],
    port=config['database']['port']
)

redis = Redis(
    host=config['redis']['host'],
    port=config['redis']['port'],
    db=config['redis']['db']
)


