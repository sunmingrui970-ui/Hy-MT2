# encoding: utf-8

import json
import os
import re
import sys
import numpy as np

def multi_language_data_check(result_path):
    lang_name_map = {
        "ko": "韩语",
        "ru": "俄语",
        "vi": "越南语",
        "th": "泰语",
        "de": "德语",
        "ar": "阿拉伯语",
        "fr": "法语",
        "pt": "葡萄牙语",
        "tr": "土耳其语",
        "ms": "马来语",
        "es": "西班牙语",
        "it": "意大利语",
        "id": "印尼语",
        "en": "英语"
    }

    lang_all_map = {}
    lang_mix_map = {}
    lang_mix_length_map = {}
    chinese_pattern = re.compile(r'[\u4e00-\u9fa5]+')
    for line in open(result_path).readlines():
        j = json.loads(line)
        if "code" in j and j["code"] != 0:
            continue

        if "answer" in j:
            answer = j["answer"]
        elif "output" in j:
            answer = j["output"]
        elif "hunyuan_output" in j:
            answer = j["hunyuan_output"]
        elif "llama3_8b_instruct" in j:
            answer = j["llama3_8b_instruct"]
        elif "response" in j:
            answer = j["response"]
        else:
            continue
        if answer.strip() == "":
            continue

        lang = j["target_lang"]

        if lang not in lang_all_map:
            lang_all_map[lang] = 0
            lang_mix_map[lang] = 0
            lang_mix_length_map[lang] = []
        lang_all_map[lang] += 1

        # 正则匹配有无中文
        chinese_phrases = chinese_pattern.findall(answer)
        if len(chinese_phrases) > 0:
            lang_mix_map[lang] += 1
            lang_mix_length_map[lang].append(len("".join(chinese_phrases)))
            if lang == "en":
                # print(json.dumps(j, ensure_ascii=False))
                print(answer)
                print("****************")

    print("语种\t数据集大小\t混杂个数\t混杂率\t平均混杂长度")
    all_cnt = 0
    err_cnt = 0
    for lang in lang_name_map.keys():
        if lang not in lang_mix_map:
            continue
        rate = 1.0*lang_mix_map[lang]/lang_all_map[lang]
        all_cnt += lang_all_map[lang]
        err_cnt += lang_mix_map[lang]
        rate = "%.2f" % (rate*100) + "%"
        avg_mix_len = "%.0f" % (np.average(lang_mix_length_map[lang]))
        print(lang_name_map[lang] + "\t" + str(lang_all_map[lang]) + "\t" + str(lang_mix_map[lang]) + "\t" + str(rate) + "\t" + str(avg_mix_len))
    avg_err_rate = "%.2f" % (100.0*err_cnt/all_cnt) + "%"
    mix_lens = [mix_len for key in lang_mix_length_map for mix_len in lang_mix_length_map[key]]
    avg_mix_len = "%.0f" % (sum(mix_lens) / len(mix_lens))

    print("平均" + "\t" + str(all_cnt) + "\t" + str(err_cnt) + "\t" + str(avg_err_rate) + "\t" + avg_mix_len)

if __name__ == "__main__":

    args = sys.argv
    result_path = args[1]

    multi_language_data_check(result_path)

    sys.exit(0)







