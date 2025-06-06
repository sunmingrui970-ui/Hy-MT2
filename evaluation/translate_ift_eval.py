# encoding: utf-8
import json
import os
import sys

def is_contain_chinese(text):
    import re
    RE = re.compile(u'[⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]', re.UNICODE)
    return bool(RE.search(text)) # 判断是否包含中文

def ift_error_rate(result_path):

    all_cnt = 0
    error_cnt = 0
    for line in open(result_path).readlines():
        j = json.loads(line)
        if "原始语言" in j:
            origin_lang = j["原始语言"]
        else:
            origin_lang = j["origin_lang"]

        if "hunyuan_output" in j:
            answer = j["hunyuan_output"]
        elif "answer" in j:
            answer = j["answer"]
        elif "output" in j:
            answer = j["output"]
        elif "response" in j:
            answer = j["response"]

        # 调用失败的情况下先不算badcase
        if answer.strip() == "":
            print("结果为空")
            continue

        all_cnt += 1

        is_error = False
        if origin_lang == "中文" and is_contain_chinese(answer):
            is_error = True
        elif origin_lang != "中文" and not is_contain_chinese(answer):
            is_error = True

        if is_error:
            error_cnt += 1

    print("all_cnt:" + str(all_cnt))
    print("error_cnt:" + str(error_cnt))
    print("error_rate:" + str(1.0*error_cnt/all_cnt))

if __name__ == "__main__":

    args = sys.argv
    result_path = args[1]

    ift_error_rate(result_path)




