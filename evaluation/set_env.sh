cd /
bash setup.sh
# 挂载ceph盘
taiji_client mount -tk token -bf nlp_tech_common_chongqing

#cd /apdcephfs_cq8/share_1324356/data/bingxinqu/tools
#nohup /opt/vllm/bin/python h800.py &

#pip3 install torch torchvision torchaudio
#pip3 install pyyaml
#pip3 install huggingface_hub
pip3 install pytorch_lightning
pip3 install scipy
#pip3 install transformers

pip3 install tensorflow

bash enable_internet_proxy.sh
source ~/.bashrc
pip3 install unbabel-comet
pip3 install entmax
