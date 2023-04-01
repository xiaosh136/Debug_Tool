# -*- coding:utf-8 -*-
import os
import sys
import codecs

def lcs(str_1, str_2):
    maxlcs = []
    len_1 = len(str_1)
    len_2 = len(str_2)
    for i in range(0, len_1):
        maxlcs.append([]);
        for j in range(0, len_2):
            maxlcs[-1].append(0)

    for i in range(0, len_2):
        if str_1[0] == str_2[i]:
            maxlcs[0][i] = 1
        elif i != 0:
            maxlcs[0][i] = maxlcs[0][i-1]
        else:
            maxlcs[0][i] = 0

    for i in range(0, len_1):
        if str_1[i] == str_2[0]:
            maxlcs[i][0] = 1
        elif i != 0:
            maxlcs[i][0] = maxlcs[i-1][0]
        else:
            maxlcs[i][0] = 0

    for i in range(1, len_1):
        for j in range(1, len_2):
            if str_1[i] == str_2[j]:
                maxlcs[i][j] = max(maxlcs[i-1][j], maxlcs[i][j-1], maxlcs[i-1][j-1]+1)
            else:
                maxlcs[i][j] = max(maxlcs[i-1][j], maxlcs[i][j-1], maxlcs[i-1][j-1])

    return maxlcs[len_1-1][len_2-1] / float(len_1)
    
def compare(task_file, queue_file):
    with codecs.open(task_file, 'r', encoding='utf-8', errors='ignore') as file:
        task_line_list = file.readlines()
    with codecs.open(queue_file, 'r', encoding='utf-8', errors='ignore') as file:
        queue_line_list = file.readlines()

    result = []
    task_name_ = []
    for queue_line in queue_line_list:
        if not "QueFull" in queue_line:
            continue
        queue_name = queue_line.split("    ")[-1].strip().rstrip()
        for task_line in task_line_list:
            task_name = task_line[0:len(task_line)-2]
            string_consistency = lcs(task_name, queue_name)
            result.append(string_consistency)
            task_name_.append(task_name)
    index = result.index(max(result))
    task_name = task_name_[index].split("    ")[0].rstrip().strip()
    print(task_name)

def main():
    task_file = sys.argv[1]
    queue_file = sys.argv[2]
    compare(task_file, queue_file)

if __name__ == '__main__':
    main()
