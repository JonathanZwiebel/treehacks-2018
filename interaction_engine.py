# This class provides an engine that decides what should be
# said based on user input and responses from the Houndify API
# The public facing elements of this class are:
# start() which handles initialization of the interface
# interact(filepath) which takes in a filepath and returns a string to be said

import houndify_interface

FREQ = 16000

"""
SCENES
********************
_INIT:
 True
    Output: "911 What is your emergency?"
    Change scene to SCENE_START

SCENE_START:
 Input - Notify operator that there is a fire
    Output: "Are you clear of the fire and out of danger?"
    Change scene to SCENE_DANGER_CHECK
 Input - Panic
    Output: "Calm down and make sure to explain the situation to me so I can help you. What is your emergency?"
 Input failure
    Output: "Make sure to speak slowly and clearly. What is your emergency?"

SCENE_DANGER_CHECK:
 Input - Notify operator that they are in danger
    Output: "Hang up the phone and get away of the fire immediately."
    Chance scene to END
 Input - Notify operator that they are not in danger
    Output: "What is the location of the fire"
    Change scene to LOCATION
 Input failure
    Output: "Make sure to speak slowly and clearly. Are you clear of the fire and out of danger?"

"""

KEY_PHRASES = {"SCENE_START": "What is your emergency?"}

START_TEXT = "Nine One One Operator. What is your emergency?"


class InteractionEngine():
    def __init__(self):
        print("Making client with name device")
        self.houndify = houndify_interface.BasicInteractionClient("device", FREQ)
        self.scene = None
        self.output_text = None
        self.output_ready = None
        self.active_pages = None

    def start(self):
        self.houndify.initialize()
        self.scene = "SCENE_START"
        self.output_ready = True
        self.output_text = START_TEXT
        self.active_pages = ["SCENE_START"]

    def interact(self, filepath):
        self.output_ready = False

        output = self.houndify.api_call(filepath, self.active_pages)
        print(output)
        if output[0]:
            print("Success Domain Case")
            self.output_ready = True
            return output[2]
        else:
            print("Fail Domain Case")
            self.output_ready = True
            return "Please speak clearly so I can understand you. " + KEY_PHRASES[self.scene]
