import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)

GPIO.output(20,GPIO.LOW)
GPIO.output(21,GPIO.LOW)


pwm17 = GPIO.PWM(17,10000)
pwm27 = GPIO.PWM(27,10000)

text = open("official_thrust.txt","w")

p = 0
while p != -1:
	p = input("enter pwm in percent: ")
	#pwm17.start(p)
	if p == -1:
		break
	pwm27.start(p)
	k = input("Thrust Value: ")
	text.write(str(p)+","+str(k)+"\n")
	
text.close()
pwm17.stop()
pwm27.stop()
GPIO.cleanup()


