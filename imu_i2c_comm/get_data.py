import gy521_imu
import time

k = gy521_imu.gy521_imu(0x68)


k.initialize();
k.calibrate();
print("start")
start = time.time()
end = start+60
#text_file = open("final_right.txt","w")
#text_file.write("time (sec), y-accel"+"\n")
while time.time() < end:
       print(str(time.time()-start)+","+str(k.get_y_accel())+", "+str(k.get_x_gyro())+"\n")
	
#text_file.close()
k.stop()


