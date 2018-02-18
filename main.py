import subprocess
from pymongo import MongoClient
from urllib import request
import interaction_engine
import time


def main():
    engine = interaction_engine.InteractionEngine()
    engine.start()
    status = "TTS_START"
    last_result = "Nine One One Operator. What is your emergency?"

    while True:
        print(status)

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
            if time.time() - tts_begin_time > 1:
                status = "PLAY_START"
        elif status == "PLAY_START":
            play_begin_time = time.time()
            play("output.wav")
            status = "PLAY_ACTIVE"
        elif status == "PLAY_ACTIVE":
            if time.time() - play_begin_time > 6:
                status = "LISTEN_START"

        time.sleep(0.1)


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

    command = "curl -X POST -u " + username + ":" + password + " --header \"Content-Type: application/json\"" + " --header \"Accept: audio/wav\"" + " --data \"{\\\"text\\\":\\\"" + text + "\\\"}\"" + " --output output.wav " + "\"https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize\""
    subprocess.run(command, shell=True)


# displayImg("test.jpg")
