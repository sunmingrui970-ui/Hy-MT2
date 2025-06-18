import json
import random
import requests
import hashlib

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

def call_vllm_model(model, messages, temperature=0.7, **kwargs):
    headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer EMPTY"
            }
    payload = {
            "model": model,  # Use the provided model parameter
            'messages': messages,
            "stream": False,
            "temperature": temperature
            }
    api = "http://29.119.98.85:8081/v1/chat/completions"
    rsp = requests.post(api, json=payload, headers=headers, timeout=300)
    return rsp

def gen_pair_md5(_input, _output):
    data = _input + _output
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()

if __name__ == "__main__":
    messages = [{"role": "user", "content": "下面的文本中包含1次k这个数量单位，k在文本中的含义是千，提取出数量单位k及其前面的数字，然后结合上下文把提取文本翻译成中文，不要在翻译结果中增加提取文本中不存在的内容，如果存在多种翻译方式，请全部列举出来。输出json格式的结果，格式为[{\"提取文本\": \"提取的文本\", \"翻译结果\": [\"翻译1\", \"翻译2\", ...]\\}。\n\nThe annual revenue of the company reached 01234567k, showcasing significant growth in the past fiscal year."}]
    model = "deepseek_v3"
    rsp = call_vllm_model(model, messages).json()
    print(rsp)
    print(rsp["choices"][0]["message"]["content"])