from smbus2 import SMBusWrapper #sudo pip install smbus2
import time


class gy521_imu:
	wait_cnt = 0.1 #sec
	
	def __init__(self,i2c_val):
		self.i2c_address = i2c_val
			

	def read(self):
		with SMBusWrapper(1) as bus:
			#configure by sending byte to 0x1C 
			bus.write_byte_data(self.i2c_address,0x6B,0b00101000) #powermanagement register - turning it on
			time.sleep(self.wait_cnt)
			#bus.write_byte_data(self.i2c_address,0x1C,0b11101000) #configuring the registers for the accelerometer
			time.sleep(self.wait_cnt)
			while True:
				z_ac_dat = bus.read_byte_data(self.i2c_address,0x3F) << 8 | bus.read_byte_data(self.i2c_address,0x40) #each reading of z (16 bits) is sent in multiple operations (2 - 8 bit messages)
				x_ac_dat = bus.read_byte_data(self.i2c_address,0x3B) << 8 | bus.read_byte_data(self.i2c_address,0x3C) #each reading of z is sent in multiple operations
				z_accel = (z_ac_dat)/16384.0 #apparently conversion rate - based on online resource
				x_accel = (x_ac_dat)/16384.0 
				print("z-accel: "+str(z_accel))
				print("x-accel: "+str(x_accel))
				
				time.sleep(self.wait_cnt)



k = gy521_imu(0x68) #use sudo i2cdetect -y 1 command to find i2c device address
k.read()
