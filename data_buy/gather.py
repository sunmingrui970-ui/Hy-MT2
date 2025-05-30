import sys
import json
import os
sys.path.append("..")
import utils
import random

lan_dic, lan_dic_reverse = utils.load_lan_dic()
lan_dic["filipino"] = "菲律宾语"
lan_dic["fil"] = "菲律宾语"
lan_dic["german"] = "德语"
lan_dic["hindi"] = "印地语"
lan_dic["indonesian"] = "印尼语"
lan_dic["hk"] = "香港中文繁体"
lan_dic["italian"] = "意大利语"
lan_dic["ph"] = "菲律宾语"
lan_dic["thai"] = "泰语"
lan_dic["turkish"] = "土耳其语"
lan_dic["vietnamese"] = "越南语"
lan_dic["vn"] = "越南语"
lan_dic["中文繁体"] = "香港中文繁体"

def sample_label_data():
    input_dir = "/apdcephfs_cq8/share_1324356/jasonzli/translation/data/data_buy/10国第二次/ft_local/10国第二次/all"

    data_dic = {}

    for file_name in os.listdir(input_dir):
        input_path = os.path.join(input_dir, file_name)
        with open(input_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    l = json.loads(line.strip())
                except:
                    continue
                language = l["language"].strip().lower()
                lan_str = ""
                if "-" in language:
                    lan_str = language.split("-")[1]
                else:
                    lan_str = lan_dic[language]

                input_text = l["input"].strip()
                output = l["output"].strip()

                domain = l["info"]["domain"]

                input = "将以下文本翻译成%s， 不要额外解释：\n%s"%(lan_str, input_text)
                to_save = {"question": input, "output": output, "language": lan_str, "origin_text": input_text, "domain": domain}
                if file_name not in data_dic:
                    data_dic[file_name] = []
                data_dic[file_name].append(to_save)

    output_path = "/apdcephfs_cq8/share_1324356/jasonzli/translation/data/data_buy/10国第二次/sample_to_label.jsonl"
    with open(output_path, "w", encoding="utf-8") as fw:
        for file_name in data_dic:
            random.shuffle(data_dic[file_name])
            for item in data_dic[file_name][:500]:
                item["file_name"] = file_name
                fw.write(json.dumps(item, ensure_ascii=False) + "\n")

def compare_by_comet():
    input_path = "/apdcephfs_cq8/share_1324356/jasonzli/translation/data/data_buy/10国第二次/ds_v3_output_cometkiwi.jsonl"
    dic = {}
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            l = json.loads(line.strip())
            buy_cometkiwi = l["output_cometkiwi"]
            ds_cometkiwi = l["answer_cometkiwi"]
            file_name = l["file_name"]
            language = l["language"]
            if file_name not in dic:
                dic[file_name] = {}
            if language not in dic[file_name]:
                dic[file_name][language] = {"buy": [], "ds": []}
            dic[file_name][language]["buy"].append(buy_cometkiwi)
            dic[file_name][language]["ds"].append(ds_cometkiwi)
    to_print = []
    for file_name in dic:
        total = 0
        total_ds_score = 0
        total_buy_score = 0
        for language in dic[file_name]:
            lan_len = len(dic[file_name][language]["buy"])
            lan_ds_sum = sum(dic[file_name][language]["ds"])
            lan_buy_sum = sum(dic[file_name][language]["buy"])
            total += lan_len
            total_ds_score += lan_ds_sum
            total_buy_score += lan_buy_sum
            to_print = [file_name, language, str(lan_len), str(round(lan_ds_sum/lan_len, 3)), str(round(lan_buy_sum/lan_len, 3))]
            print("\t".join(to_print))
        to_print = [file_name, "ALL", str(total), str(round(total_ds_score/total, 3)), str(round(total_buy_score/total, 3))]
        print("\t".join(to_print))
        print("-------------------------------")

def main():
    compare_by_comet()

if __name__ == "__main__":
    main()