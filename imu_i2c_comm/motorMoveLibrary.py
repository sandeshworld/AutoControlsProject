import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)

pwm17 = GPIO.PWM(17,10000)
pwm27 = GPIO.PWM(27,10000)


import gy521_imu
import time

k = gy521_imu.gy521_imu(0x68)


k.initialize();
k.calibrate();
print("start")
start = time.time()
end = start+6
text_file = open("trial_step_bottom.txt","w")
zq = 0
while time.time() < end:
        p = time.time()
        text_file.write(str(p-start)+","+str(k.get_y_accel())+","+str(k.get_z_accel()))
	if p > start+2 and zq == 0:
		pwm17.start(100)
		#pwm27.start(50)
		zq = 1



pwm17.stop()
#pwm27.stop()
GPIO.cleanup()
	
text_file.close()
k.stop()
