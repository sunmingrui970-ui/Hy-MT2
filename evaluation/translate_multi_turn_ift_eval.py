import json
import random
import sys
import hashlib
import unicodedata

def gen_pair_md5(_input, _output):
    data = _input + _output
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()

def letter_cnt(text):
    letter_cnt = 0
    all_cnt = 0
    for c in text:
        # 剔除掉空格和换行之后
        if len(c.strip()) == 0:
            continue
        all_cnt += 1
        try:
            name = unicodedata.name(c)
            if "HIRAGANA" in name or "KATAKANA" in name or "CJK" in name or "LETTER" in name:
                letter_cnt += 1
        except:
            # print(c + "\t:error")
            continue

    return letter_cnt


def is_chinese_doc(text):
    letter_cnt = 0
    chinese_letter_cnt = 0
    japanese_letter_cnt = 0

    chinese_ranges = [(0x4E00, 0x9FFF)]
    japanese_ranges = [(0x3040, 0x309F), (0x30A0, 0x30FF), (0x4E00, 0x9FBF)]

    has_ko = False

    for c in text:
        try:
            name = unicodedata.name(c)
            # if "LETTER" in name or "CJK" in name or "HIRAGANA" in name or "KATAKANA" in name:
            if "HIRAGANA" in name or "KATAKANA" in name or "CJK" in name or "LETTER" in name or "CHARACTER" in name or 'HANGUL SYLLABLE' in name:
                letter_cnt += 1
                char_ord = ord(c)
                if 'HANGUL SYLLABLE' in name:
                    has_ko = True

                if any(lower <= char_ord <= upper for lower, upper in chinese_ranges):
                    chinese_letter_cnt += 1
                if any(lower <= char_ord <= upper for lower, upper in japanese_ranges):
                    japanese_letter_cnt += 1
        except:
            continue
    # print("letter_cnt:" + str(letter_cnt))
    # print("chinese_letter_cnt:" + str(chinese_letter_cnt))
    # print("japanese_letter_cnt:" + str(japanese_letter_cnt))

    # 无字符
    if letter_cnt == 0:
        return False
    # 有韩语
    if has_ko:
        return False
    # 无中文字符
    if chinese_letter_cnt == 0:
        return False
    if japanese_letter_cnt > chinese_letter_cnt:
        return False
    # print("chinese_rate:" + str(1.0*chinese_letter_cnt/letter_cnt))
    if 1.0*chinese_letter_cnt/letter_cnt > 0.3:
        return True
    return False

def is_all_chinese(text):
    letter_cnt = 0
    chinese_letter_cnt = 0

    chinese_ranges = [(0x4E00, 0x9FFF)]
    for c in text:
        try:
            name = unicodedata.name(c)
            if "LETTER" in name or "CJK" in name or "HIRAGANA" in name or "KATAKANA" in name:
                letter_cnt += 1
                char_ord = ord(c)
                if any(lower <= char_ord <= upper for lower, upper in chinese_ranges):
                    chinese_letter_cnt += 1

        except :
            continue

    # 无字符
    if letter_cnt == 0:
        return False
    # 无中文字符
    return letter_cnt == chinese_letter_cnt

import re
def is_chinese_sentence(sentence):
    # 正则表达式匹配中文字符的范围以及常见的中文标点符号
    pattern = r'^[\u4e00-\u9fa5，。？！；：‘’“”（）【】《》、]+?$'
    if re.match(pattern, sentence):
        return True
    else:
        return False


def is_contain_chinese_char(text):
    for char in text:
        try:
            name = unicodedata.name(char)
            if "CJK" in name:
                return True
        except:
            continue
    return False

def is_contain_english(text):
    return bool(re.search('[a-zA-Z]', text))

def is_english_sentence(sentence):
    pattern = re.compile(r'^[\w\s!@#$%^&*()-_=+[\]{}|;:\'",.<>/?]*$')
    return bool(re.match(pattern, sentence))

def ja_letter_cnt(text):
    japanese_ranges = [(0x3040, 0x309F), (0x30A0, 0x30FF), (0x4E00, 0x9FBF)]
    japanese_letter_cnt = 0
    for c in text:
        try:
            name = unicodedata.name(c)
            if "LETTER" in name or "CJK" in name or "HIRAGANA" in name or "KATAKANA" in name:
                char_ord = ord(c)
                if any(lower <= char_ord <= upper for lower, upper in japanese_ranges):
                    japanese_letter_cnt += 1
        except:
            continue
    return japanese_letter_cnt

def chinese_rate(text):
    letter_cnt = 0
    chinese_letter_cnt = 0

    chinese_ranges = [(0x4E00, 0x9FFF)]

    for c in text:
        try:
            name = unicodedata.name(c)
            if "LETTER" in name or "CJK" in name or "HIRAGANA" in name or "KATAKANA" in name or "CHARACTER" in name or 'HANGUL SYLLABLE' in name:
                letter_cnt += 1
                char_ord = ord(c)
                if any(lower <= char_ord <= upper for lower, upper in chinese_ranges):
                    chinese_letter_cnt += 1
        except :
            continue

    # 无字符
    if letter_cnt == 0:
        return -1
    return 1.0*chinese_letter_cnt/letter_cnt

import requests
def req_transmart_lang_dect(text):
    url = 'https://dev.transmart.qq.com/api/imt'
    data = {
        'header': {
            'fn': 'lang_detect',
            'user': 'aspirant',
            'token': 'f1pEQLS7A9NiWMOURMJi',
        },
        'text': text,
    }
    try_cnt_max = 1
    tyt_index = 0
    is_succeed = False
    while not is_succeed and tyt_index < try_cnt_max:
        tyt_index += 1
        try:
            response = requests.post(url, json=data)
            res1 = response.text
            res = json.loads(res1)
            # res = response.json
            # print(res)
            is_succeed = True
        except Exception as ex:
            print("error:" + str(ex))
    if is_succeed:
        return res
    else:
        return {}

def checklist_check(path):
    error_cnt = 0
    all_cnt = 0
    for line in open(path).readlines():
        j = json.loads(line)
        if "hunyuan_output" in j:
            answer = j["hunyuan_output"]
        elif "answer" in j:
            answer = j["answer"]
        elif "output" in j:
            answer = j["output"]
        elif "response" in j:
            answer = j["response"]
        #if answer == "" and "messages" in j:
        #    answer = j["messages"][-1]["content"][-1]["value"]
        if answer.strip() == "":
            continue
        #text = j['origin_text']
        if "origin_text" in j:
            text = j['origin_text']
        else:
            text = j['messages'][0]['content']

        all_cnt += 1

        if "抱歉" in answer or "对不起" in answer or "无法" in answer:
            continue

        is_error = False

        # 输入输出完全一致，错误
        if text.strip() == answer.strip():
            # print("error0")
            is_error = True

        # 输入和输出都不是中文
        if not is_contain_chinese_char(text) and  not is_contain_chinese_char(answer):
            is_error = True

        # 都是中文，但是文本很相近，可以认为没有翻译
        if is_chinese_doc(text) and is_chinese_doc(answer) and abs(len(text) - len(answer)) < 10:
            is_error = True

        # 输入的中文占比很少，但是输出是纯英文
        if is_contain_chinese_char(text) and chinese_rate(text) < 0.1 and not is_contain_chinese_char(answer):
            # print("error2")
            is_error = True

        # 输入是中文，但是输出不包含英文
        if is_chinese_doc(text) and not is_contain_english(text) and not is_contain_english(answer) and abs(len(text) - len(answer)) < 20:
            is_error = True

        # 输入包含英文，输出全是中文，没有问题
        if is_error and is_contain_english(text) and is_all_chinese(answer):
            is_error = False


        if is_error:
            if 'last_input' in j:
                print(j['last_input'])
            else:
                print(text)
            print(answer)
            print("******")
            error_cnt += 1

    error_rate = "%.2f" % (error_cnt*1.0/all_cnt*100)
    res = str(error_cnt) + "/" + str(all_cnt) + "=" + error_rate + "%"
    print(res)

if __name__ == "__main__":
    args = sys.argv
    result_path = args[1]

    checklist_check(result_path)

    print("done")

