import gy521_imu
import time
import math
k = gy521_imu.gy521_imu(0x68)


k.initialize();
k.calibrate();
print("start")
start = time.time()
while time.time() < start+40:
	y_accel = k.get_y_accel()
	z_accel = k.get_z_accel()
        print("x_gyro: "+str(k.get_x_gyro())+"\n")
	print("y_accel: "+str(y_accel)+" "+str(math.asin(y_accel))+"\n")
	print("z_accel: "+str(z_accel)+" "+str(math.acos(z_accel))+"\n")
	print("difference: "+ str(math.asin(z_accel)-math.acos(y_accel))+"\n")	
	time.sleep(0.5)
k.stop()


