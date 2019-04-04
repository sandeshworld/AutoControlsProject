import time


listzero = [0]*500
listone = [1]*2000

input_list = listzero+listone

start = time.time()

yk1 = 0
yk2 = 0
uk1 = 0
uk2 = 0

output_list = []

for y in input_list:
	uk = 0.21*y+0.41*yk1+0.21*yk2+0.37*uk1+0.2*uk2
	yk2 = yk1
	yk1 = y
	uk2 = uk1
	uk1 = uk
	output_list.append([time.time()-start,y,uk])

file_data = open("bandwidth_test.txt","w")
for k in output_list:
	file_data.write(','.join(map(str,k))+"\n")

file_data.close()


	


