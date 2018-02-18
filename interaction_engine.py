# This class provides an engine that decides what should be
# said based on user input and responses from the Houndify API
# The public facing elements of this class are:
# start() which handles initialization of the interface
# interact(filepath) which takes in a filepath and returns a string to be said

import houndify_interface

FREQ = 16000

KEY_PHRASES = {"SCENE_FIRE_START": "What is your emergency?", "SCENE_WATER_START": "What is your emergency?",
               "SCENE_VIOLENCE_START": "What is your emergency?", "SCENE_INJURY_START": "What is your emergency?", "SCENE_FIRE_CLEAR": "Are you away from the fire?",
               "SCENE_NAME": "What is your name?"}

START_TEXT = "Nine One One Operator. What is your emergency?"


class InteractionEngine():
    def __init__(self):
        print("Making client with name device")
        self.houndify = houndify_interface.BasicInteractionClient("device", FREQ)
        self.scene = None
        self.output_text = None
        self.output_ready = None
        self.active_pages = None

    def load_image(self, image):
        self.image_type = image["type"]
        self.image_tags = image["tags"]

    def start(self):
        self.houndify.initialize()
        self.output_ready = True
        self.output_text = START_TEXT
        print(self.image_type)
        if self.image_type == 1:
            self.active_pages = ["SCENE_FIRE_START"]
            self.scene = "SCENE_FIRE_START"
        if self.image_type == 2:
            self.active_pages = ["SCENE_VIOLENCE_START"]
            self.scene = "SCENE_VIOLENCE_START"
        if self.image_type == 3:
            self.active_pages = ["SCENE_WATER_START"]
            self.scene = "SCENE_WATER_START"
        if self.image_type == 4:
            self.active_pages = ["SCENE_INJURY_START"]
            self.scene = "SCENE_INJURY_START"

    def interact(self, filepath):
        self.output_ready = False

        output = self.houndify.api_call(filepath, self.active_pages)
        print(output)
        if output[0]:
            self.output_ready = True
            if output[3]["identified"]:
                self.scene = output[3]["next_scene"]
                self.active_pages = [output[3]["next_scene"]]
                print(self.next_scene)
            return output[2]
        else:
            self.output_ready = True
            return "Please speak clearly so I can understand you. " + KEY_PHRASES[self.scene]
