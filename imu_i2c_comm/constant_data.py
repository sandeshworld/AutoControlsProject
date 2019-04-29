import gy521_imu
import time

k = gy521_imu.gy521_imu(0x68)


k.initialize();
k.calibrate();
raw_input("Press Enter. ")

text_file = open("Moving_Around.txt","w")
text_file.write("time (sec), y-accel"+"\n")

print("start")
start = time.time()
end = start + 15

while True:
	try:
		text_file.write(str(time.time()-start)+","+str(k.get_y_accel())+"\n")
	except KeyboardInterrupt:
		break
text_file.close()
k.stop()


