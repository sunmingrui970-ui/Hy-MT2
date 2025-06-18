import json
from tqdm import tqdm
import os
import random

def load_cometkiwi():
    from comet import load_from_checkpoint
    model_path = "/apdcephfs_gy2/share_303033943/hunyuan/jasonzli/model_zoo/wmt23-cometkiwi-da-xxl/checkpoints/model.ckpt"
    model_path = "/apdcephfs_gy2/share_303033943/hunyuan/jasonzli/model_zoo/wmt23-cometkiwi-da-xl/checkpoints/model.ckpt"
    model = load_from_checkpoint(model_path)
    return model

def load_xcomet():
    from comet import load_from_checkpoint
    model_path = "/apdcephfs_gy2/share_303033943/hunyuan/jasonzli/model_zoo/XCOMET-XXL/checkpoints/model.ckpt"
    model = load_from_checkpoint(model_path)
    return model

def load_data(input_path):
    data = []
    with open(input_path) as f:
        for line in f:
            l = json.loads(line)
            data.append(l)
    return data

def build_input_data(data, src_key, mt_key):
    input_data = []
    for item in data:
        src = item[src_key]
        mt = item[mt_key]
        input_data.append({"src": src, "mt": mt})
    return input_data

def build_input_data_with_ref(data, src_key, mt_key, ref_key):
    input_data = []
    for item in data:
        src = item[src_key]
        mt = item[mt_key]
        ref = item[ref_key]
        input_data.append({"src": src, "mt": mt, "ref": ref})
    return input_data

def main():
    batch_size = 48
    GPU_NUM = 4
    model = load_cometkiwi()
    input_path = "/apdcephfs_cq8/share_1324356/jasonzli/translation/data/wmt24/crawl_input/output_gpt4.jsonl"
    data = load_data(input_path)
    output_path = "/apdcephfs_cq8/share_1324356/jasonzli/translation/data/wmt24/crawl_input/output_gpt4_cometkiwi.jsonl"
    fw = open(output_path, "w")
    src_key = "origin_text"
    mt_key = "model_res"
    input_data = build_input_data(data, src_key, mt_key)
    model_output = model.predict(input_data, batch_size, gpus=GPU_NUM)
    scores = model_output.scores
    for item, score in zip(data, scores):
        item["%s_cometkiwi"%(mt_key)] = score
        fw.write(json.dumps(item, ensure_ascii=False) + "\n")
    fw.close()
    print(f"CometKiwi scores saved to {output_path}")
    print(f"CometKiwi system score: {model_output.system_score}")
    print("CometKiwi evaluation completed.")
    
if __name__ == "__main__":
    main()
