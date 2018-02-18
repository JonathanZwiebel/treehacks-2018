#!/usr/bin/env python3
import houndify.houndify as hound
import sys
import wave

ID_KEY_FILE = "keys.txt"
BUFFER_SIZE = 128
LEGAL_SAMPLE_WIDTHS = [2]
LEGAL_SAMPLE_FREQS = [8000, 16000]
LEGAL_N_CHANNELS = [1]


# Builds a basic listener to print out the transcript as it comes from the API


class MyListener(hound.HoundListener):
    def onPartialTranscript(self, transcript):
        # print("Partial transcript: " + transcript)
        pass

    def onFinalResponse(self, response):
        # print("Final response: " + str(response))
        pass

    def onError(self, err):
        print("Error: " + str(err))

# Author: Jonathan Zwiebel
# Version: 17 Feb 2018
# A sample file to convert a .wav file into text using the Houndify API


_AUDIO_FILE = sys.argv[1]
_CLIENT_ID = ""
_CLIENT_KEY = ""

print("Start")

with open(ID_KEY_FILE, "r") as key_file:
    content = key_file.read().splitlines()
    _CLIENT_ID = content[0]
    _CLIENT_KEY = content[1]

print("File opened")

client = hound.StreamingHoundClient(_CLIENT_ID, _CLIENT_KEY, "test")

print("Client established")

audio = wave.open(_AUDIO_FILE)
if audio.getsampwidth() not in LEGAL_SAMPLE_WIDTHS:
    print("wrong sample width | expected %s | got %s" % (LEGAL_SAMPLE_WIDTHS, audio.getsampwidth()))
if audio.getframerate() not in LEGAL_SAMPLE_FREQS:
    print("unsupported sampling frequency | expected %s | got %s" % (LEGAL_SAMPLE_FREQS, audio.getframerate()))
if audio.getnchannels() not in LEGAL_N_CHANNELS:
    print("must be single channel | expected %s | got %s" % (LEGAL_N_CHANNELS, audio.getnchannels()))

print("Audio file read")

client.setSampleRate(audio.getframerate())
client.start(MyListener())

while True:
    samples = audio.readframes(BUFFER_SIZE)
    if len(samples) == 0:
        break
    if client.fill(samples):
        break
    # no sleep

result = client.finish()
print("################################################################3")
print("Transcription: " + result["Disambiguation"]["ChoiceData"][0]["Transcription"])
print("Confidence: " + str(result["Disambiguation"]["ChoiceData"][0]["ConfidenceScore"]))
print("################################################################3")

for key in result:
    print(key + ": " + str(result[key]))
