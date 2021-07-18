from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # создаем объект client класса MongoClient
db = client['pymongo_test']  # запускаем mongod.exe и работаем с БД 'pymongo_test'
collection = db['docs']  # работаем с коллекцией 'docs'
user_coll = db['users']  # с авторизацией работаем с коллекцией 'users'

app.config.from_pyfile('config.cfg')

