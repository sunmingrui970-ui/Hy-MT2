input_file=/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/grpo/human_label.jsonl
output_file=/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/grpo/human_label.jsonl_grpo_format
python -u prepare_t1_grpo_data.py ${input_file} --output_file=${output_file}