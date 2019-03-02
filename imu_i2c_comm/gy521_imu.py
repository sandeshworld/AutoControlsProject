from smbus2 import SMBusWrapper #sudo pip install smbus2
import time


class gy521_imu:
	wait_cnt = 0.1 #sec
	
	def __init__(self,i2c_val):
		self.i2c_address = i2c_val
			

	def read(self):
		with SMBusWrapper(1) as bus:
			#configure by sending byte to 0x1C 
			bus.write_byte_data(self.i2c_address,0x1C,0b11101000) #configuring the registers for the accelerometer
			time.sleep(self.wait_cnt)
			while True:
					b = bus.read_byte_data(self.i2c_address,0x3F) #each reading of x is sent in multiple operations
					c = bus.read_byte_data(self.i2c_address,0x40)
					print(b)
					print(c)
					time.sleep(self.wait_cnt)



k = gy521_imu(0x68) #use sudo i2cdetect -y 1 command to find i2c device address
k.read()
