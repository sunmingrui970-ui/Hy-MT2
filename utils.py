import json
import random

def load_instruction_list():
    instruction_list = []
    with open("/apdcephfs_cq8/share_1324356/jasonzli/translation/data/机器翻译prompt.jsonl") as f:
        for line in f:
            l = json.loads(line)
            sheet_name = l["sheet_name"]
            if sheet_name != "机器翻译-通用" and sheet_name != "机器翻译-复杂指令":
                continue
            instruction = l["instruction"]
            instruction_list.append(instruction)
    return instruction_list

def random_concat_instruction(instruction_list, source_text, source_language, target_language):
    instruction = random.choice(instruction_list)
    input = instruction.replace("{{{text}}}", source_text).replace("{{{target_lang}}}", target_language).replace("{{{origin_lang}}}", source_language)
    return input

def load_lan_dic():
    lan_dic = {"en": "英语", "fr": "法语", "pt": "葡萄牙语", "es": "西班牙语", "ja": "日语", "tr": "土耳其语", "ru": "俄语", "ar": "阿拉伯语", "ko": "韩语", "th": "泰语", "it": "意大利语", "de": "德语", "vi": "越南语", "ms": "马来语", "id": "印尼语", "zh": "中文", "tl": "菲律宾语", "hi": "印地语", "zh-Hant": "中文繁体", "yue": "粤语", "mix": "混杂", "bo": "藏语", "kk": "哈萨克语", "mn": "蒙古语", "ug": "维吾尔语"}

    lan_dic_reverse = {}
    for lan in lan_dic:
        lan_dic_reverse[lan_dic[lan]] = lan

    return lan_dic, lan_dic_reverse