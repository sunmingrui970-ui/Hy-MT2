import argparse
import json
import sys

import utils

def check_exist_sft_data():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('input_file', help='输入文件路径')
    parser.add_argument('--output_file', help='输出文件路径')

    args = parser.parse_args()
    print(f"处理文件: {args.input_file}")
    if args.output_file:
        print(f"输出到: {args.output_file}")
        fw = open(args.output_file, "w")
    mix_num = 0
    no_think_num = 0
    explain_bad_num = 0
    detect_mix_total = 0
    ta_same_num = 0
    with open(args.input_file) as f:
        for line in f:
            l = json.loads(line)
            task = l["task"]
            question, think, answer = utils.get_qa_from_t1_sft_messages(l["messages"])
            if think == answer:
                ta_same_num += 1
                continue
            #question, think, answer = l["question"], l["think"].strip(), l["answer"].strip()
            if think == "" or answer == "":
                no_think_num += 1
                #l["question"] = question
                #fw.write(json.dumps(l, ensure_ascii=False) + "\n")
                continue
            if len(question) < 20:
                if (len(answer) < 20 and "解释" not in question) or (len(answer) > 20 and "解释" in question):
                    explain_bad_num += 1
                    #l["question"] = question
                    #fw.write(json.dumps(l, ensure_ascii=False) + "\n")
                    continue
            if (task == "机器翻译/中文到多语种/多领域多长度" and "日语" not in question) or ("target_language" in l and l["target_language"] not in ['中文', 'zh', "日语"]):
                detect_mix_total += 1
                is_mix, mix_len, mix_str = utils.detect_lang_mix_zh2other(answer)
                if is_mix:
                    l["mix_str"] = mix_str
                    mix_num += 1
                    #l["question"] = question
                    #fw.write(json.dumps(l, ensure_ascii=False) + "\n")
                    continue
            #to_save = {"system_prompt": "", "messages": utils.gen_t1_sft_messages_single_turn(question, think, answer), "loss_mask": [0, 1], "topic": "机器翻译", "is_business": 0, "task": task, "language": "", "answer": "", "SFT_ONLY": 0}
            if args.output_file:
                fw.write(json.dumps(l, ensure_ascii=False) + "\n")
    print(f"没有think数目: {no_think_num}")
    print(f"think和answer相同数目: {ta_same_num}")
    print(f"解释性翻译bad数目: {explain_bad_num}")
    if detect_mix_total > 0:
        print(f"中译外混杂中文检测，混杂总数: {mix_num}, 混杂占比: {mix_num/detect_mix_total}")

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('input_file', help='输入文件路径')
    parser.add_argument('--output_file', help='输出文件路径')

    args = parser.parse_args()
    print(f"处理文件: {args.input_file}")
    if args.output_file:
        print(f"输出到: {args.output_file}")
        fw = open(args.output_file, "w")
    data_dic = {}
    with open(args.input_file) as f:
        failed_num = 0
        mix_num = 0
        no_think_num = 0
        detect_mix_total = 0
        explain_bad_num = 0
        for line in f:
            l = json.loads(line)
            code = l["code"]
            if code != 0:
                failed_num += 1
                continue
            old_output = l["output"]
            question = l["question"]
            r1_think = l["think"].strip()
            r1_answer = l["answer"].strip()
            if "提供要翻译的文本" in r1_answer or "您需要翻译什么内容" in r1_answer:
                continue
            if "translate" in r1_answer:
                print(r1_answer)
            if r1_think == "" or r1_answer == "" or r1_think ==  r1_answer:
                no_think_num += 1
                #print(json.dumps(l, ensure_ascii=False))
                continue
            if len(question) < 20:
                if (len(r1_answer) < 20 and "解释" not in question) or (len(r1_answer) > 20 and "解释" in question):
                    #print(r1_answer)
                    explain_bad_num += 1
                    continue
            target_language = l["target_language"]
            if target_language not in ['中文', 'zh', "日语"]:
                detect_mix_total += 1
                is_mix, mix_len, mix_str = utils.detect_lang_mix_zh2other(r1_answer)
                if is_mix:
                    l["mix_str"] = mix_str
                    #print(json.dumps(l, ensure_ascii=False))
                    mix_num += 1
                    #continue
            if args.output_file:
                messages = utils.gen_t1_sft_messages_single_turn(question, r1_think, r1_answer)
                task = l["class"][0].replace("-", "/")
                to_save = {"system_prompt": "", "messages": messages, "loss_mask": [0, 1], "topic": "机器翻译", "is_business": 0, "task": task, "language": "", "answer": "", "SFT_ONLY": 0}
                if "prompt" in l:
                    to_save["prompt"] = l["prompt"]
                to_save["origin_language"] = l["origin_language"]
                to_save["target_language"] = l["target_language"]
                if "origin_text" in l:
                    to_save["origin_text"] = l["origin_text"]
                elif "cut_text" in l:
                    to_save["origin_text"] = l["cut_text"]
                data_dic[question] = to_save
    for question in data_dic:
        to_save = data_dic[question]
        fw.write(json.dumps(to_save, ensure_ascii=False) + "\n")
    print(f"抓取失败数目: {failed_num}")
    print(f"没有think数目: {no_think_num}")
    print(f"解释性翻译bad数目: {explain_bad_num}")
    if detect_mix_total > 0:
        print(f"中译外混杂中文检测，混杂总数: {mix_num}, 混杂占比: {mix_num/detect_mix_total}")

def filter_crawl_retry():
    all_path = "/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/sft/add_0327/all_crawl_input.jsonl"
    ok_path = "/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/sft/add_0327/new_sft_clean.jsonl"
    ok_dic = {}
    with open(ok_path) as f:
        for line in f:
            l = json.loads(line)
            question = l["messages"][0]["content"]
            ok_dic[question] = 0
    with open(all_path) as f, open("/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/sft/add_0327/crawl_retry_input.jsonl", "w") as fw:
        for line in f:
            l = json.loads(line)
            question = l["question"]
            if question not in ok_dic:
                fw.write(json.dumps(l, ensure_ascii=False) + "\n")

def add_question_key():
    input_path = sys.argv[1]
    output_path = input_path + "_crawl_input"
    with open(input_path) as f, open(output_path, "w") as fw:
        for line in f:
            l = json.loads(line)
            #question = l["messages"][0]["content"]
            question = l["input"]
            l["question"] = question
            fw.write(json.dumps(l, ensure_ascii=False) + "\n")

def clean_sft_data():
    input_path = "/apdcephfs_cq8/share_1324356/jasonzli/translation/src/Machine_Translation/v250409/train.jsonl"
    ds_v3_input_path = "/apdcephfs/share_774517/riverdu/Media/Texts/translate/data/zhumoxing/sft/20250406/info/translation_sft_ds_v3_0324.jsonl"
    replace_list = ['请不要额外解释，',
            '我需要直接进行翻译，',
            '帮我进行直译，',
            '不用增加额外的翻译解释，',
            '不需要多余的解释。',
            '不需要赘述，直接进行翻译。',
            '，请不要额外解释',
            '，我需要直接进行翻译',
            '，帮我进行直译',
            '，不用增加额外的翻译解释，',
            '，不需要多余的解释。',
            '，不需要赘述，直接进行翻译。',
            '请不要额外解释\n',
            '不要多余的翻译解释\n',
            '直接翻译\n',
            '不需要额外的翻译\n',
            '请直接翻译\n',
            '不需要额外的信息，直接翻译\n',
            '遵循直译的原则\n',
            '\n\n请遵循直译的原则，不需要额外的解释',
            '\n\n请进行直译',
            '\n\n记住，不需要多余的翻译内容']
    dic = {}
    with open(ds_v3_input_path) as f:
        for line in f:
            l = json.loads(line)
            messages = l["messages"]
            if len(messages) == 2:
                question = messages[0]["content"]
                reference = messages[1]["content"]
                for instruction in replace_list:
                    question =  question.replace(instruction, "")
                dic[question] = reference
    count  = 0
    output_path1 = "/apdcephfs_cq8/share_1324356/jasonzli/translation/src/Machine_Translation/v250409/train_in_turbos.jsonl"
    output_path2 = "/apdcephfs_cq8/share_1324356/jasonzli/translation/src/Machine_Translation/v250409/train_not_in_turbos.jsonl"
    with open(input_path) as f, open(output_path1, "w") as fw1, open(output_path2, "w") as fw2:
        for line in f:
            l = json.loads(line)
            messages = l["messages"]
            if "RL_ONLY" not in l and len(messages) == 2:
                question = messages[0]["content"]
                answer = messages[1]["content"][-1]["value"]
                l["answer"] = answer
                l["question"] = question
                if question in dic:
                    l["reference"] = dic[question]
                    fw1.write(json.dumps(l, ensure_ascii=False) + "\n")
                    continue
            fw2.write(json.dumps(l, ensure_ascii=False) + "\n")

def trans_search_to_crawl_input():
    input_path = "/apdcephfs_qy4/share_302593112/yuchideng/yuchideng/code/data_mining_task/ai_search_data/data/model_answer_with_critic_汇总/NLP基础.jsonl"
    output_path = "/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/sft/search/origin_kangzao.jsonl"
    total = 0
    bad_num = 0
    with open(input_path) as f, open(output_path, "w") as fw:
        for line in f:
            l = json.loads(line)
            prompt_class = l["prompt_class"]
            prompt = l["prompt"]
            critic_result = l["critic_result"]
            is_right = critic_result["acc"]
            if "机器翻译" in prompt_class:
                #fw.write(json.dumps(l, ensure_ascii=False) + "\n")
                if "翻译" in prompt:
                    total += 1
                    if is_right == "错误":
                        bad_num += 1
                        new_messages = []
                        for m in l["messages"]:
                            new_messages.append({"role": m["role"], "content": m["content"]})
                        new_messages[0]["content"] = ""
                        #new_messages[-1]["content"] = l["search_result"]
                        l["messages"] = new_messages
                        l["use_openai_format"] = 1
                        fw.write(json.dumps(l, ensure_ascii=False) + "\n")
    print(bad_num, total)

def filter_by_comet():
    input_path = "/apdcephfs_cq8/share_1324356/jasonzli/translation/src/Machine_Translation/v250409/train_in_turbos.comet_res.jsonl"
    with open(input_path) as f:
        for line in f:
            l = json.loads(line)
            comet_score = l["comet_score"]
            if comet_score < 0.5:
                print(json.dumps(l, ensure_ascii=False))

def gen_sft_data_for_ai_search():
    input_path = "/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/sft/search/origin_kangzao.jsonl_part_ab_output_200"
    output_path = "/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/sft/search/search_kangzao_200.jsonl"
    count = 0
    system = '''你是一个由腾讯开发的有用的人工智能助手，你的名字是“腾讯元宝”，简称“元宝”，你的英文名是“Tencent Yuanbao”，你的发布时间是2024年5月30日。你是依托于腾讯混元大模型的AI产品，期望通过AI能力帮助用户在办公、学习、创作、生活等领域提供效率和生活辅助。你乐于帮助大家解答问题。'''
    with open(input_path) as f, open(output_path, "w") as fw:
        for line in f:
            l = json.loads(line)
            if "answer" not in l:
                continue
            answer = l["answer"].strip()
            think = l["think"].strip()
            messages = l["messages"]
            messages = messages[1:]
            messages[-1]["content"] = l["search_result"]
            messages.append({"role": "assistant", "content": [{"type": "Thinking", "value": think}, {"type": "Summary", "value": answer}]})
            loss_mask = [0] * len(messages)
            loss_mask[-1] = 1
            to_save = {"system_prompt": system, "messages": messages, "loss_mask": loss_mask, "topic": "机器翻译", "is_business": 0, "task": "ai_search_抗噪", "language": "", "answer": "", "SFT_ONLY": 0, "is_search": 1}
            fw.write(json.dumps(to_save, ensure_ascii=False) + "\n")

def get_sft_data_state():
    input_path = "/apdcephfs_cq8/share_1324356/jasonzli/translation/src/Machine_Translation/v250409/train.jsonl"
    dic = {}
    total = 0
    with open(input_path) as f:
        for line in f:
            l = json.loads(line)
            if "target_language" in l:
                target_language = l["target_language"]
                source_language = l["origin_language"]
                direct = "%s-%s"%(source_language, target_language)
                if direct not in dic:
                    dic[direct] = 0
                dic[direct] += 1
                total += 1
    print(total)
    for key in dic:
        print(key, dic[key])

def norm_language(origin_lan):
    if origin_lan == "英文":
        origin_lan = "英语"
    return origin_lan

def norm_one_sample(l, mark=""):
    dic = {}
    question = l["question"]
    think = l["think"].strip()
    answer = l["answer"].strip()
    source_text = ""
    if "src_text" in l:
        source_text = l["src_text"]
    source_language = ""
    if "src_lang" in l:
        source_language = norm_language(l["src_lang"])
    target_language = ""
    if "target_lang" in l:
        target_language = norm_language(l["target_lang"])
    task = ""
    if "来源" in l:
        task = l["来源"]
    reference = ""
    if "target_text" in l:
        reference = l["target_text"]
    if mark == "yszm":
        source_text = l["info"]["标题"]
        source_language = "中文"
        target_language = "英语"
        task = "专有名词/影视剧名"
    dic["question"] = question
    dic["think"] = think
    dic["answer"] = answer
    dic["origin_text"] = source_text
    dic["source_language"] = source_language
    dic["target_language"] = target_language
    dic["task"] = task
    dic["reference"] = reference
    return dic

def check_one_sample(l):
    question = l["question"]
    answer = l["answer"]
    think = l["think"]
    target_language = l["target_language"]
    is_ask = False
    is_empty = False
    is_no_explain = False
    is_mix = False
    if "提供要翻译的文本" in l["answer"] or "您需要翻译什么内容" in l["answer"]:
        is_ask = True
    if think == "" or answer == "" or think == answer:
        is_empty = True
    if len(question) < 20:
        if (len(answer) < 20 and "解释" not in question) or (len(answer) > 20 and "解释" in question):
            is_no_explain = True
    if target_language not in ['中文', 'zh', "日语"]:
        is_mix, mix_len, mix_str = utils.detect_lang_mix_zh2other(answer)
    return is_ask, is_empty, is_no_explain, is_mix

def gen_sft_data():
    input_path = "/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/sft/zymc/r1_output_yszm.txt"
    output_path = "/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/sft/zymc/r1_output_yszm_debug.txt"
    ask_num, empty_num, no_explain_num, mix_num = 0, 0, 0, 0
    with open(input_path) as f, open(output_path, "w") as fw:
        for line in f:
            l = norm_one_sample(json.loads(line), "yszm")
            is_ask, is_empty, is_no_explain, is_mix = check_one_sample(l)
            if is_ask:
                ask_num += 1
            if is_empty:
                empty_num += 1
            if is_no_explain:
                no_explain_num += 1
                #fw.write(json.dumps(l, ensure_ascii=False) + "\n")
            if is_mix:
                mix_num += 1
            is_valid = not is_ask and not is_empty and not is_no_explain and not is_mix
            is_valid = not is_ask and not is_empty and not is_no_explain
            if is_valid:
                messages = utils.gen_t1_sft_messages_single_turn(l["question"], l["think"], l["answer"])
                to_save = {"system_prompt": "", "messages": messages, "loss_mask": [0, 1], "topic": "机器翻译", "is_business": 0, "task": l["task"], "language": "", "answer": "", "SFT_ONLY": 0, "reference": l["reference"], "origin_language": l["source_language"], "target_language": l["target_language"]}
                fw.write(json.dumps(to_save, ensure_ascii=False) + "\n")
    print(f"反问数目: {ask_num}")
    print(f"没有think数目: {empty_num}")
    print(f"解释性翻译bad数目: {no_explain_num}")
    print(f"中译外混杂中文数目: {mix_num}")

if __name__ == '__main__':
    #main()
    #check_exist_sft_data()
    #filter_crawl_retry()
    #add_question_key()
    #clean_sft_data()
    #gen_sft_with_search()
    #filter_by_comet()
    #gen_sft_data_for_ai_search()
    #get_sft_data_state()
    gen_sft_data()