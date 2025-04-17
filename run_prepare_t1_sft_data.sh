#input_file=/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/sft/add_0327/sft_craw_r1_zh2other.jsonl
#output_file=/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/sft/add_0327/new_sft_clean.jsonl
#input_file=/apdcephfs_cq8/share_1324356/jasonzli/translation/src/Machine_Translation/v250314/train.jsonl
#output_file=/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/sft/add_0327/old_sft_bad.jsonl
#input_file=/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/sft/add_0327/ft_local/crawl_retry_output.jsonl
#output_file=/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/sft/add_0327/new_sft_clean_part2.jsonl
#input_file=/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/sft/add_0327/ft_local/old_sft_bad_crawl2.jsonl
#output_file=/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/sft/add_0327/old_sft_clean_part2.jsonl
input_file=/apdcephfs_cq8/share_1324356/jasonzli/translation/src/Machine_Translation/v250409/train.jsonl
#python -u prepare_t1_sft_data.py ${input_file}
output_file=/apdcephfs_cq8/share_1324356/jasonzli/translation/src/Machine_Translation/v250409/train_clean.jsonl
input_file=/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/sft/add_0406/ft_local/translate_zhen_hecheng_v1.0_crawl_input_part_aa_output
output_file=/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/sft/add_0406/ft_local/translate_zhen_hecheng_v1.0_crawl_input_part_aa_output_sft_format
input_file=/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/sft/explain/explain_output.jsonl
output_file=/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/sft/explain/explain_output_clean.jsonl
python -u prepare_t1_sft_data.py ${input_file} --output_file=${output_file}