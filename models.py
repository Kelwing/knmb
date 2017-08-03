from peewee import *
import pymysql
import datetime
from playhouse.shortcuts import RetryOperationalError

db = SqliteDatabase('musicbot.db')

class Song(Model):
    title = CharField(max_length=100, null=True)
    url = CharField(max_length=100, null=False)
    length = IntegerField(null=True)
    plays = IntegerField(default=0)

class Playlist(Model):
    name = CharField()

class Mapping(Model):
    song = ForeignKeyField(Song)
    playlist = ForeignKeyField(Playlist)

class Operator(Model):
    user_id = BigIntegerField(null=False)

class Server(Model):
    server_id = BigIntegerField(null=False)
    music_channel = BigIntegerField(null=True)
    chat_channel = BigIntegerField(null=True)
    autojoin = BooleanField(null=False, default=False)
