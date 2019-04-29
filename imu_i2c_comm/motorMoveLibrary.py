import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)

pwm17 = GPIO.PWM(17,10000)
pwm27 = GPIO.PWM(27,10000)

p = 0
j = 0
k = 50
while j < 10:
	p = input("enter perturbation in percent")
	if k+p > 100:
		break;
	pwm17.start(k-p)
	pwm27.start(k+p)
	j += 1

pwm17.stop()
pwm27.stop()
GPIO.cleanup()


