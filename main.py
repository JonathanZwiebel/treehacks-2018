import subprocess
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests
from io import BytesIO


def record(filename):
    record_cmd = "arecord -D plughw:1 --duration=10 -f S16_LE -r16 -vv " + filename
    subprocess.run(record_cmd, shell=True)

def play(filename):
    play_cmd = "aplay " + filename
    subprocess.run(play_cmd, shell=True)

def displayImg():
    
