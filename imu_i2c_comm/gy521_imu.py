
#*Written by Sandesh Banskota 2019 for calibrating and reading MPU6050 (GY-521) data*
#*Change registers in initialze for higher sensitivity things but make sure to change to
#to corresponding accelFactor and gyroFactor when you do that*

from smbus2 import SMBus #sudo pip install smbus2
import time
import numpy as np


class gy521_imu:
	wait_cnt = 0.5 #sec
	calibrationSamples = 50
	accelFactor = 16384.0
	gyroFactor = 250.0
	
	def __init__(self,i2c_val):
		self.i2c_address = i2c_val
		self.bus = SMBus(1)
		
		#offset values to be updated during calibration
		self.x_a_offset = 0
		self.y_a_offset = 0
		self.z_a_offset = 0
		
		self.x_g_offset = 0
		self.y_g_offset = 0
		self.z_g_offset = 0
	def stop(self):
		self.bus.close()
		
			
	def initialize(self):
		self.bus.write_byte_data(self.i2c_address,0x6B,0b00000001) #powermanagement register - turning it on using x guro phase lock loop

		time.sleep(self.wait_cnt)

		self.bus.write_byte_data(self.i2c_address,0x1C,0b11100000) #configuring the registers for the accelerometer

		time.sleep(self.wait_cnt)
	
		self.bus.write_byte_data(self.i2c_address,0x1B,0b11100000) #configuring the registers for the gyro
			
		time.sleep(self.wait_cnt)
		
		
	def calibrate(self):
		print("Place the gyroscope down on a flat sheet - this will be your zero position")
		x_accel_raw = 0
		y_accel_raw = 0
		z_accel_raw = 0
		x_gyro_raw = 0
		y_gyro_raw = 0
		z_gyro_raw = 0
		
		#getting multiple data to sum up and get average
		for i in range(self.calibrationSamples):
			z_gyro_raw += self.bus.read_byte_data(self.i2c_address,0x47) << 8 | self.bus.read_byte_data(self.i2c_address,0x48) #each reading of z gyro(16 bits) is sent in multiple operations (2 - 8 bit messages)
				
			x_gyro_raw += self.bus.read_byte_data(self.i2c_address,0x43) << 8 | self.bus.read_byte_data(self.i2c_address,0x44) #each reading of x gyro(16 bits) is sent in multiple operations (2 - 8 bit messages)
				
			y_gyro_raw += self.bus.read_byte_data(self.i2c_address,0x45) << 8 | self.bus.read_byte_data(self.i2c_address,0x46) #each reading of y gyro(16 bits) is sent in multiple operations (2 - 8 bit messages)
				
			z_accel_raw += self.bus.read_byte_data(self.i2c_address,0x3F) << 8 | self.bus.read_byte_data(self.i2c_address,0x40) #each reading of z (16 bits) is sent in multiple operations (2 - 8 bit messages)
				
			x_accel_raw += self.bus.read_byte_data(self.i2c_address,0x3B) << 8 | self.bus.read_byte_data(self.i2c_address,0x3C) #each reading of z is sent in multiple operations
				
			y_accel_raw += self.bus.read_byte_data(self.i2c_address,0x3D) << 8 | self.bus.read_byte_data(self.i2c_address,0x3E) #each reading of y is sent in multiple operations
			
			time.sleep(0.001)
		

		#getting the average to get the offset value for calibration purposes
		self.x_a_offset = x_accel_raw/(self.accelFactor*self.calibrationSamples)
		self.y_a_offset = y_accel_raw/(self.accelFactor*self.calibrationSamples)
		self.z_a_offset = z_accel_raw/(self.accelFactor*self.calibrationSamples)
		
		self.x_g_offset = x_gyro_raw/(self.gyroFactor*self.calibrationSamples)
		self.y_g_offset = y_gyro_raw/(self.gyroFactor*self.calibrationSamples)
		self.z_g_offset = z_gyro_raw/(self.gyroFactor*self.calibrationSamples)
	
	
	
	def get_z_accel(self):
		z_ac_dat = self.bus.read_byte_data(self.i2c_address,0x3F) << 8 | self.bus.read_byte_data(self.i2c_address,0x40) #each reading of z (16 bits) is sent in multiple operations (2 - 8 bit messages)
		z_a = (z_ac_dat)/self.accelFactor - self.z_a_offset + 1 #apparently conversion rate - based on manufacturer spec sheet
		return z_a
		
	def get_z_gyro(self):
		z_gy_dat = self.bus.read_byte_data(self.i2c_address,0x47) << 8 | self.bus.read_byte_data(self.i2c_address,0x48) #each reading of z gyro(16 bits) is sent in multiple operations (2 - 8 bit messages)
		z_g = (z_gy_dat)/self.gyroFactor - self.z_g_offset
		return z_g
		
		
	def get_x_accel(self):
		x_ac_dat = self.bus.read_byte_data(self.i2c_address,0x3B) << 8 | self.bus.read_byte_data(self.i2c_address,0x3C) #each reading of z is sent in multiple operations
		x_a = (x_ac_dat)/self.accelFactor - self.x_a_offset
		return x_a
		
	def get_x_gyro(self):
		x_gy_dat = self.bus.read_byte_data(self.i2c_address,0x43) << 8 | self.bus.read_byte_data(self.i2c_address,0x44) #each reading of x gyro(16 bits) is sent in multiple operations (2 - 8 bit messages)
		x_g = (x_gy_dat)/self.gyroFactor - self.x_g_offset
		return x_g	
	
	def get_y_accel(self):
		y_ac_dat = self.bus.read_byte_data(self.i2c_address,0x3D) << 8 | self.bus.read_byte_data(self.i2c_address,0x3E) #each reading of y is sent in multiple operations
		y_a = (y_ac_dat)/self.accelFactor - self.y_a_offset
		return y_a
		
	def get_y_gyro(self):
		y_gy_dat = self.bus.read_byte_data(self.i2c_address,0x45) << 8 | self.bus.read_byte_data(self.i2c_address,0x46) #each reading of y gyro(16 bits) is sent in multiple operations (2 - 8 bit messages)
		y_g = (y_gy_dat)/self.gyroFactor - self.y_g_offset
		return y_g	
		
	def readAll(self):			
				z_gy_dat = self.bus.read_byte_data(self.i2c_address,0x47) << 8 | self.bus.read_byte_data(self.i2c_address,0x48) #each reading of z gyro(16 bits) is sent in multiple operations (2 - 8 bit messages)
				
				x_gy_dat = self.bus.read_byte_data(self.i2c_address,0x43) << 8 | self.bus.read_byte_data(self.i2c_address,0x44) #each reading of x gyro(16 bits) is sent in multiple operations (2 - 8 bit messages)
				
				y_gy_dat = self.bus.read_byte_data(self.i2c_address,0x45) << 8 | self.bus.read_byte_data(self.i2c_address,0x46) #each reading of y gyro(16 bits) is sent in multiple operations (2 - 8 bit messages)
				
				z_ac_dat = self.bus.read_byte_data(self.i2c_address,0x3F) << 8 | self.bus.read_byte_data(self.i2c_address,0x40) #each reading of z (16 bits) is sent in multiple operations (2 - 8 bit messages)
				
				x_ac_dat = self.bus.read_byte_data(self.i2c_address,0x3B) << 8 | self.bus.read_byte_data(self.i2c_address,0x3C) #each reading of z is sent in multiple operations
				
				y_ac_dat = self.bus.read_byte_data(self.i2c_address,0x3D) << 8 | self.bus.read_byte_data(self.i2c_address,0x3E) #each reading of y is sent in multiple operations
				
				z_accel = (z_ac_dat)/self.accelFactor - self.z_a_offset + 1 #conversion rate - based on spec sheet resource
				
				x_accel = (x_ac_dat)/self.accelFactor - self.x_a_offset
				
				y_accel = (y_ac_dat)/self.accelFactor - self.y_a_offset
				
				z_gyro = (z_gy_dat)/self.gyroFactor - self.z_g_offset
				
				x_gyro = (x_gy_dat)/self.gyroFactor - self.x_g_offset
				
				y_gyro = (y_gy_dat)/self.gyroFactor - self.y_g_offset
				
				print("Reading at " +str(1/self.wait_cnt) + " hz")
				print("x-accel: "+str(x_accel))
				print("")
				print("y-accel: "+str(y_accel))
				print("")
				print("z-accel: "+str(z_accel))
				print("")
				print("---")
				print("x-gyro "+str(x_gyro))
				print("")
				print("y-gyro "+str(y_gyro))
				print("")
				print("z-gyro "+str(z_gyro))
				print("________________________________________")
				time.sleep(self.wait_cnt)
		
	#this method can be used to analyze the mean standard deviation and etc at buffer speed			
	def analyze_data_stat(self,bufferNumber):
		x_a = [];
		x_g = [];
		y_a = [];
		y_g = [];
		z_a = [];
		z_g = [];
		for i in range(bufferNumber):
			x_a.append(self.get_x_accel());
			x_g.append(self.get_x_gyro());
			y_a.append(self.get_y_accel());
			y_g.append(self.get_y_gyro());
			z_a.append(self.get_z_accel());
			z_g.append(self.get_z_gyro());
			time.sleep(0.001)
		
		list_all_data = [x_a,x_g,y_a,y_g,z_a,z_g]
		data_stat = []
		for k in list_all_data:
			a_m = np.mean(np.array(k))
			a_s = np.std(np.array(k))
			data_stat.append(a_m)
			data_stat.append(a_s)
			
		print("x_a - avg = " + str(data_stat[0]) + " std = " + str(data_stat[1]))
		print("x_g - avg = "+str(data_stat[2]) + " std = " + str(data_stat[3]))
		print("y_a - avg = "+str(data_stat[4]) + " std = " + str(data_stat[5]))
		print("y_g - avg = "+str(data_stat[6]) + " std = " + str(data_stat[7]))
		print("z_a - avg = "+str(data_stat[8]) + " std = " + str(data_stat[9]))
		print("z_g - avg = "+str(data_stat[10]) + " std = " + str(data_stat[11]))
		
		
k = gy521_imu(0x68) #use sudo i2cdetect -y 1 command to find i2c device address
k.initialize();
k.calibrate();
print("start")
start = time.time()
end = start+3
text_file = open("trial3.txt","w")
while time.time() < end:
	text_file.write(str(time.time())+","+str(k.get_y_accel())+","+str(k.get_z_accel())+","+str(k.get_y_gyro())+"\n")
text_file.close()
k.stop()
#change code to add more features for only initializing the gyro and accelorme
#ter axis we need to improve efficiency
