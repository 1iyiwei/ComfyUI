#!/bin/bash

sudo apt install -y tmux
sudo apt install ffmpeg
conda create -n comfyui python=3.11 -c conda-forge
conda activate comfyui
pip install -r requirements.txt
session_name=comfyUI
tmux kill-session -t ${session_name}
conda init bash
conda activate comfyui
tmux new-session -d -s ${session_name} 'python main.py --listen --port 8188 --prefix "/comfyUI/"'