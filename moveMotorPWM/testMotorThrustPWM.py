import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)

pwm17 = GPIO.PWM(17,10000)
pwm27 = GPIO.PWM(27,10000)

text = open("bottom_motor_data.txt","w")

p = 0
while p != -1:
	p = input("enter pwm in percent: ")
	#pwm17.start(p)
	if p == -1:
		break
	pwm17.start(p)
	k = input("Thrust Value: ")
	text.write(str(p)+","+str(k)+"\n")
	
text.close()
pwm17.stop()
pwm27.stop()
GPIO.cleanup()


