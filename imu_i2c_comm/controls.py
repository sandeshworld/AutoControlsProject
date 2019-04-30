#simple PID loop for balancing the motor

import gy521_imu
import time
import Queue #using queues will help with getting moving average
import math

f = open("data.txt","w+")

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
runtime = 60
global setpoint
setpoint = 0
global m_av_size
m_av_size = 10
upper_pwm = 20
lower_pwm = int(20*0.62/0.41)

print("Vehicle is Ready to Start")

begin = input("Enter anything to start")


pwm27.start(upper_pwm)
pwm17.start(lower_pwm)

def assignThrust(torque):
	global upper_pwm
	global lower_pwm
	#ideally in the future we want a transfer function here  for conversion
	
	upper_pwm+=torque/0.62
	lower_pwm-=torque/0.41
	
	upper_pwm = 1 if upper_pwm < 1 else 98.0 if upper_pwm > 98 else upper_pwm  #it was getting stuck  in here smh 
	lower_pwm = 1 if lower_pwm < 1 else 98.0 if lower_pwm > 98 else lower_pwm
	
	pwm27.start(upper_pwm)
	pwm17.start(lower_pwm)

	f.write("upper_pwm: " + str(upper_pwm)+"\n")
	f.write("lower_pwm: " + str(lower_pwm)+"\n")

"""{


def get_average(queue):
	#python does pass by reference so it should work like this as well since i can modify the parameter
	sum = 0
	
	for i in range(0,m_av_size):
		a = queue.get()
		sum += a
		print("inside" + str(a))
		queue.put(a)
	return sum/m_av_size
"""

prev_error = 0

while True:
	time_stop = time.time()+runtime
	kp = float(input("Enter kp value: "))
	kd = float(input("Enter kd value: "))
	
	f.write("kp: " + str(kp) + " kd: " + str(kd) + "\n")
	q = Queue.Queue()
	print(time.time())
	print(time_stop)
	while time.time() < time_stop:
		print("Here")
		while q.qsize() >= m_av_size:
			#code for filtering - currently a moving average
			p1 = False
			num1 = k.get_y_accel() #make 0 to 1 proportional to 0 to pi/4
			if num1 < 1 and num1 > -1:
				k12 = math.asin(num1*math.pi/4)
				q.put(k12)
				p1 = True
				q.get()
				#print("inside if statement: " + str(q.get()))
				q.put(k12)
			sum = 0
			
			for i in range(0,m_av_size):
				a = q.get()
				sum += a
				#print(str(a) + ", ")
				q.put(a)

			#print("sum: " + str(sum))
			theta = sum/m_av_size 
			f.write("Theta: " + str(theta) + "\n")
			error = setpoint - theta
			Pc = kp*error
			f.write("Pc: "+ str(Pc)+"\n")
			derivative = (error-prev_error)/0.01 #fix the sample time
			Dc = derivative*kd
			f.write("Dc: "+str(Dc)+"\n")
			control = Pc+Dc
			throttle = control
			f.write("Control: " + str(throttle)+"\n")
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


