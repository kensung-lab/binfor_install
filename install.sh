#!/bin/bash

CONDA_PATH="$HOME/miniconda3"
INSTALLER="Miniconda3-latest-Linux-x86_64.sh"

if [ ! -f "$INSTALLER" ]; then
    wget https://repo.anaconda.com/miniconda/$INSTALLER
fi

bash $INSTALLER -b -u -p $CONDA_PATH

$CONDA_PATH/bin/conda init bash
source ~/.bashrc

echo "Done！"
echo "------------------------------------------------------------"
echo "Miniconda installation is complete!"
echo "IMPORTANT: To start using conda, please run the command below:"
echo "source ~/.bashrc"
echo "------------------------------------------------------------"

source "$CONDA_PATH/etc/profile.d/conda.sh"

conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

conda install -c bioconda -c conda-forge bwa -y
conda install -c bioconda -c conda-forge samtools -y
conda install -c conda-forge ncurses --force-reinstall -y
conda install -c bioconda -c conda-forge fastqc -y

