import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(14, GPIO.IN,pull_up_down=GPIO.PUD_UP)

count = 1

sequence = []
val1 = GPIO.input(18)
val2 = GPIO.input(14)
while sequence != [9,1,1]:
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
	if len(sequence) == 3:
		sequence = []

"""

while True:
    inputValue = GPIO.input(18)
    while not inputValue:

        if (inputValue == False):
             print("Button pressed ", count, "times")
        time.sleep(0.3)
        count += 1
        inputValue = True


"""
