import re
import json
import math
import os
from pathlib import Path
import shutil
import time, glob

# function to convert a number value in a boolean sequence

def bin_convert(x,a0,a1,n):
	Xn = (x-a0)/(a1-a0)
	Xm = pow(2,n)*Xn
	ix = math.floor(Xm)
	x = bin(ix)
	x = '{:0b}'.format(ix)
	m=len(x)
	while m != n:
		x = "0" + x
		m=m+1
	bool_result=[]	
	for t in range(n):
		if x[t] == '1':
			x_c = True
			bool_result.append(x_c)
		elif x[t] == '0':
			x_c = False
			bool_result.append(x_c)
	return bool_result

try:

# n-upla parameters:
# x0,x1,x2 => battery level
# x3,x4,x5,x6 => x position
# x7,x8,x9,x10 => y position
# x11 => grasp

# parameters related to the resolution map:
# -(a0,a1) x-axis extremes
# -(b0,b1) y-axis extremes
# - n bit number

	
# initialise some variables
	n = 4
	fail = 0
	reached = 0
	trace = []
	init_bat_found = False
	init_pos_found = False
	init_gra_found = False
	count=0
	count_=0
	check_pose=0
	dist=0
	n_f = 0
	n_s = 0

# keywords to find the lines we are looking for in the log file
	key1 = "Command   : level"
	key2 = "getCurrentPose"
	key3 = "Command   : hasGrasped"
	key4 = "Command   : getPoseOf"
	key5 = " Arguments : kitchen"

	dirpath = os.getcwd()
	path = dirpath+'/json_trace_folder'


	print("This script allows you to convert log_file to a boolean trace")
	print("by entering:")
	print("1 - you can choose a log_file in the current folder and convert it to a json trace")
	print("2 - you can convert a folder containing log_files to a folder containing json traces")
	print("3 - you can convert a folder containing json traces to a single sample containing all converted positive and negative traces")
	val = input("insert command: ")

############################################## trace generation #########################################################################################################

# set the file to analyze
	if val == "1":
		print("Enter the coordinates of the extremes of the simulation map:")
		a0 = float(input("x0: " ))
		a1 = float(input("x1: " ))
		b0 = float(input("y0: " ))
		b1 = float(input("y1: " ))
		file_name = input("insert the name of log_file (example: log1.txt): ")
		while count < 3:
			with open(file_name) as file_iterator:
				for line in file_iterator:

					if key1 in line and init_bat_found != True:
						nex = next(file_iterator)
						nex_1 = next(file_iterator)
						bat_level = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
						if bat_level != []:
	 						#print('\n- start_battery_state -')
	 						bat_level= bat_level[0]
	 						min_bat = 0
	 						max_bat = 101
	 						n_bit = 3 
	 						x0_x1_x2 = bin_convert(bat_level, min_bat, max_bat, n_bit)
	 						#print(x0_x1_x2)
	 						init_bat_found = True
	 						count=count+1

					if key2 in line and init_pos_found != True:
	 					nex = next(file_iterator)
	 					nex_1 = next(file_iterator)
	 					rob_pose = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
	 					

	 					if rob_pose != []:
	 						x_pose = rob_pose[0]
	 						y_pose = rob_pose[1]
	 						

	 						x_bin = bin_convert(x_pose, a0, a1, n)
	 						y_bin = bin_convert(y_pose, b0, b1, n)
	 						x3_x4_x5_x6_x7_x8_x9_x10 = x_bin + y_bin

	 						#print('\n- start_position_state: -')
	 						#print(x3_x4_x5_x6_x7_x8_x9_x10)
	 						init_pos_found = True
	 						count=count+1

					if key3 in line and init_gra_found != True:
	 					nex = next(file_iterator)
	 					nex_1 = next(file_iterator)
	 					grasp = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
	 					if grasp != []: 
	 						if grasp == [27503.0] or grasp == [1.0]:
	 							grasp_var = True
	 						else:
	 							grasp_var = False
	 						x11 = [grasp_var]
	 						#print('\n- start_grasp_state: -')
	 						#print(x11)
	 						init_gra_found = True
	 						count=count+1

		zero_tupla = x0_x1_x2 + x3_x4_x5_x6_x7_x8_x9_x10 + x11
		trace.append(zero_tupla)
		n_upla = [x0_x1_x2,x3_x4_x5_x6_x7_x8_x9_x10,x11]

	# check for new messages

		with open(file_name) as file_iterator:	
	 		for line in file_iterator:
	 			if fail == 0: 

	 				# check for new battery messages

	 				if key1 in line:
	 					nex = next(file_iterator)
	 					nex_1 = next(file_iterator)
	 					bat_level = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
	 					if bat_level != []:
	 						#print('\n- New Battery Message -')
	 						#print(bat_level)
	 						bat_level=bat_level[0]
	 						if bat_level<10:
	 							fail = 1
	 						min_bat = 0
	 						max_bat = 101
	 						n_bit = 3 
	 						x0_x1_x2 = bin_convert(bat_level, min_bat, max_bat, n_bit)
	 						
	 						# update the trace adding new tupla 

	 						if x0_x1_x2 != n_upla[0]:
	 							#print('\n**update battery**')
	 							n_upla[0] = x0_x1_x2
	 							tupla=n_upla[0]+n_upla[1]+n_upla[2]
	 							#print(tupla)
	 							trace.append(tupla)
	 						else: 
	 							continue

	 				# check for new position messages

	 				if key2 in line:
	 					nex = next(file_iterator)
	 					nex_1 = next(file_iterator)
	 					rob_pose = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
	 					if rob_pose != []:
	 						x_pose = rob_pose[0]
	 						y_pose = rob_pose[1]
	 						if check_pose == 1:
	 							p1 = (x_pose,y_pose)
	 							p2 = (kx_pose, ky_pose)
	 							#print(p1)
	 							#print(p2)
	 							dist = math.dist(p1,p2)
	 							if dist < 0.25:
	 								reached = 1
	 						x_bin = bin_convert(x_pose, a0, a1, n)
	 						y_bin = bin_convert(y_pose, b0, b1, n)
	 						x3_x4_x5_x6_x7_x8_x9_x10 = x_bin + y_bin
	 						
	 						# update the trace adding new tupla
	 					
	 						if x3_x4_x5_x6_x7_x8_x9_x10 != n_upla[1]:
	 							#print('\n**update position**')
	 							n_upla[1] = x3_x4_x5_x6_x7_x8_x9_x10
	 							tupla=n_upla[0]+n_upla[1]+n_upla[2]
	 							#print(tupla)
	 							trace.append(tupla)
	 						else:
	 							continue

	 				# check for new grasp messages

	 				if key3 in line:
	 					nex = next(file_iterator)
	 					nex_1 = next(file_iterator)
	 					grasp = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
	 					if grasp != []: 
	 						#print('\n- New Grasp Message -')
	 						if grasp == [27503.0] or grasp == [1.0]:
	 							grasp_var = True
	 						else:
	 							grasp_var = False
	 						x11 = [grasp_var]

	 						# update the trace adding new tupla
	 						
	 						if x11 != n_upla[2]:						
	 							#print('\n**update grasp**')
	 							n_upla[2] = x11
	 							tupla=n_upla[0]+n_upla[1]+n_upla[2]
	 							#print(tupla)
	 							trace.append(tupla)
	 						else:
	 							continue

	 				if key4 in line:
	 					nex = next(file_iterator)
	 					if check_pose == 0:
		 					if key5 in nex:
		 						nex_1 = next(file_iterator)
	 							k_pose = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
	 							if k_pose != []:
	 								check_pose = 1
	 								kx_pose = k_pose[0]
	 								ky_pose = k_pose[1]
			 						#print(kx_pose, ky_pose)
			 			else:
			 				continue



	 			elif(fail == 1):
	 				break

		print('\nTrace:\n')
		#print(len(trace))
		print(trace)

	# save the trace as a json file, if the robot reached the kitchen the task is complete and the trace will be indicate ad trace_s 
	# instead if for some reason the robot don't reach the kicthen the trace is indicate ad trace_f 

		if fail == 0 and reached == 1:
			print("SUCCESS")
			with open('trace_s.json', "w") as outfile:
	 			json.dump(trace, outfile)
		elif fail == 1 or reached == 0:
			print("FAILURE")
			with open('trace_f.json', "w") as outfile:
	 			json.dump(trace, outfile)

################################################ json trace folder generation ###########################################################################################
	
	elif val == "2":
		print("Enter the coordinates of the extremes of the simulation map:")
		a0 = float(input("x0: " ))
		a1 = float(input("x1: " ))
		b0 = float(input("y0: " ))
		b1 = float(input("y1: " ))
		log_path = input("Enter the path to the folder containing the log files: ")
		print("Conversion being processed.." )
		if os.path.exists(path) == True:
			shutil.rmtree(path)

		files = os.listdir(log_path)
		for file in files:
			#print(file)
			count_ = count_+1
			#print(path+"/"+file)
			file_name=Path(log_path+"/"+file)

# initialize the trace with the zero tuple
			while count < 3:
				with open(file_name) as file_iterator:
					for line in file_iterator:

						if key1 in line and init_bat_found != True:
							nex = next(file_iterator)
							nex_1 = next(file_iterator)
							bat_level = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
							if bat_level != []:
		 						#print('\n- start_battery_state -')
		 						bat_level= bat_level[0]
		 						min_bat = 0
		 						max_bat = 101
		 						n_bit = 3 
		 						x0_x1_x2 = bin_convert(bat_level, min_bat, max_bat, n_bit)
		 						#print(x0_x1_x2)
		 						init_bat_found = True
		 						count=count+1

						if key2 in line and init_pos_found != True:
		 					nex = next(file_iterator)
		 					nex_1 = next(file_iterator)
		 					rob_pose = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
		 					

		 					if rob_pose != []:
		 						x_pose = rob_pose[0]
		 						y_pose = rob_pose[1]
		 						

		 						x_bin = bin_convert(x_pose, a0, a1, n)
		 						y_bin = bin_convert(y_pose, b0, b1, n)
		 						x3_x4_x5_x6_x7_x8_x9_x10 = x_bin + y_bin

		 						#print('\n- start_position_state: -')
		 						#print(x3_x4_x5_x6_x7_x8_x9_x10)
		 						init_pos_found = True
		 						count=count+1

						if key3 in line and init_gra_found != True:
		 					nex = next(file_iterator)
		 					nex_1 = next(file_iterator)
		 					grasp = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
		 					if grasp != []: 
		 						if grasp == [27503.0] or grasp == [1.0]:
		 							grasp_var = True
		 						else:
		 							grasp_var = False
		 						x11 = [grasp_var]
		 						#print('\n- start_grasp_state: -')
		 						#print(x11)
		 						init_gra_found = True
		 						count=count+1

			zero_tupla = x0_x1_x2 + x3_x4_x5_x6_x7_x8_x9_x10 + x11
			trace.append(zero_tupla)
			n_upla = [x0_x1_x2,x3_x4_x5_x6_x7_x8_x9_x10,x11]
			#print(n_upla)
			init_gra_found = False
			init_bat_found = False
			init_pos_found = False
			count = 0

		# check for new messages

			with open(file_name) as file_iterator:	
		 		for line in file_iterator:
		 			if fail == 0: 

		 				# check for new battery messages

		 				if key1 in line:
		 					nex = next(file_iterator)
		 					nex_1 = next(file_iterator)
		 					bat_level = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
		 					if bat_level != []:
		 						#print('\n- New Battery Message -')
		 						#print(bat_level)
		 						bat_level=bat_level[0]
		 						if bat_level<10:
		 							fail = 1
		 						min_bat = 0
		 						max_bat = 101
		 						n_bit = 3 
		 						x0_x1_x2 = bin_convert(bat_level, min_bat, max_bat, n_bit)
		 						
		 						# update the trace adding new tupla 

		 						if x0_x1_x2 != n_upla[0]:
		 							#print('\n**update battery**')
		 							n_upla[0] = x0_x1_x2
		 							tupla=n_upla[0]+n_upla[1]+n_upla[2]
		 							#print(tupla)
		 							trace.append(tupla)
		 						else: 
		 							continue

		 				# check for new position messages

		 				if key2 in line:
		 					nex = next(file_iterator)
		 					nex_1 = next(file_iterator)
		 					rob_pose = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
		 					if rob_pose != []:
		 						x_pose = rob_pose[0]
		 						y_pose = rob_pose[1]
		 						#print("position", x_pose, y_pose)
		 						
		 						if check_pose == 1:
		 							p1 = (x_pose,y_pose)
		 							p2 = (kx_pose, ky_pose)
		 							#print(p1)
		 							#print(p2)
		 							dist = math.dist(p1,p2)
		 							#print(dist)
		 							if dist < 0.35:
		 								reached = 1

		 						x_bin = bin_convert(x_pose, a0, a1, n)
		 						y_bin = bin_convert(y_pose, b0, b1, n)
		 						x3_x4_x5_x6_x7_x8_x9_x10 = x_bin + y_bin
		 						
		 						# update the trace adding new tupla
		 					
		 						if x3_x4_x5_x6_x7_x8_x9_x10 != n_upla[1]:
		 							#print('\n**update position**')
		 							n_upla[1] = x3_x4_x5_x6_x7_x8_x9_x10
		 							tupla=n_upla[0]+n_upla[1]+n_upla[2]
		 							#print(tupla)
		 							trace.append(tupla)
		 						else:
		 							continue

		 				# check for new grasp messages

		 				if key3 in line:
		 					nex = next(file_iterator)
		 					nex_1 = next(file_iterator)
		 					grasp = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
		 					if grasp != []: 
		 						#print('\n- New Grasp Message -')
		 						if grasp == [27503.0] or grasp == [1.0]:
		 							grasp_var = True
		 						else:
		 							grasp_var = False
		 						x11 = [grasp_var]

		 						# update the trace adding new tupla
		 						
		 						if x11 != n_upla[2]:						
		 							#print('\n**update grasp**')
		 							n_upla[2] = x11
		 							tupla=n_upla[0]+n_upla[1]+n_upla[2]
		 							#print("GRASP")
		 							trace.append(tupla)
		 						else:
		 							continue

			 			if key4 in line:
		 					nex = next(file_iterator)
		 					if check_pose == 0:
			 					if key5 in nex:
			 						nex_1 = next(file_iterator)
		 							k_pose = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
		 							if k_pose != []:
		 								check_pose = 1
		 								kx_pose = k_pose[0]
		 								ky_pose = k_pose[1]
				 						#print(kx_pose, ky_pose)
				 			else:
				 				continue

		 			elif(fail == 1):
		 				break

		#print('\nTrace:\n')
		#	print(len(trace))
		#print(trace)

	# save the trace as a json file, if the robot reached the kitchen the task is complete and the trace will be indicate ad trace_s 
	# instead if for some reason the robot don't reach the kicthen the trace is indicate ad trace_f 

			os.makedirs(path, exist_ok=True)
			if reached == 1:
				print('Trace n.',count_)
				print("SUCCESS")
				with open(os.path.join(path, file.replace(".txt", "") + '_s.json'), "w") as outfile:
		 			json.dump(trace, outfile)
				fail = 0
				reached=0
				n_s = n_s + 1
				trace.clear()

			elif fail == 1 or reached == 0:
				print('Trace n.',count_)
				print("FAILURE")
				if fail==1:
					print("critical battery level")
				elif reached==0:
					print("robot did't reach the kitchen")
				with open(os.path.join(path, file.replace(".txt", "") + '_f.json'), "w") as outfile:
		 			json.dump(trace, outfile)
				fail = 0
				reached=0
				n_f = n_f +1
				trace.clear()

		print("Conversion finished, you can find your traces in the json_trace_folder")
		print("Total SUCCESS: ", n_s)
		print("Total FAILURE: ", n_f)

######################################################### sample generation #############################################################################################

	elif val == "3":
		trace_path = input("Enter the path to the folder containing the traces that will make up the sample: ")
		print("Sample being processed.. ")
		time.sleep(1)
		outfilename = "sample.json"
		x=os.listdir(trace_path)

		succ = []
		fail = []
		i=0
		i_ = 0
		_i = 0

		while i < len(x):
		    if ("_s.json" in x[i]) == True:
		        succ.append(x[i])
		        i=i+1
		    elif ("_f.json" in x[i]) == True:
		        fail.append(x[i])
		        i=i+1

		ls = len(succ)
		lf = len(fail)

		with open(outfilename, 'w') as outfile:

		    outfile.write('{ "var_names": ["Battery_1dd", "Battery_d1d", "Battery_dd1", "X_1ddd", "X_d1dd", "X_dd1d", "X_ddd1", "Y_1ddd", "Y_d1dd", "Y_dd1d", "Y_ddd1", "Grasp"], \n\n')
		    outfile.write('"positive_traces": [ \n\n')

		    while i_ < (ls-1):
		        with open(trace_path+"/"+succ[i_], 'r') as readfile:
		             outfile.write(readfile.read() + "\n\n")
		             outfile.write(",")
		        i_=i_+1

		    with open(trace_path+"/"+succ[ls-1], 'r') as readfile:
		        outfile.write(readfile.read() + "\n\n")
		        
		    outfile.write('], "negative_traces": [ \n\n')

		    while _i < (lf-1): 
		        with open(trace_path+"/"+fail[_i], 'r') as readfile:
		             outfile.write(readfile.read() + "\n\n")
		             outfile.write(",")
		        _i=_i+1

		    with open(trace_path+"/"+fail[lf-1], 'r') as readfile:
		        outfile.write(readfile.read() + "\n\n")

		    outfile.write('] }')

		print("The sample is ready. In the folder you can find the sample.json file")
		
	# entering except block
except :
	print("\nThe file or this directory doesn't exist!")