
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)


#turning on 20 and 21 cause they are direction pins and will make motor move
#correct way
GPIO.output(20,GPIO.HIGH)
GPIO.output(21,GPIO.HIGH)


pwm17 = GPIO.PWM(17,10000)
pwm27 = GPIO.PWM(27,10000)


import gy521_imu
import time

k = gy521_imu.gy521_imu(0x68)


k.initialize();
k.calibrate();

print("move the vehicle to a tilt now")
raw_input("Press Enter. ")
text_file = open("constant_data_with_motors.txt","w")
start = time.time()
count = 0
while True:
	try:
        	p = time.time()
        	text_file.write(str(p-start)+", "+str(count)+", "+str(k.get_y_accel())+"\n")
		if p > start+2:
			pwm17.start(90)
		time.sleep(0.003)
		count+=0.003
	except KeyboardInterrupt:
		break
pwm17.stop()
pwm27.stop()
GPIO.cleanup()
text_file.close()
k.stop()
