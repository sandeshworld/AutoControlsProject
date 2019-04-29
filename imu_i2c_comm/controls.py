#simple PID loop for balancing the motor

import gy521_imu
import time
import Queue #using queues will help with getting moving average
import math

k = gy521_imu.gy521_imu(0x68)

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)

GPIO.output(20,GPIO.HIGH)  #setting the direction pins for the h-bridge to make motor spin the proper way
GPIO.output(21,GPIO.LOW) 

#global pwm17
#global pwm27

pwm17 = GPIO.PWM(17,10000)
pwm27 = GPIO.PWM(27,10000)


k.initialize();
k.calibrate();

global runtime
runtime = 20
global setpoint
setpoint = 0
global m_av_size
m_av_size = 5
upper_pwm = 20
lower_pwm = 20*0.62/0.41

print("Vehicle is Ready to Start")

begin = input("Enter anything to start")


pwm17.start(upper_pwm)
pwm27.start(lower_pwm)

def assignThrust(torque):
	global upper_pwm
	global lower_pwm
	#ideally in the future we want a transfer function here  for conversion
	if torque > 0:
		upper_pwm += torque
		lower_pwm -= torque
	elif torque < 0:
		upper_pwm -= torque
		lower_pwm += torque
	
	upper_pwm = 0 if upper_pwm < 10 else 100 if upper_pwm > 97 else upper_pwm  
	lower_pwm = 0 if lower_pwm < 10 else 100 if lower_pwm > 97 else lower_pwm

def get_average(queue):
	#python does pass by reference so it should work like this as well since i can modify the parameter
	sum = 0
	for i in range(0,m_av_size):
		a = queue.get()
		sum += a
		queue.put(a)
	return sum/m_av_size

prev_error = 0

while True:
	time_stop = time.time()+runtime
	kp = int(input("Enter kp value: "))
	kd = int(input("Enter kd value: "))
	
	q = Queue.Queue()
	print(time.time())
	print(time_stop)
	while time.time() < time_stop:
		print("Here")
		while q.qsize() >= m_av_size:
			#code for filtering - currently a moving average
			p1 = False
			num1 = k.get_y_accel()*math.pi/4 #make 0 to 1 proportional to 0 to pi/4
			if num1 < 1 and num1 > -1:
				q.put(math.asin(num1))
				p1 = True
			theta = get_average(q)
			print(theta)	
			error = setpoint - theta
			Pc = kp*error
			derivative = (error-prev_error)/0.01 #fix the sample time
			Dc = derivative*kd
			control = Pc+Dc
			throttle = control
			assignThrust(throttle)
			if p1:
				q.get()
			prev_error = error
		num2 = k.get_y_accel()*math.pi/4
		if num2 < 1 and num2 > -1:
			q.put(math.asin(num2))
				


pwm17.stop()
pwm27.stop()
k.stop()
GPIO.cleanup()


