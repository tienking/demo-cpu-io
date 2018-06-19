import copy

#Checking finish all process
def checkFinal(input_dict):
	for value in input_dict.values():
		for process_time in value:
			if len(process_time) > 0:
				return False
	return True

#Checking process that finish all CPU and IO
def checkFinishCPU(input_dict, number):
	if len(input_dict[number][0]) == 0:
		return True
	return False

#Finding minimum process time
def findMinProcess(ready_list):
	min_process = ready_list[0]
	for ready_process in ready_list:
		if ready_process[1] < min_process[1]:
			min_process = ready_process[:]
	return min_process

#Using for both CPU and general IO
def run(ready_list, ready_process, process_state, input_dict):
	process_number = ready_process[0]
	return_check = False
	for process in ready_list:
		if process[0] == ready_process[0]:
			process[1] -= 1
			if process[1] == 0:
				return_check = True
				ready_list.remove(process)
				if process_state == "cpu":
					del input_dict[ready_process[0]][0][0]
				elif process_state == "io":
					del input_dict[ready_process[0]][1][0]
	return (ready_list, process_number, return_check)

#Using for separate IO
def runIO(io_board, io_ready_list, input_dict, finish_io_list, option_list):
	temp_list = []
	for io in io_ready_list:
		temp_list.append(io[0])
	for index in range(len(io_board)):
		if option_list[index] in temp_list:
			io_board[index].append(1)
		else:
			io_board[index].append(0)
	for io in io_ready_list:
		io[1] -= 1
		if io[1] == 0:
			finish_io_list.append(io[0])
			io_ready_list.remove(io)
			del input_dict[io[0]][1][0]
	return (io_board, io_ready_list, input_dict, finish_io_list)

def FCFS(input_dict, option_list):
	cpu_board = []
	io_board = [[],[]]
	ready_list = []
	io_ready_list = [[],[]]
	io_board = [[],[[] for _ in range(len(option_list[1]))]]
	cpu_list = sorted(list(input_dict.keys()))
	for cpu in cpu_list:
		ready_list.append([cpu, input_dict[cpu][0][0]])
	while checkFinal(input_dict) == False:
		new_cpu = []

		#Running general IO
		if len(io_ready_list[0]) > 0:
			io_ready_list[0], process_number, return_check = run(io_ready_list[0], io_ready_list[0][0], 'io', input_dict)
			io_board[0].append(process_number)
			if return_check == True:
				new_cpu.append([process_number, input_dict[process_number][0][0]])
		else:
			io_board[0].append(0)

		#Running separate IO
		if len(io_ready_list[1]) > 0:
			finish_io_list = []
			io_board[1], io_ready_list[1], input_dict, finish_io_list = runIO(io_board[1], io_ready_list[1], input_dict, finish_io_list, option_list[1])
			if len(finish_io_list) > 0:
				finish_io_list.sort()
				for process_number in finish_io_list:
					new_cpu.append([process_number, input_dict[process_number][0][0]])
		else:
			for io in io_board[1]:
				io.append(0)

		#Running CPU
		if len(ready_list) > 0:
			ready_list, process_number, return_check = run(ready_list, ready_list[0], 'cpu', input_dict)
			cpu_board.append(process_number)
			if checkFinishCPU(input_dict, process_number) == False and return_check == True:
				if process_number in option_list[0]:
					io_ready_list[0].append([process_number, input_dict[process_number][1][0]])
				else:
					io_ready_list[1].append([process_number, input_dict[process_number][1][0]])
		else:
			cpu_board.append(0)	

		#Return CPU after finish IO
		if new_cpu != []:
			new_cpu.sort(key=lambda x: x[0])
			for process in new_cpu:
				ready_list.append(process)

	return (cpu_board, io_board)

def SJF(input_dict, option_list):
	cpu_board = []
	io_board = [[],[]]
	ready_list = []
	io_ready_list = [[],[]]
	io_board = [[],[[] for _ in range(len(option_list[1]))]]
	cpu_list = sorted(list(input_dict.keys()))
	for cpu in cpu_list:
		ready_list.append([cpu, input_dict[cpu][0][0]])
	running_process = 0
	while checkFinal(input_dict) == False:
		new_cpu = []

		#Running general IO
		if len(io_ready_list[0]) > 0:
			io_ready_list[0], process_number, return_check = run(io_ready_list[0], io_ready_list[0][0], 'io', input_dict)
			io_board[0].append(process_number)
			if return_check == True:
				new_cpu.append([process_number, input_dict[process_number][0][0]])
		else:
			io_board[0].append(0)
		
		#Running separate IO
		if len(io_ready_list[1]) > 0:
			finish_io_list = []
			io_board[1], io_ready_list[1], input_dict, finish_io_list = runIO(io_board[1], io_ready_list[1], input_dict, finish_io_list, option_list[1])
			if len(finish_io_list) > 0:
				finish_io_list.sort()
				for process_number in finish_io_list:
					new_cpu.append([process_number, input_dict[process_number][0][0]])
		else:
			for io in io_board[1]:
				io.append(0)
		
		#Running CPU
		if len(ready_list) > 0:
			if running_process == 0:
				min_process = findMinProcess(ready_list)
				running_process = min_process[1]
			ready_list, process_number, return_check = run(ready_list, min_process, 'cpu', input_dict)
			cpu_board.append(process_number)
			running_process -= 1
			if checkFinishCPU(input_dict, process_number) == False and return_check == True:
				if process_number in option_list[0]:
					io_ready_list[0].append([process_number, input_dict[process_number][1][0]])
				else:
					io_ready_list[1].append([process_number, input_dict[process_number][1][0]])
		else:
			cpu_board.append(0)

		#Return CPU after finish IO
		if new_cpu != []:
			new_cpu.sort(key=lambda x: x[0])
			for process in new_cpu:
				ready_list.append(process)

	return (cpu_board, io_board)

def SRTF(input_dict, option_list):
	cpu_board = []
	io_board = [[],[]]
	ready_list = []
	io_ready_list = [[],[]]
	io_board = [[],[[] for _ in range(len(option_list[1]))]]
	cpu_list = sorted(list(input_dict.keys()))
	for cpu in cpu_list:
		ready_list.append([cpu, input_dict[cpu][0][0]])
	while checkFinal(input_dict) == False:
		new_cpu = []

		#Running general IO
		if len(io_ready_list[0]) > 0:
			io_ready_list[0], process_number, return_check = run(io_ready_list[0], io_ready_list[0][0], 'io', input_dict)
			io_board[0].append(process_number)
			if return_check == True:
				new_cpu.append([process_number, input_dict[process_number][0][0]])
		else:
			io_board[0].append(0)
		
		#Running separate IO
		if len(io_ready_list[1]) > 0:
			finish_io_list = []
			io_board[1], io_ready_list[1], input_dict, finish_io_list = runIO(io_board[1], io_ready_list[1], input_dict, finish_io_list, option_list[1])
			if len(finish_io_list) > 0:
				finish_io_list.sort()
				for process_number in finish_io_list:
					new_cpu.append([process_number, input_dict[process_number][0][0]])
		else:
			for io in io_board[1]:
				io.append(0)

		#Running CPU
		if len(ready_list) > 0:
			min_process = findMinProcess(ready_list)
			ready_list, process_number, return_check = run(ready_list, min_process, 'cpu', input_dict)
			cpu_board.append(process_number)
			if checkFinishCPU(input_dict, process_number) == False and return_check == True:
				if process_number in option_list[0]:
					io_ready_list[0].append([process_number, input_dict[process_number][1][0]])
				else:
					io_ready_list[1].append([process_number, input_dict[process_number][1][0]])
		else:
			cpu_board.append(0)
		
		#Return CPU after finish IO
		if new_cpu != []:
			new_cpu.sort(key=lambda x: x[0])
			for process in new_cpu:
				ready_list.append(process)

	return (cpu_board, io_board)

def RR(input_dict, q, option_list):
	cpu_board = []
	io_board = [[],[]]
	ready_list = []
	io_ready_list = [[],[]]
	io_board = [[],[[] for _ in range(len(option_list[1]))]]
	cpu_list = sorted(list(input_dict.keys()))
	for cpu in cpu_list:
		ready_list.append([cpu, input_dict[cpu][0][0]])
	running_time = q
	running_process = ready_list[0][:]
	while checkFinal(input_dict) == False:
		new_cpu = []

		#Running general IO
		if len(io_ready_list[0]) > 0:
			io_ready_list[0], process_number, return_check = run(io_ready_list[0], io_ready_list[0][0], 'io', input_dict)
			io_board[0].append(process_number)
			if return_check == True:
				new_cpu.append([process_number, input_dict[process_number][0][0]])
		else:
			io_board[0].append(0)
		
		#Running separate IO
		if len(io_ready_list[1]) > 0:
			finish_io_list = []
			io_board[1], io_ready_list[1], input_dict, finish_io_list = runIO(io_board[1], io_ready_list[1], input_dict, finish_io_list, option_list[1])
			if len(finish_io_list) > 0:
				finish_io_list.sort()
				for process_number in finish_io_list:
					new_cpu.append([process_number, input_dict[process_number][0][0]])
		else:
			for io in io_board[1]:
				io.append(0)

		#Running CPU
		if len(ready_list) > 0:	
			if running_time == 0 and len(ready_list) > 0:
				stop_process = ready_list[0][:]
				del ready_list[0]
				ready_list.append(stop_process)
				running_time = q

			ready_list, process_number, return_check = run(ready_list, ready_list[0], 'cpu', input_dict)
			cpu_board.append(process_number)
			running_time -= 1
			
			if checkFinishCPU(input_dict, process_number) == False and return_check == True:
				if process_number in option_list[0]:
					io_ready_list[0].append([process_number, input_dict[process_number][1][0]])
				else:
					io_ready_list[1].append([process_number, input_dict[process_number][1][0]])
				running_time = q
		else:
			cpu_board.append(0)
		
		#Return CPU after finish IO
		if new_cpu != []:
			new_cpu.sort(key=lambda x: x[0])
			for process in new_cpu:
				ready_list.append(process)

	return (cpu_board, io_board)

def display(cpu_board, io_board, number_cpu, option_list):
	#Print number line
	number_index = "     |"
	for i in range(1, len(cpu_board) + 1):
		number_index += "{0:<2}|".format(i)
	print(number_index)

	#Print CPU
	for i in range(1,number_cpu + 1):
		print_line = "P{0:<3} |".format(i)
		for time in cpu_board:
			if time == i:
				print_line += "--|"
			else:
				print_line += "  |"
		print(print_line)

	#Print separate IO
	if len(option_list[1]) > 0:
		i = 0
		for process_number in option_list[1]:
			io_print_line = "IO{0:<2} |".format(process_number)
			for time in io_board[1][i]:
				if time == 1:
					io_print_line += "--|"
				else:
					io_print_line += "  |"
			print(io_print_line)
			i += 1

	#Print general IO
	if len(option_list[0]) > 0:
		io_print_line = "IO   |"
		for time in io_board[0]:
			if time == 0:
				io_print_line += "  |"
			else:
				io_print_line += "{0:<2}|".format(time)
		print(io_print_line)

def runAll():
	input_dict = {}
	i = 1
	while True:
		#Input process string separate by ","
		new_process = input("Process {0}: ".format(i))
		new_process = new_process.split(",")
		cpu = []
		io = []
		for index,time in enumerate(new_process):
			if index % 2 == 0:
				cpu.append(int(time))
			else:
				io.append(int(time))
		input_dict[i] = [cpu, io]
		option = int(input("[1]Add\t[2]Run\nSelect: "))
		if option == 2:
			break
		elif option == 1:
			i+=1
		else:
			raise ValueError
	q = int(input("Enter q (for RR): "))
	#Test data
	#input_dict = {1:[[1,1,1,1,1],[4,4,4,4]],2:[[2,2,3],[7,7]],3:[[13,2],[6]]}

	#Get list of process that have separate IO
	se_process = input("Processes have separate IO: ")
	if "," in se_process:
		se_process = se_process.split(",")
		se_process = [int(x) for x in se_process].sort()
	elif se_process != "":
		se_process = [int(se_process)]
	else:
		se_process = []

	#Check if process number not in input processes
	for process in se_process:
		if process not in list(range(1, len(input_dict) + 1)):
			raise ValueError

	#Test se_process
	#se_process = [1]
	option_list = [[],[]]
	for process_number in range(1, len(input_dict) + 1):
		if process_number in se_process:
			option_list[1].append(process_number)
		else:
			option_list[0].append(process_number)
	print("Processes have general IO: {0}".format(",".join(str(x) for x in option_list[0])))

	#Make a copy of input_dict to be sure that can be ran in another algorithm again
	number_cpu = len(input_dict)
	print("\n\n[FCFS]")
	run_dict = copy.deepcopy(input_dict)
	cpu_board, io_board = FCFS(run_dict, option_list)
	display(cpu_board, io_board, number_cpu, option_list)
	print("\n\n[SJF]")
	run_dict = copy.deepcopy(input_dict)
	cpu_board, io_board = SJF(run_dict, option_list)
	display(cpu_board, io_board, number_cpu, option_list)
	print("\n\n[SRTF]")
	run_dict = copy.deepcopy(input_dict)
	cpu_board, io_board = SRTF(run_dict, option_list)
	display(cpu_board, io_board, number_cpu, option_list)
	print("\n\n[RR]")
	print("q =", q)
	run_dict = copy.deepcopy(input_dict)
	cpu_board, io_board = RR(run_dict, q, option_list)
	display(cpu_board, io_board, number_cpu, option_list)

def main():
	print("\t[MY DEMO]")
	while True:
		runAll()
		select = int(input("[1]Continue\t[2]Exit\nSelect: "))
		if select == 2:
			break
		elif select != 1:
			raise ValueError

if __name__ == '__main__':
	main()