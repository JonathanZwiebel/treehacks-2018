import subprocess
from pymongo import MongoClient
from urllib import request
import interaction_engine
import time
import random
import RPi.GPIO as GPIO


def record(filename):
    record_cmd = "arecord -D plughw:1 --duration=10 -f S16_LE -r16 -vv " + filename
    subprocess.run(record_cmd, shell=True)


def play(filename):
    play_cmd = "aplay " + filename
    subprocess.run(play_cmd, shell=True)


def find_random_comic(comic_image_list):
    index = random.randint(0, len(comic_image_list))
    return comic_image_list[index]


def displayImg(filename):
    MONGOLAB_URI = "mongodb://treehax:Soyboy100!@ds225028.mlab.com:25028/comic-images"
    client = MongoClient(MONGOLAB_URI)
    db = client.get_default_database()
    comic_images = db['comic-images']
    image_list = list(comic_images.find())
    # print(image_list)

    # Creates file called 'filename'
    f = open(filename, 'wb')
    random_img = find_random_comic(image_list)
    f.write(request.urlopen(random_img['url'].format("Raspberry Pi")).read())
    f.close()

    subprocess.run("sudo fbi -d /dev/fb0 -a -T 1 " + filename, shell=True)
    return random_img


def textToSpeech(text):
    username = '5cc5826f-36d2-480e-854f-00897a72e4ac'
    password = 'lMrLyiF0o1bW'

    command = "curl -X POST -u " + username + ":" + password + " --header \"Content-Type: application/json\"" + " --header \"Accept: audio/wav\"" + " --data \"{\\\"text\\\":\\\"" + text + "\\\"}\"" + " --output output.wav " + "\"https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize\""
    subprocess.run(command, shell=True)


def button():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    sequence = []
    val1 = GPIO.input(18)
    val2 = GPIO.input(14)
    while sequence != [9, 1, 1]:
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
    engine = interaction_engine.InteractionEngine()
    status = "LOAD_IMAGE"
    last_result = "Nine One One Operator. What is your emergency?"

    toHeadphones = "amixer cset numid=3 1"
    subprocess.run(toHeadphones, shell=True)

    while True:
        print(status)

        if status == "LOAD_IMAGE":
            image = displayImg("image.jpeg")
            engine.load_image(image)
            engine.start()
            status = "LISTEN_START"
        if status == "LISTEN_START":
            listen_begin_time = time.time()
            record("recording.wav")
            status = "LISTEN_ACTIVE"
        elif status == "LISTEN_ACTIVE":
            if time.time() - listen_begin_time > 10:
                status = "HOUND"
        elif status == "HOUND":
            last_result = engine.interact("recording.wav")
            status = "TTS_START"
        elif status == "TTS_START":
            tts_begin_time = time.time()
            textToSpeech(last_result)
            status = "TTS_ACTIVE"
        elif status == "TTS_ACTIVE":
            if time.time() - tts_begin_time > 6:
                status = "PLAY_START"
        elif status == "PLAY_START":
            play_begin_time = time.time()
            play("output.wav")
            status = "PLAY_ACTIVE"
        elif status == "PLAY_ACTIVE":
            if time.time() - play_begin_time > 6:
                status = "LISTEN_START"

        time.sleep(0.1)


main()
