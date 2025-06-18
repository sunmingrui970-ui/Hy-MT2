# xcomet

## 测试数据
/apdcephfs_cq8/share_1324356/jasonzli/translation/data/test/test_data/multi_language_translate_text_with_ref_all_no_long.jsonl

## 测试步骤
Step1: 一站式申请机器,开启debug模式

Step2: 配置环境,执行set_env.sh

Step3: get_comet.py 对上面的数据进行打分

Step4: translate_comet_eval.py 统计分数
