# encoding: utf-8
import json
import sys
import numpy as np

task_list = [
    "中译外-英语",
    "中译外-法语",
    "中译外-葡萄牙语",
    "中译外-西班牙语",
    "中译外-日语",
    "中译外-土耳其语",
    "中译外-俄语",
    "中译外-阿拉伯语",
    "中译外-韩语",
    "中译外-泰语",
    "中译外-意大利语",
    "中译外-德语",
    "中译外-越南语",
    "中译外-马来语",
    "中译外-印尼语",
    "外译中-法语",
    "外译中-西班牙语",
    "外译中-俄语",
    "外译中-英语",
    "外译中-葡萄牙语",
    "外译中-土耳其语",
    "外译中-阿拉伯语",
    "外译中-日语",
    "外译中-韩语",
    "外译中-泰语",
    "外译中-意大利语",
    "外译中-德语",
    "外译中-越南语",
    "外译中-马来语",
    "外译中-印尼语"
]

args = sys.argv
input_file = args[1]

score_map = {}
for line in open(input_file).readlines():
    j = json.loads(line)
    data = []
    question = j["origin_text"]

    if "correct_res" in j:
        correct_res = j["correct_res"]
    elif "reference" in j:
        correct_res = j["reference"]
    else:
        print("error")
        continue

    if "hunyuan_output" in j:
        answer = j["hunyuan_output"]
    elif "answer" in j:
        answer = j["answer"]
    elif "output" in j:
        answer = j["output"]
    else:
        print("answer key error!")
        continue

    comet_score =  j["wmt22-comet-da_withref_score"] # note: this is the key for comet

    if "l1" in j:
        l1 = j["l1"]
        l2 = j["l2"]
        l3 = j["l3"]
    else:
        l1 = j["一级类目"]
        l2 = j["二级类目"]
        l3 = j["三级类目"]

    if "长文本" in l1:
        continue

    task = l3 + "-" + l2
    if task not in score_map:
        score_map[task] = []
    score_map[task].append(comet_score)

# 分数统计
all_score_list = []
zh_2_foreign_list = []
foreign_2_zh_list = []
zh_2_foreign_cnt = 0
foreign_2_zh_cnt = 0

for task in task_list:
    if task not in score_map:
        continue
    cnt = len(score_map[task])
    avg_score = np.average(score_map[task])*100 # 分数乘以100
    print(task + "\t" + str(cnt) + "\t" + str(avg_score))
    all_score_list.append(avg_score)
    if "中译外" in task:
        zh_2_foreign_list.append(avg_score)
        zh_2_foreign_cnt += cnt
    elif "外译中" in task:
        foreign_2_zh_list.append(avg_score)
        foreign_2_zh_cnt += cnt
    else:
        print("error")

print("中译外-平均" + "\t" + str(zh_2_foreign_cnt) + "\t" + str(np.average(zh_2_foreign_list)))
print("外译中-平均" + "\t" + str(foreign_2_zh_cnt) + "\t" + str(np.average(foreign_2_zh_list)))
print("整体-平均" + "\t" + str(zh_2_foreign_cnt+foreign_2_zh_cnt) + "\t" + str(np.average(zh_2_foreign_list+foreign_2_zh_list)))

print("done")
