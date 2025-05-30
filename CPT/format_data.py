import json
import sys
import os
from bs4 import BeautifulSoup
import hashlib
sys.path.append("..")
import utils
import trace

def parse_news_data(input_dir):
    file_name_list = os.listdir(input_dir)
    save_path = os.path.join(input_dir, "parsed_news_data.jsonl")
    fw = open(save_path, 'w', encoding='utf-8')
    for file_name in file_name_list:
        if not file_name.startswith("news_") and not file_name.endswith(".jsonl"):
            continue
        file_path = os.path.join(input_dir, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if "CONTENT" in data and "TITLE" in data:
                        content = data["CONTENT"]
                        title = data["TITLE"]
                        soup = BeautifulSoup(content, 'html.parser')
                        text_content = soup.get_text()
                        id = hashlib.md5((title + text_content).encode('utf-8')).hexdigest()
                        #print(f"Title: {title}\nContent: {text_content}\n")
                        to_save = {"id":id, "title": title, "text": text_content, "language": "th", "ori": "news"}
                        fw.write(json.dumps(to_save, ensure_ascii=False) + "\n")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {file_path}")
                    continue
    fw.close()

def parse_subtitle_data(input_dir):
    def get_text(origin_text):
        text = ""
        for item in origin_text.split("\n\n"):
            text += " " + item.split("\n")[-1]
        return text.strip()

    instruction_list = utils.load_instruction_list()
    lan_dic, lan_dic_reverse = utils.load_lan_dic()

    file_name_list = os.listdir(input_dir)
    save_path = os.path.join(input_dir, "parsed_subtitle_data.jsonl")
    fw = open(save_path, 'w', encoding='utf-8')
    for file_name in file_name_list:
        if not file_name.startswith("subtitle_") or not file_name.endswith(".jsonl"):
            continue
        file_path = os.path.join(input_dir, file_name)
        print(file_path)
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    input = get_text(data["input"])
                    output = get_text(data["output"])
                    source_language = data["source_language"].split("-")[0]
                    target_language = data["target_language"].split("-")[0]
                    language = target_language if target_language not in ["zh", "en"] else source_language
                    id = hashlib.md5((input + output).encode('utf-8')).hexdigest()
                    #print(f"Title: {title}\nContent: {text_content}\n")
                    if input == "":
                        language = target_language
                        to_save = {"id":id, "text": output, "language": language, "ori": "subtitle"}
                    else:
                        input = utils.random_concat_instruction(instruction_list, input, lan_dic[source_language], lan_dic[target_language])
                        to_save = {"id":id, "input": input, "output": output, "language": language, "ori": "subtitle", "info": {"source_language": source_language, "target_language": target_language}}
                    fw.write(json.dumps(to_save, ensure_ascii=False) + "\n")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {file_path}")
                    continue

    fw.close()

def parse_minhan_data(input_dir):
    def norm_text(text):
        text = text.replace(" ", "").replace("@", "").strip("▁")
        return text
    instruction_list = utils.load_instruction_list()
    lan_dic, lan_dic_reverse = utils.load_lan_dic()

    file_name_list = os.listdir(input_dir)
    save_path = os.path.join(input_dir, "parsed_minhan_data.jsonl")
    fw = open(save_path, 'w', encoding='utf-8')
    for file_name in file_name_list:
        if not file_name.startswith("train.") or not file_name.endswith(".txt"):
            continue
        language = file_name.split(".")[1].split("-")[0]
        file_path = os.path.join(input_dir, file_name)
        print(file_path)
        encoding='utf-8'
        #if file_name == "train.kk-zh.txt":
        #    encoding = "gbk"
        with open(file_path, 'r', encoding=encoding) as f:
            try:
                for line in f:
                    try:
                        input, output = line.strip().split("\t")
                        input = norm_text(input)
                        output = norm_text(output)
                        source_language = language
                        target_language = "zh" 
                        input = utils.random_concat_instruction(instruction_list, input, lan_dic[source_language], lan_dic[target_language])
                        id = hashlib.md5((input + output).encode('utf-8')).hexdigest()
                        to_save = {"id":id, "input": input, "output": output, "language": language, "ori": "minhan", "info": {"source_language": source_language, "target_language": target_language}}
                        fw.write(json.dumps(to_save, ensure_ascii=False) + "\n")
                    except Exception as e:
                        print(e, file_path)
                        continue
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
    fw.close()

def main():
    input_dir = "/apdcephfs/share_774517/riverdu/Media/Texts/translate/data/minhan_data/ft_local/minhan_data"
    parse_minhan_data(input_dir)

if __name__ == "__main__":
    main()