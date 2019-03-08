import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(12,GPIO.OUT)


pwm12 = GPIO.PWM(12,10000)


p = 0

while p < 10:
	k = input("enter duty cycle in percent")
	if k > 80:
		break;
	pwm12.start(k)
	p += 1

pwm12.stop()

GPIO.cleanup()


