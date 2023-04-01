# -*- coding:utf-8 -*-
import os
import sys
import codecs

def TmSplitOneLine(line):
	list_1 = line.split(":")
	list_2 = list_1[1].strip().rstrip().split("(")
	list_3 = line.split(");")
	other = list_3[1].strip().rstrip()
	if "Irq" in other:
		other += ")"
	return list_1[0].strip().rstrip(), list_2[0].strip().rstrip(), other;

def TaskSplitOneLine(line):
	tmp = line.split("    ")
	return tmp[0].strip().rstrip(), eval(tmp[-1])


def analyzeTask(tm_path, task_path):
	with codecs.open(tm_path, 'r', encoding='utf-8', errors='ignore') as file:
		tm_line_list = file.readlines()
	with codecs.open(task_path, 'r', encoding='utf-8', errors='ignore') as file:
		task_line_list = file.readlines()
	stack = []
	result = {}
	unscheduled_task = {}
	pre_is_irq = False
	pre_is_idle = False
	pre_is_leave_sleep = False
	start_time = {}
	all_task_cost = {}
	wake_up_cost = []
	all_task_cost["IN SLEEP"] = 0
	all_task_cost["SYSTEM LOSS(SLEEP)"] = 0
	all_task_cost["SYSTEM LOSS(SCHEDULE)"] = 0
	odd_sleep = []
	odd_schedule = []
	cost_time = {}
	task_prio = {}
	end_time = 0
	t_cur_task = ""
	t_start_time = -1
	idle_start_time = -1
	leave_sleep_time = -1
	i = 0

	for line in task_line_list:
		if len(line) <= 2:
			continue
		task, prio = TaskSplitOneLine(line)
		tmp = task.split("(")
		task_addr = tmp[0].strip().rstrip()
		task_prio[eval(task_addr)] = prio

	for line in tm_line_list:
		if len(line) <= 2:
			continue
		tag, time, other = TmSplitOneLine(line)
		end_time = eval(time)

		if "TASK" in tag:
			t_cur_task = other.split("  ")[-1].strip().rstrip()
			if pre_is_idle is True:
				all_task_cost["SYSTEM LOSS(SCHEDULE)"] += eval(time) - idle_start_time
			if not t_cur_task in all_task_cost:
				all_task_cost[t_cur_task] = 0
			if (not t_cur_task in start_time) or (start_time[t_cur_task][0] == -1):
				start_time[t_cur_task] = [eval(time), i]
				stack.append(t_cur_task)
			elif pre_is_irq:
				all_task_cost["SYSTEM LOSS(SCHEDULE)"] += eval(time) - t_start_time
			t_start_time = eval(time)
			pre_is_irq = False
			pre_is_idle = False

			pre_is_leave_sleep = False

		elif "ENTER IRQ" in tag:
			if t_cur_task != "":
				all_task_cost[t_cur_task] += eval(time) - t_start_time
			irq_name = "IRQ " + other.split("  ")[-1].strip().rstrip()
			if pre_is_irq is True and len(stack) == 0:
				all_task_cost["SYSTEM LOSS(SCHEDULE)"] += eval(time) - t_start_time
			stack.append(irq_name)
			start_time[irq_name] = [eval(time), i]
			if pre_is_leave_sleep is True:
				all_task_cost["SYSTEM LOSS(SLEEP)"] += eval(time) - leave_sleep_time
				wake_up_cost.append([irq_name, leave_sleep_time, eval(time) - leave_sleep_time])
			if pre_is_idle is True:
				all_task_cost["SYSTEM LOSS(SCHEDULE)"] += eval(time) - idle_start_time
			pre_is_irq = False
			pre_is_idle = False
			pre_is_leave_sleep = False

		elif "LEAVE IRQ" in tag:
			if len(stack) != 0 and "IRQ" in stack[-1]:
				val = stack[-1]
				cost_time[val] = eval(time) - start_time[val][0]
				irq = val[4:]
				tmp = irq.split("(")
				irq_addr = tmp[0].strip().rstrip()
				if (not val in result):
					result[val] = [[start_time[val][0], eval(time), cost_time[val]]]
				else:
					result[val].append([start_time[val][0], eval(time), cost_time[val]])
				start_time[val] = [-1, -1]
				while len(stack) != 0 and start_time[stack[-1]][0] == -1:
					stack.pop()
			pre_is_irq = True
			pre_is_idle = False
			pre_is_leave_sleep = False
			t_start_time = eval(time)

		elif "IDLE" in tag:
			pre_is_idle = True
			pre_is_leave_sleep = False
			idle_start_time = eval(time)
			if len(stack) == 0:
				if pre_is_irq is True:
					all_task_cost["SYSTEM LOSS(SCHEDULE)"] += eval(time) - t_start_time
				i += 1
				pre_is_irq = False
				continue

			cur_task = stack[-1]
			tmp = cur_task.split("(")
			cur_task_addr = tmp[0].strip().rstrip()
			tag_ = ""
			if i + 1 < len(tm_line_list) and len(tm_line_list[i + 1]) > 2:
				tmp = tm_line_list[i+1]
				tag_, time_, other_ = TmSplitOneLine(tmp)
				next_task = other_.split("  ")[-1].strip().rstrip()
				tmp = next_task.split("(")
				next_task_addr = tmp[0].strip().rstrip()

			if pre_is_irq is True:
				pre_is_irq = False
				if i + 1 < len(tm_line_list) and len(tm_line_list[i + 1]) > 2:
					if tag_ != "" and "TASK" in tag_ and task_prio[eval(next_task_addr)] < task_prio[eval(cur_task_addr)]:
						all_task_cost["SYSTEM LOSS(SCHEDULE)"] += eval(time) - t_start_time
						t_cur_task = ""
						i += 1
						continue
				else:
					i += 1
					continue

			if t_cur_task != "":
				all_task_cost[t_cur_task] += eval(time) - t_start_time
				t_cur_task = ""

			cost_time[cur_task] = eval(time) - start_time[cur_task][0]
			name = cur_task.split("  ")[-1].strip().rstrip()
			if (not name in result):
				result[name] = [[start_time[cur_task][0], eval(time), cost_time[cur_task]]]
			else:
				result[name].append([start_time[cur_task][0], eval(time), cost_time[cur_task]])
			tmp_time = start_time[cur_task][0]
			start_time[cur_task] = [-1, -1]

			while len(stack) != 0:
				if start_time[stack[-1]][0] == -1:
					stack.pop()
				else:
					stack_top = stack[-1]
					tmp = stack_top.split("(")
					stack_top_addr = tmp[0].strip().rstrip()
					if task_prio[eval(stack_top_addr)] < task_prio[eval(cur_task_addr)]:
						cost_time[stack_top] = eval(time) - start_time[stack_top][0]
						name = stack_top.split("  ")[-1].strip().rstrip()
						odd_schedule.append([name, start_time[stack_top][0], tmp_time])
						if (not name in result):
							result[name] = [[start_time[stack_top][0], eval(time), cost_time[stack_top]]]
						else:
							result[name].append([start_time[stack_top][0], eval(time), cost_time[stack_top]])
						start_time[stack_top] = [-1, -1]
					else:
						break

			if tag_!= "" and "ENTER SLEEP" in tag_:
				while len(stack) != 0:
					stack_top = stack.pop()
					if start_time[stack_top][0] == -1:
						continue
					cost_time[stack_top] = eval(time) - start_time[stack_top][0]
					name = stack_top.split("  ")[-1].strip().rstrip()
					odd_sleep.append([name, start_time[stack_top][0], time_])
					if (not name in result):
						result[name] = [[start_time[stack_top][0], eval(time), cost_time[stack_top]]]
					else:
						result[name].append([start_time[stack_top][0], eval(time), cost_time[stack_top]])
					start_time[stack_top] = [-1, -1]

			pre_is_irq = False

		elif "ENTER SLEEP" in tag:
			t_start_time = eval(time)
			t_cur_task = "IN SLEEP"
			if pre_is_idle is True:
				all_task_cost["SYSTEM LOSS(SLEEP)"] += eval(time) - idle_start_time
			if pre_is_leave_sleep is True:
				all_task_cost["SYSTEM LOSS(SLEEP)"] += eval(time) - leave_sleep_time
			pre_is_irq = False
			pre_is_idle = False
			pre_is_leave_sleep = False

		elif "LEAVE SLEEP" in tag:
			if "IN SLEEP" in t_cur_task:
				all_task_cost[t_cur_task] += eval(time) - t_start_time
				t_cur_task = ""
			pre_is_irq = False
			pre_is_idle = False
			pre_is_leave_sleep = True
			leave_sleep_time = eval(time)

		else:
			pre_is_irq = False
			pre_is_idle = False
			#pre_is_leave_sleep = False
		i += 1
	if len(stack) != 0:
		for task in stack:
			unscheduled_task[task] = start_time[task][0]

	total_time = 0
	for task in result:
		if "IRQ" in task:
			all_task_cost[task] = sum([i[2] for i in result[task]])
	total_time = sum(all_task_cost[i] for i in all_task_cost)
	tmp_list = sorted(all_task_cost.items(), key=lambda x:x[1], reverse=True)

	print("*"*90)
	print("Printing sleep and wake-up comparation...")
	print("*"*90)
	print("NAME".center(50) + " " + "SPEND".center(15) + " " + "PERCENT".center(15))
	print("sleep".center(50) +
			" {:^15} {:^15.2f}%".format(all_task_cost["IN SLEEP"], 100.0 * all_task_cost["IN SLEEP"] / total_time))
	print("wake-up".center(50) +
			" {:^15} {:^15.2f}%".format(total_time - all_task_cost["IN SLEEP"], 100 - 100.0 * all_task_cost["IN SLEEP"] / total_time))
	print("")
	print("")

	print("*"*90)
	print("Printing all tasks runtime status, excluding sleep...")
	print("*"*90)
	total_time -= all_task_cost["IN SLEEP"]
	print("NAME".center(50) + " " + "PRIO.".center(10) + " " + "SPEND".center(10) + " " + "PERCENT".center(10))
	for item in tmp_list:
		if  "SYSTEM LOSS(SLEEP)" in item[0]:
			print("SYSTEM LOSS(SLEEP)".center(50) +
				" {:^10} {:^10d} {:^10.2f}%".format("*", all_task_cost["SYSTEM LOSS(SLEEP)"],\
				100.0 * all_task_cost["SYSTEM LOSS(SLEEP)"] / total_time))
			continue
		if  "SYSTEM LOSS(SCHEDULE)" in item[0]:
			print("SYSTEM LOSS(SCHEDULE)".center(50) +
				" {:^10} {:^10d} {:^10.2f}%".format("*", all_task_cost["SYSTEM LOSS(SCHEDULE)"],\
				100.0 * all_task_cost["SYSTEM LOSS(SCHEDULE)"] / total_time))
			continue
		if "IN SLEEP" in item[0]:
			continue
		if "IRQ" in item[0]:
			tmp = item[0].split("IRQ")
			str = tmp[-1].strip().rstrip()
			print(item[0].center(50) +
				" {:^10} {:^10d} {:^10.2f}%".format("*", item[1], 100.0 * item[1] / total_time))
			continue
		else:
			str = item[0]
		tmp = str.split("(")
		item_addr = tmp[0].strip().rstrip()
		print(item[0].center(50) +
			" {:^10d} {:^10d} {:^10.2f}%".format(task_prio[eval(item_addr)], item[1], 100.0 * item[1] / total_time))
	print("")
	print("")

	print("*"*90)
	print("Following tasks were preempted but have not been re-scheduled or have not performed \nactive-schedule...")
	print("*"*90)
	print("NAME".center(50) + " " + "START".center(20) + "QTS AFTER RUN".center(20))
	for task in unscheduled_task:
		print(task.center(50) + " {:^20}".format(unscheduled_task[task]) + " {:^20}".format(end_time - unscheduled_task[task]))
	print("")
	print("")

	print("*"*90)
	print("Following tasks seems to be ready but system would enter sleep according to tm data,\n need re-check...")
	print("*"*90)
	print("NAME".center(50) + " " + "TASK START".center(20) + " " + "ENTER SLEEP".center(20))
	for task in odd_sleep:
		print(task[0].center(50) + " {:^20} {:^20}".format(task[1], task[2]))
	print("")
	print("")

	print("*"*90)
	print("Following tasks seems to be preempted by lower-priority task according to tm data,\n need re-check...")
	print("*"*90)
	print("NAME".center(50) + " " + "TASK START".center(20) + " " + "CURRENT TASK START".center(20))
	for task in odd_schedule:
		print(task[0].center(50) + " {:^20} {:^20}".format(task[1], task[2]))
	print("")
	print("")

	print("*"*90)
	print("Following IRQ woke up the system...")
	print("*"*90)
	print("IRQ".center(50) + " " + "START".center(20) + " " + "WAKE-UP COST".center(20))
	tmp_list = sorted(wake_up_cost, key=lambda x:x[2], reverse=True)
	for irq in tmp_list:
		print(irq[0].center(50) + " {:^20}".format(irq[1]) + " {:^20}".format(irq[2]))
	print("*"*90)
	print("")
	print("")

	print("*"*90)
	print("Printing the spending-time of per task entry, including the waiting-time after being \ninterrupted by IRQ or preempted by other high-priority tasks...")
	print("*"*90)
	print("NAME".center(50) + " " + "START".center(15) + " " + "END".center(15) + " " + "SPEND".center(10))
	for task in result:
		result[task] = sorted(result[task], key=lambda x:x[2], reverse=True)
		for item in result[task]:
			print(task.center(50) + " {:^15} {:^15} {:^10}".format(item[0], item[1], item[2]))
		print("-"*90)
	print("")
	print("")


def main():
	tm_file = sys.argv[1]
	task_file = sys.argv[2]
	analyzeTask(tm_file, task_file)
	print("Fin...")

if __name__ == '__main__':
	main()
