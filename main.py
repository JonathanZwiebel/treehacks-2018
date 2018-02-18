import subprocess
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests
from io import BytesIO
from urllib import request

def main():
    print('hello world')

if __name__ == "__main__":
    main()


def record(filename):
    record_cmd = "arecord -D plughw:1 --duration=10 -f S16_LE -r16 -vv " + filename
    subprocess.run(record_cmd, shell=True)

def play(filename):
    play_cmd = "aplay " + filename
    subprocess.run(play_cmd, shell=True)

def displayImg(filename):
    MONGOLAB_URI = "mongodb://treehax:Soyboy100!@ds225028.mlab.com:25028/comic-images"
    client = MongoClient(MONGOLAB_URI)
    db = client.get_default_database()
    comic_images = db['comic-images']
    image_list = comic_images.find()

    # Creates file called 'filename'
    f = open(filename, 'wb')
    f.write(request.urlopen(image_list[0]['url'].format("Raspberry Pi")).read())
    f.close()

    subprocess.run("sudo fbi -d /dev/fb0 -a -T 1 " + filename, shell=True)

def textToSpeech(text):
    url = 'https://stream.watsonplatform.net/text-to-speech/api'
    username = '5cc5826f-36d2-480e-854f-00897a72e4ac'
    password = 'lMrLyiF0o1bW'

    command = "curl -X POST -u " + username + ":" + password + " --header \"Content-Type: application/json\"" +  " --header \"Accept: audio/wav\"" + " --data \"{\\\"text\\\":\\\"" + text + "\\\"}\"" + " --output hello_world.wav " + "\"https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize\""
    subprocess.run(command, shell=True)


#displayImg("test.jpg")
