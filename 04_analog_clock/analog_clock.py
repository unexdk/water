import time
import RPi.GPIO as GPIO

# Constants
PULSE_LEN = 0.03 # length of clock motor pulse
A_PIN = 18       # one motor drive pin
B_PIN = 23       # second motor drive pin
BUTTON_PIN = 24

# Configure the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(A_PIN, GPIO.OUT)
GPIO.setup(B_PIN, GPIO.OUT)

# Glogal variables
positive_polarity = True
period = 1.0          # default tick period of 1 second
last_tick_time = 0    # the time at which last tick occured

def tick():
	# Alternate positive and negative pulses
	global positive_polarity
	if positive_polarity:
		pulse(A_PIN, B_PIN)
	else:
		pulse(B_PIN, A_PIN)
	# Flip the polarity ready for the next tick
	positive_polarity = not positive_polarity
		
def pulse(pos_pin, neg_pin):
	# Turn on the pulse
	GPIO.output(pos_pin, True)
	GPIO.output(neg_pin, False)
	time.sleep(PULSE_LEN)
	# Turn the power off until the next tick
	GPIO.output(pos_pin, False)

try:
	while True:
		t = time.time()
		if t > last_tick_time + period:
			# its time for the next tick
			tick()
			last_tick_time = t
		if GPIO.input(BUTTON_PIN) == False:
			# the button is pressed
			period = 0.2
		else:
			period = 1.0
finally:
    print('Cleaning up GPIO')
    GPIO.cleanup()
