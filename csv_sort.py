#encoding=UTF-8
import sys
import csv

sort_col = [3, 1]
path = ""
if len(sys.argv) > 2:
    path = sys.argv[1]
    print(path)
if len(sys.argv) > 3:
    sort_col = int(sys.argv[3])
    print(sort_col)

lines = list()
with open(path, 'r') as f:
    lines = f.readlines()

line_num = len(lines)
sort_lines = list()
max_col = max(sort_col)
for i in range(3, line_num):
    line = lines[i]
    line = line.rstrip().split(',')
    if len(line) <= max_col:
        print("line %d column count is not enough.\n", i)
    else:
        sort_lines.append(line)

sort_lines.sort(key = lambda line: (int(line[sort_col[0]]), int(line[sort_col[1]])), reverse = False)

with open(path + "sort.csv", "w") as f:
    for line in sort_lines:
        f.write(",".join(line) + "\n")
