#!/bin/bash

CONDA_PATH="$HOME/miniconda3"
INSTALLER="Miniconda3-latest-Linux-x86_64.sh"

# 下载
if [ ! -f "$INSTALLER" ]; then
    wget https://repo.anaconda.com/miniconda/$INSTALLER
fi

bash $INSTALLER -b -u -p $CONDA_PATH

$CONDA_PATH/bin/conda init bash
source ~/.bashrc

echo "Done！"
