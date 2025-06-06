import json
import threading
import queue
import time
import re
import os
import sys
from concurrent.futures import ThreadPoolExecutor
import requests  # 用于HTTP请求
import uuid

lang_dict = {"俄语": "ru",
"印尼语": "id",
"土耳其语": "tr",
"德语": "de",
"意大利语": "it",
"日语": "ja",
"法语": "fr",
"泰语": "th",
"英语": "en",
"葡萄牙语": "pt",
"西班牙语": "es",
"越南语": "vi",
"阿拉伯语": "ar",
"韩语": "ko",
"马来语": "ms",
"中文": "zh"}

def extract_short_answer(model_response):
    #global_pattern = re.compile(r"<answer>.*?\\boxed{(.*)}.*?</answer>", re.DOTALL)
    global_pattern = re.compile(r"<answer>(.*?)</answer>", re.DOTALL)
    matches = re.findall(global_pattern, model_response)
    final_answer = ""
    if matches is not None and type(matches) == list and len(matches) >= 1:
        final_answer = matches[-1].strip()
    return final_answer


def request_xcomet_single(src, mt, ref):
    url = 'http://gateway.botong.woa.com/translation_xcomet'
    headers = { 
        "Content-Type": "application/json",
        "Authorization": "Bearer 7auGXNATFSKl7dF",
        'business-id': 'm988lav0wc1vkrmvms'
    }

    json_data = { 
        "model": "any",
        "messages": [
            {   
                "role": "user",
                "content": json.dumps({"src": src, "mt": mt, "ref": ref}, ensure_ascii=False)
            }   
        ]   
    }
    resp = requests.post(url, headers=headers, json=json_data, stream=True).json()
    score = json.loads(resp['choices'][0]['message']['content'])['final_score']
    return score

def postprocess_output(answer, ref_answer, origin_language, target_language):
    answer = answer.strip("<|startoftext|>").strip()
    #answer = answer.split("\n")[0].strip().split("英语：")[0].split("中文：")[0].split("英文：")[0]
    answer = re.split('%s:|%s:|%s：|%s：|英文：｜英文:'%(origin_language, target_language, origin_language, target_language), answer)[0]
    if "\n" not in ref_answer:
        answer = answer.split("\n")[0]
    answer_msg = answer.split("<|startoftext|>")
    if answer_msg[0] == "":
        answer = answer.replace("<|startoftext|>", "").strip()
    else:
        answer = answer_msg[0].strip()
    #if len(answer) > len(ref_answer) + 10:
    #    answer = answer[:len(ref_answer)]
    return answer

def request_hunyuan_model(model_name, wsid, messages, stop=[]):
    url = "http://stream-server-online-openapi.turbotke.production.polaris:81/openapi/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 7auGXNATFSKl7dF",
        "Wsid": wsid,
    }

    json_data = {
        "model": model_name,
        "query_id": "test_query_id_" + str(uuid.uuid4()),
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.6,
        "top_k": 20,
        "repetition_penalty": 1.05,
        "output_seq_len": 2048,
        "max_input_seq_len": 2048,
        "stream": False,
        "stop": stop
    }
    resp = requests.post(url, headers=headers, json=json_data, stream=False)
    #print(resp)
    for i in range(3): # retry 3 times
        if resp.status_code == 200:
            break
        else:
            time.sleep(1)
            resp = requests.post(url, headers=headers, json=json_data, stream=False)
    if resp.status_code == 200:
        content = resp.json()['choices'][0]['message']['content']
    else:
        print("Error: ", resp.status_code, resp.text)
        content = ""
    return content

def request_hy_pretrain(data):
    model_name = "HY-7B-Dense-Pretrain-256k-v2-250327"
    wsid = "10316"
    messages = [{"role": "system", "content": ""}, {"role": "user", "content": data["question"]}]
    source_lang = data["question"].split(":")[0].strip()
    stop = ["%s:"%(source_lang), "%s："%(source_lang)]
    response = request_hunyuan_model(model_name, wsid, messages, stop=stop)
    return response

def pretrain_res_to_xcomet(data):
    ref = data["input"]["correct_res"]
    mt = postprocess_output(data["response"], ref, data["input"]["origin_language"], data["input"]["target_language"])
    src = data["input"]["origin_text"]
    response = request_xcomet_single(src, mt, ref)
    return response

def request_hy_sft_for_eval(data):
    model_name = "2B-Dense-Translation-SFT-8k-250214-jason"
    #model_name = "translate_dpo_7b_dense_v30_0214_fp8"
    #model_name = "translate_7b_moe_dpo_v30_20250217_jason"
    #model_name = "translate_dpo_v29"
    #model_name = "translate_7b_moe_sft_0109"
    #model_name = "translate_7b_moe_dpo_v32_20250605"
    wsid = "10316"
    if "messages" in data:
        messages = data["messages"]
    else:
        #messages = [{"role": "system", "content": "你是一个资深的语言翻译专家"}, {"role": "user", "content": data["question"]}]
        messages = [{"role": "system", "content": ""}, {"role": "user", "content": data["question"]}]
    response = request_hunyuan_model(model_name, wsid, messages)
    return response

class Counter:
    """线程安全的计数器"""
    def __init__(self):
        self.value = 0
        self.failures = 0
        self.start_time = 0
        self.end_time = 0
        self.lock = threading.Lock()

def worker(data, result_queue, counter):
    """处理单个数据项的worker函数"""
    try:
        data = json.loads(data)
        #response = request_hy_pretrain(data)
        #response = pretrain_res_to_xcomet(data)
        response = request_hy_sft_for_eval(data)
        #comet = request_xcomet_single(data["origin_text"], data["response"], data["correct_res"])

        result = data
        result["response"] = response
        result["success"] = True

    except Exception as e:
        result = data
        result["response"] = response
        result["success"] = False
        result["error"] = str(e)
        with counter.lock:
            counter.failures += 1
    finally:
        result_queue.put(result)
        with counter.lock:
            counter.value += 1
            counter.end_time = time.time()

def writer(output_file, result_queue):
    """文件写入线程"""
    with open(output_file, 'a', encoding='utf-8') as f:
        while True:
            result = result_queue.get()
            if result is None:  # 结束信号
                break
            f.write(json.dumps(result, ensure_ascii=False) + '\n')
            f.flush()  # 确保及时写入磁盘

def reporter(counter):
    """统计报告线程"""
    while True:
        time.sleep(1)
        with counter.lock:
            current_total = counter.value
            current_failures = counter.failures
            current_endtime = counter.end_time
            current_starttime = counter.start_time
        time_cost = (current_endtime - current_starttime)
        qps = current_total / time_cost

        print(f"[STAT] Total: {current_total}, TimeCost: {time_cost/60} minuts, QPS: {qps}/s, Total Failures: {current_failures}")

def main(input_file, output_file, max_workers=10):
    # 读取输入数据
    with open(input_file, 'r') as f:
        data_list = [line.strip() for line in f]
    os.system("rm %s"%(output_file))
    # 初始化共享对象
    result_queue = queue.Queue()
    counter = Counter()
    counter.start_time = time.time()
    # 启动写入线程
    writer_thread = threading.Thread(
        target=writer,
        args=(output_file, result_queue)
    )
    writer_thread.start()

    # 启动统计线程
    reporter_thread = threading.Thread(
        target=reporter,
        args=(counter,)
    )
    reporter_thread.daemon = True
    reporter_thread.start()

    # 使用线程池处理任务
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        futures = [executor.submit(worker, data, result_queue, counter) 
                  for data in data_list]
        
        # 等待所有任务完成
        for future in futures:
            future.result()

    # 结束写入线程
    result_queue.put(None)
    writer_thread.join()

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)
    main(
        input_file=sys.argv[1],
        output_file=sys.argv[2],
        max_workers=20  # 根据实际情况调整并发数
    )
    """
    #print(request_xcomet_single("a", "a", "a"))

    test_data_path = "/apdcephfs_cq8/share_1324356/jasonzli/translation/data/test/multi_language_translate_text_with_ref_all_no_long.jsonl"
    test_data_few_shot_path = "/apdcephfs_cq8/share_1324356/jasonzli/translation/data/test/multi_language_translate_text_with_ref_all_no_long.fewshot_v2.jsonl"
    model_name = "HY-7B-Dense-Pretrain-256k-v2-250327"
    wsid = "10316"
    print(request_hunyuan_model(model_name, wsid, [{"role": "system", "content": ""}, {"role": "user", "content": '''英语：In New Jersey, smokers can receive the vaccine before teachers do — and proof that you're a smoker is not required. In New York, psychologists and psychiatrists can get the vaccine along with essential workers.
中文：在新泽西州，吸烟人士排在教师之前接种疫苗，而且无须提供证明。在纽约州，心理学家和精神病学家可以和必要岗位的工作人员一起接种疫苗。
英语：Li has pulled off the move before at competitions, including at the 2017 Asian championships.
中文：李发彬在之前的比赛中也展示过这个动作，其中就包括2017年的亚洲举重锦标赛。
英语：Results from the study found that teachers of students with severe disabilities utilize and find observations of students in the special education classroom as the most important assessment method.
中文：研究结果表明，严重残疾学生的教师对特殊教育教室中的学生进行观察，将此作为最重要的评估方法。
英语：Lymph nodes, key components of our immune system, contain more immune cells that recognize the antigens in vaccines and start the immune process of creating antibodies.
中文：作为人体免疫系统的关键组成部分，淋巴结所含的免疫细胞更多，这些免疫细胞能够识别疫苗中的抗原，从而启动制造抗体的免疫程序。
英语：The 4th session of the 13th National People’s Congress (NPC) of China held recently made a decision to improve Hong Kong’s electoral system. The purpose is to provide an institutional guarantee for the principle of “patriots governing Hong Kong”, and ultimately for the long-term implementation of “one country, two systems”. To gain an accurate understanding, let me share with you the following perspectives.
中文：'''}], stop=["英语：", "英语:"]))
    """