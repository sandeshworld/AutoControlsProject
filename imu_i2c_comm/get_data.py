import gy521_imu
import time

k = gy521_imu.gy521_imu(0x68)


k.initialize();
k.calibrate();
print("start")
start = time.time()
end = start+3
text_file = open("free_fall_data_trial3.txt","w")
text_file.write("time (sec), y-accel"+"\n")
while time.time() < end:
       text_file.write(str(time.time()-start)+","+str(k.get_y_accel())+"\n")
	
text_file.close()
k.stop()


