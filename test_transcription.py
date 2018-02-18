# A simple script to test the transcription engine
# Author: Jonathan Zwiebel

import transcription
import sys

st = transcription.SimpleTranscription("name", 16000)
st.initialize()
print(st.transcribe(sys.argv[1], sys.argv[2:]))
