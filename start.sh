#!/bin/bash

prefix="$1" #e.g., /kineto-demo/lwei-comfy/igocsxlepson
sleep_amount=$2

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd ${SCRIPT_DIR}
unset SCRIPT_DIR

sudo apt-get update
sudo apt install -y tmux
sudo apt install -y ffmpeg
conda create -n comfyui python=3.11 -c conda-forge
conda activate comfyui
pip install --upgrade pip
pip install -r requirements.txt
for custom_node in custom_nodes/*; do
    custom_node_requirement=${custom_node}/requirements.txt
    if [ -f ${custom_node_requirement} ]; then
        echo ${custom_node_requirement}
        pip install -r ${custom_node_requirement}
    fi
done
session_name=comfyUI
#tmux kill-session -t ${session_name}
tmux new-session -d -s ${session_name} "python main.py --listen --port 8188 --prefix ${prefix} 2>&1 | tee ${session_name}.log"

if [ -n "$sleep_amount" ]; then
    sleep $sleep_amount
fi

