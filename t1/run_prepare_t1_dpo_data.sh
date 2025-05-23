input_file=/apdcephfs_cq8/share_1324356/jasonzli/translation/data/t1/dpo/infer_res_8_times_turbos_t1_0321bus_exp14_5epo_gy_xcomet_output/part_aa
input_file=/apdcephfs_cq8/share_1324356/jasonzli/translation/src/Machine_Translation/v250331/train.jsonl
output_file=/apdcephfs_cq8/share_1324356/jasonzli/translation/src/Machine_Translation/v250331/train_clean.jsonl
python -u prepare_t1_dpo_data.py ${input_file} --output_file=${output_file}