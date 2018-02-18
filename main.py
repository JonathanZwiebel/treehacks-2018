import subprocess
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests
from io import BytesIO
from urllib import request
import RPi.GPIO as GPIO
import time


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

    command = "curl -X POST -u " + username + ":" + password + " --header \"Content-Type: application/json\"" +  " --header \"Accept: audio/wav\"" + " --data \"{\\\"text\\\":\\\"" + text + "\\\"}\"" + " --output output.wav " + "\"https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize\""
    subprocess.run(command, shell=True)

def button():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(14, GPIO.IN,pull_up_down=GPIO.PUD_UP)

    count = 1

    sequence = []
    val1 = GPIO.input(18)
    val2 = GPIO.input(14)
    while sequence != [9,1,1]:
    	if len(sequence) == 3:
    		sequence = []

    	val1 = GPIO.input(18)
    	val2 = GPIO.input(14)

    	if not val1:
    		sequence.append(9)
    		print(sequence)
    		val1 = True
    		time.sleep(0.3)
    	elif not val2:
    		sequence.append(1)
    		print(sequence)
    		val2 = True
    		time.sleep(0.3)

def main():
    print('hello world')
    textToSpeech("Hey Iris")

if __name__ == "__main__":
    main()
#displayImg("test.jpg")
