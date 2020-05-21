import os, sys

easy_cmd = 'python3 HW3.py --level easy'
medium_cmd = 'python3 HW3.py --level medium'
hard_cmd = 'python3 HW3.py --level hard'
iterations = 10
easy_success = 0
medium_success = 0
hard_success = 0

for i in range(iterations):
    p = os.popen(easy_cmd, 'r')
    result = p.read()
    if result == "success: True\n":
        easy_success += 1
print("success rate for easy part: %f" %(easy_success / iterations))

for i in range(iterations):
    p = os.popen(medium_cmd, 'r')
    result = p.read()
    if result == "success: True\n":
        medium_success += 1
print("success rate for medium part: %f" %(medium_success / iterations))

for i in range(iterations):
    p = os.popen(hard_cmd, 'r')
    result = p.read()
    if result == "success: True\n":
        hard_success += 1
print("success rate for hard part: %f" %(hard_success / iterations))

