import os, sys
import numpy as np
import matplotlib.pyplot as plt

def createLabels(data):
    for item in data:
        height = item.get_height()
        plt.text(
            item.get_x()+item.get_width()/2.,
            height*1.05,
            '%d' % int(height),
            ha = "center",
            va = "bottom",
        )

easy_cmd = 'python3 HW3.py --level easy'
medium_cmd = 'python3 HW3.py --level medium'
hard_cmd = 'python3 HW3.py --level hard'
hint_ls = [" less", " middle", " more"]
iterations = 10
easy_success = 0
medium_success = 0
hard_success = 0

col_count = 3
bar_width = 0.2
index = np.arange(col_count)
easy_scores = []
medium_scores = []
hard_scores = []

for j in range(len(hint_ls)):
    easy_success = 0
    medium_success = 0
    hard_success = 0
    print("[INFO] hint" + hint_ls[j] + " part start: ")
    for i in range(iterations):
        p = os.popen(easy_cmd + " --hint" + hint_ls[j], 'r')
        result = p.read()
        if result == "success: True\n":
            easy_success += 1
    print("    success rate for easy part: %f %%" %(easy_success / iterations * 100))

    for i in range(iterations):
        p = os.popen(medium_cmd + " --hint" + hint_ls[j], 'r')
        result = p.read()
        if result == "success: True\n":
            medium_success += 1
    print("    success rate for medium part: %f %%" %(medium_success / iterations * 100))

    for i in range(iterations):
        p = os.popen(hard_cmd + " --hint" + hint_ls[j], 'r')
        result = p.read()
        if result == "success: True\n":
            hard_success += 1
    print("    success rate for hard part: %f %%" %(hard_success / iterations * 100))

    easy_scores.append(easy_success / iterations * 100)
    medium_scores.append(medium_success / iterations * 100)
    hard_scores.append(hard_success / iterations * 100)

ax2  = plt.subplot(1,1,1)
easy = plt.bar(index,
           tuple(easy_scores),
           bar_width,
           alpha=.4,
           label="easy")
medium = plt.bar(index+0.2,
            tuple(medium_scores),
            bar_width,
            alpha=.4,
            label="medium")
hard = plt.bar(index+0.4,
            tuple(hard_scores),
            bar_width,
            alpha=.4,
            label="hard") # x,y ,width

createLabels(easy)
createLabels(medium)
createLabels(hard)

plt.ylabel("success rate (%)")
plt.xlabel("initial safe cells")
figure_title = "initial safe cells vs. success rate"
plt.text(0.5, 1.08, figure_title,
         horizontalalignment='center',
         fontsize=20,
         transform = ax2.transAxes)
plt.xticks(index+.3 / 2 ,("less","middle","more"))
plt.legend()
plt.grid(True)
plt.savefig("compare.png")
plt.show()

