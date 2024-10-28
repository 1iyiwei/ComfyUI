#!/bin/bash

prefix="$1" #e.g., /kineto-demo/lwei-comfy/igocsxlepson

export LD_LIBRARY_PATH=/opt/conda/envs/comfyui/lib/python3.11/site-packages/nvidia/nvjitlink/lib:$LD_LIBRARY_PATH
sudo apt-get update
sudo apt install -y tmux
sudo apt install ffmpeg
session_name=comfyUI
tmux kill-session -t ${session_name}
conda create -n comfyui python=3.11 -c conda-forge
conda activate comfyui
pip install -r requirements.txt
tmux new-session -d -s ${session_name} "python main.py --listen --port 8188 --prefix ${prefix} 2>&1 | tee ${session_name}.log"