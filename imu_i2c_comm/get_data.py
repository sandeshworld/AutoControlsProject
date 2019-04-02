import gy521_imu
import time

k = gy521_imu.gy521_imu(0x68)


k.initialize();
k.calibrate();
print("start")
start = time.time()
end = start+3
text_file = open("trialF.txt","w")
while time.time() < end:
       text_file.write(str(time.time()-start)+","+str(k.get_y_accel())+","+str(k.get_z_accel())+","+str(k.get_y_gyro())+"\n")
	
text_file.close()
k.stop()


