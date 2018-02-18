# A simple script to test the transcription engine
# Author: Jonathan Zwiebel

import houndify_interface
import sys

st = houndify_interface.BasicInteractionClient("name", 16000)
st.initialize()
print(st.api_call(sys.argv[1], sys.argv[2:]))
