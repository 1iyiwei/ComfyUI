#!/bin/bash

sudo apt install -y tmux
session_name=comfyUI
tmux kill-session -t ${session_name}
conda init bash
conda activate comfyui
tmux new-session -d -s ${session_name} 'python main.py --listen --port 8188 --prefix "/comfyUI/"'