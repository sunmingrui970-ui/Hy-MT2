import sys
import os
import json
import pandas as pd
import math

lan_dic = {"en": "英语", "fr": "法语", "pt": "葡萄牙语", "es": "西班牙语", "ja": "日语", "tr": "土耳其语", "ru": "俄语", "ar": "阿拉伯语", "ko": "韩语", "th": "泰语", "it": "意大利语", "de": "德语", "vi": "越南语", "ms": "马来语", "id": "印尼语", "zh": "中文", "tl": "菲律宾语", "hi": "印地语", "zh-Hant": "中文繁体", "yue": "粤语", "mix": "混杂"}

lan_dic_reverse = {}
for lan in lan_dic:
    lan_dic_reverse[lan_dic[lan]] = lan

if __name__ == '__main__':
    input_path = "翻译多语言数据资源汇总-预训练.xlsx"
    
    en_para_sample_total = 190
    en_single = {"2147/en": 15.76, "1829/final_clean_v1_quality2": 85}
    zh_single = {"1389/base_data": 49, "2400/quality_score_filter_v2.1_extsv1_rulev1.1_psv1_futsv1_toxicv1_wmv1_qav1.1_qafilterv1_10_part_cn_quality_0903_threshold_2": 50}
    #little_sample_total = 400

    df = pd.read_excel(input_path, sheet_name=None)
    lan2size = {}
    other_total = 0
    total = 0
    filter_data_id = ["8941", "12100", "8512", "11278"]
    for sheet_name in df:
        if sheet_name != "采样数据全集-new":
            continue
        sheet_data = df[sheet_name]
        for row_idx in range(len(sheet_data)):
            data_id = str(sheet_data["数据平台id"][row_idx])
            data_version = str(sheet_data["平台版本号"][row_idx])
            dd = data_version.split('/')
            data_suffix = "_".join(dd)
            data_key = data_id.strip() + "/" + data_suffix
            # 不使用某些数据
            if data_id in filter_data_id:
                continue
            is_para = sheet_data["是否平行语料"][row_idx]
            is_sample = sheet_data["采样是否指定语言"][row_idx]
            lan = sheet_data["归一化语言"][row_idx]

            
            if is_sample not in ["是", "否"] or lan not in lan_dic:
                continue
            size = sheet_data["数据量"][row_idx]
            if size.endswith("M"):
                size = float(size.replace("M", "").strip()) / 1000
            elif size.endswith("T"):
                size = float(size.replace("T", "").strip()) * 1000
            else:
                size = float(size.replace("G", "").strip())
            if lan not in lan2size:
                lan2size[lan] = {"para_size": 0, "single_size": 0,  "data_dic": {}}
            if data_key not in lan2size[lan]["data_dic"]:
                if is_para == "是":
                    lan2size[lan]["para_size"] += size
                else:
                    lan2size[lan]["single_size"] += size
                lan2size[lan]["data_dic"][data_key] = {"size":size, "is_para": is_para, "is_select_lan": is_sample}
    little_total = 0
    en_para_total = 0
    lan_size_dist = {}
    for lan in lan2size:
        if lan not in ["en", "zh", "zh-Hant", "yue"]:
            cur_lan_size = lan2size[lan]["para_size"] + lan2size[lan]["single_size"]
            lan_size_dist[lan] = cur_lan_size
            little_total += cur_lan_size
        elif lan == "en":
            en_para_total += lan2size[lan]["para_size"]
    for lan in lan_size_dist:
        lan_size_dist[lan] /= little_total
    sample_data_list = []
    sample_size_list = []
    sample_size_dic = {}
    sample_ratio_list = []
    sample_ratio_dic = {}
    sample_little_total = 0
    sample_total = 0
    for lan in lan2size:
        cur_total = lan2size[lan]["para_size"] + lan2size[lan]["single_size"]
        para_sample_total = 0
        single_sample_total = 0
        for data_key in lan2size[lan]["data_dic"]:
            is_para = lan2size[lan]["data_dic"][data_key]["is_para"]
            size = lan2size[lan]["data_dic"][data_key]["size"]
            is_sample = lan2size[lan]["data_dic"][data_key]["is_select_lan"]
            if lan == "en":
                if is_para == "是":
                    sample_size = round(size * en_para_sample_total / en_para_total, 3)
                    para_sample_total += sample_size
                else:
                    if data_key not in en_single:
                        continue
                    sample_size = en_single[data_key]
                    single_sample_total += sample_size
            elif lan == "zh":
                if data_key not in zh_single:
                    continue
                sample_size = zh_single[data_key]
                if is_para == "是":
                    para_sample_total += sample_size
                else:
                    single_sample_total += sample_size
            elif lan == "zh-Hant":
                sample_size = 50
                if is_para == "是":
                    para_sample_total += sample_size
                else:
                    single_sample_total += sample_size
            else:
                sample_size = int(size*1000) / 1000 # 小语种全部使用
                sample_little_total += sample_size
                if is_para == "是":
                    para_sample_total += sample_size
                else:
                    single_sample_total += sample_size
            sample_total += sample_size
            path = "${DATA_ID:5979"+ "}/cleaned_data/" + data_key
            if path not in sample_data_list:
                sample_data_list.append(path)
            #print(lan, data_key, size, sample_size) 
            data_path = f"5979/cleaned_data/{data_key}"
            need_beishu = 1
            if is_sample != "是":
                if sample_size > size:
                    need_beishu = math.ceil(1.0*sample_size/size)
                    print(lan, need_beishu)
            if data_path not in sample_ratio_dic:
                sample_ratio_dic[data_path] = need_beishu
            else:
                sample_ratio_dic[data_path] = max(sample_ratio_dic[data_path], need_beishu)
            #sample_ratio_list.append(data_path + "," + str(need_beishu))
            if data_path not in sample_size_dic:
                sample_size_dic[data_path] = {}
            if is_sample == "是":
                sample_size_dic[data_path][lan] = sample_size
            else:
                sample_size_dic[data_path]["default"] = sample_size
        print(lan, "TOTAL: ", round(lan2size[lan]["para_size"], 3), round(lan2size[lan]["single_size"], 3))
        print(lan, "SAMPLE: ", round(para_sample_total, 3), round(single_sample_total, 3))
    # res2构建
    for data_path_item in sample_ratio_dic.keys():
        res = data_path_item + "," + str(sample_ratio_dic[data_path_item])
        sample_ratio_list.append(res)

    # res3构建
    for data_path_item in sample_size_dic.keys():
        res = data_path_item
        for language in sample_size_dic[data_path_item].keys():
            res += "," + language + "," + str(sample_size_dic[data_path_item][language])
        sample_size_list.append(res)
           
    print(sample_total, sample_little_total)
    print("输出模版参数:")
    print("采样数据集")
    sample_data_str = ",".join(sample_data_list)
    print(sample_data_str)
    print("***********")
    print("采样大小（单位：GB）")
    sample_size_str = ";".join(sample_size_list)
    print(sample_size_str)
    print("***********")
    print("采样倍数")
    sample_ratio_str = ";".join(sample_ratio_list)
    print(sample_ratio_str)
    print("***********")
    


'''
fw = open("/apdcephfs_cq8/share_1324356/jasonzli/translation/data/pretrain/exp_add_little/tmp.txt", "w")
for lan in cpt_perf_dic:
    lan_code = lan_dic_reverse[lan]
    if lan_code not in lan_size_dist:
        continue
    dist = lan_size_dist[lan_code]
    fw.write(lan + "\t" + str(cpt_perf_dic[lan]) + "\t" + str(dist) + "\n")
'''