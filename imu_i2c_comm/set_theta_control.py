#simple PID loop for balancing the motor

import gy521_imu
import time
import Queue #using queues will help with getting moving average
import math

#f = open("data00.txt","w+")

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
m_av_size = 40
upper_pwm = 20
lower_pwm = int(20*0.62/0.41)

global stop_program
stop_program = False

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

	upper_pwm = 1 if upper_pwm < 1 else 99.0 if upper_pwm > 99 else upper_pwm  #it was getting stuck  in here smh
	lower_pwm = 1 if lower_pwm < 1 else 99.0 if lower_pwm > 99 else lower_pwm

	pwm27.start(upper_pwm)
	pwm17.start(lower_pwm)
#	print("u: "+str(upper_pwm))
#	print("l: "+str(lower_pwm))

	#f.write("upper_pwm: " + str(upper_pwm)+"\n")
	#f.write("lower_pwm: " + str(lower_pwm)+"\n")

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



def control():
	prev_error = 0
	ranum = 1
	while True:
		time_stop = time.time()+runtime
		#kp = float(input("Enter kp value: "))
		#kd = float(input("Enter kd value: "))

		kp = float(1000)
		kd = float(2200)


		#f.write("kp: " + str(kp) + " kd: " + str(kd) + "\n")
		q = Queue.Queue()
		print(time.time())
		print(time_stop)
		while time.time() < time_stop:
			print("Here")
			#prev_time = time.time()
			while q.qsize() >= m_av_size:
				#code for filtering - currently a moving average
				p1 = False
				num1 = k.get_y_accel() #make 0 to 1 proportional to 0 to pi/4


				#print(time.time())
				if num1 < 1 and num1 > -1:
					k12 = math.asin(num1*math.pi/4 ) + 0.025
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
				if (ranum % 100) == 1:
					print("theta: " + str(theta) + "\n")
				#theta = k12
				#f.write("Theta: " + str(theta) + "\n")
				#error = setpoint - theta
				ranum += 1
				error = setpoint - theta

				Pc = kp*error
				#f.write("Pc: "+ str(Pc)+"\n")
				gyrox = -1*k.get_x_gyro()*2*3.1415926535/360
				derivative =  gyrox #fix the sample time
				Dc = derivative*kd
				#f.write("Dc: "+str(Dc)+"\n")
				control = Pc+Dc
				throttle = control
				#f.write("Control: " + str(throttle)+"\n")
				assignThrust(throttle)
				#f.write("Time: " + str(time.time())+"\n")
				if p1:
					q.get()
				prev_error = error
				#prev_time = time.time()

			num2 = k.get_y_accel()*math.pi/4
			if num2 < 1 and num2 > -1:
				q.put(math.asin(num2)+0.025)

	stop_program = True
	pwm17.stop()
	pwm27.stop()
	k.stop()
	GPIO.cleanup()

def user_input():

	while not stop_program:
		ok = 0
		while ok == 0:
			try:
				theta_input = int(input("Enter a setpoint theta value: "))
				ok = 1
			except:
				print("Please enter an integer between -3 and 3")
				ok == 0
		setpoint = theta_input

def main_task():

    # creating threads
    t1 = threading.Thread(target=control)
    t2 = threading.Thread(target=user_input)

    # start threads
    t1.start()
    t2.start()

    # wait until threads finish their job
    t1.join()
    t2.join()


if name == "__main__":
	main_task()
	
