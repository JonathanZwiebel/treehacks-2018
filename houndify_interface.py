#!/usr/bin/env python3

# Author: Jonathan Zwiebel
# Version: 17 Feb 2018
# A class that wraps methods to get a transcription of an .wav file
import houndify.houndify as hound
import wave
import time

ID_KEY_FILE = "keys.txt"
BUFFER_SIZE = 512
LEGAL_SAMPLE_WIDTHS = [2]
LEGAL_N_CHANNELS = [1]


def verify_audio(audio, freq):
    if audio.getframerate() != freq:
        print("Setup error: unsupported sampling frequency | expected %s | got %s" % (freq, audio.getframerate()))
        return False
    if audio.getsampwidth() not in LEGAL_SAMPLE_WIDTHS:
        print("Setup error: wrong sample width | expected %s | got %s" % (LEGAL_SAMPLE_WIDTHS, audio.getsampwidth()))
        return False
    if audio.getnchannels() not in LEGAL_N_CHANNELS:
        print("Setup error: must be single channel | expected %s | got %s" % (LEGAL_N_CHANNELS, audio.getnchannels()))
        return False
    return True


class BasicInteractionListener(hound.HoundListener):
    def initialize(self):
        self.internal_status = "Not Started"

    def onPartialTranscript(self, transcript):
        self.internal_status = "In Progress"
        pass

    def onFinalResponse(self, response):
        self.internal_status = "Complete"

    def onError(self, err):
        self.internal_status = "Failed"
        self.error_message = str(err)


class BasicInteractionClient():
    def __init__(self, id, freq):
        self.id = id
        self.status = "Idle"
        self.freq = freq
        self.client = None

    def initialize(self):
        self.status = "Client Setup"
        _CLIENT_ID = ""
        _CLIENT_KEY = ""

        with open(ID_KEY_FILE, "r") as key_file:
            content = key_file.read().splitlines()
            _CLIENT_ID = content[0]
            _CLIENT_KEY = content[1]

        self.client = hound.StreamingHoundClient(_CLIENT_ID, _CLIENT_KEY, "test")

        try:
            self.client.setSampleRate(self.freq)
            self.listener = BasicInteractionListener()
            self.listener.initialize()
        except:
            self.status = "Failed In Client Setup"
            return
        self.status = "Idle"

    def transcribe(self, file_location, pages_to_match):
        transcription_start_time = time.time()
        self.status = "Page Matching Setup"
        self.client.setHoundRequestInfo("StoredGlobalPagesToMatch", pages_to_match)
        self.client.start(self.listener)

        self.status = "Audio Setup"

        _AUDIO_FILE = file_location

        audio = wave.open(_AUDIO_FILE)
        if not verify_audio(audio, self.freq):
            self.status = "Failed In Audio Setup"
            return

        self.status = "Transcribe"

        while True:
            samples = audio.readframes(BUFFER_SIZE)
            if len(samples) == 0:
                break
            if self.client.fill(samples):
                break

        result = self.client.finish()

        transcription = result["Disambiguation"]["ChoiceData"][0]["Transcription"]

        transcription_end_time = time.time()
        transcription_duration = transcription_end_time - transcription_start_time
        self.status = "Idle"

        if len(result["DomainUsage"]) == 0:
            return False, transcription, transcription_duration
        else:
            spoken_response = result["AllResults"][0]["SpokenResponse"]
            results = result["AllResults"][0]["Result"]
        return True, transcription, spoken_response, results, transcription_duration
