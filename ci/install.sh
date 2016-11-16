#!/bin/sh

wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
conda config --set always_yes yes --set changeps1 no
conda update -q conda

# create test environement
conda create --quite -n env python=$TRAVIS_PYTHON_VERSION numpy
source activate env

# install requirements
pip install -r requirements.txt
pip install -r requirements_test.txt

if [[ $TRAVIS_PYTHON_VERSION == "2.7" ]]; then
  pip install https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-$TENSORFLOW-cp27-none-linux_x86_64.whl
elif [[ $TRAVIS_PYTHON_VERSION == "3.4" ]]; then
  pip install https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-$TENSORFLOW-cp34-cp34m-linux_x86_64.whl
elif [[ $TRAVIS_PYTHON_VERSION == "3.5" ]]; then
  pip install https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-$TENSORFLOW-cp35-cp35m-linux_x86_64.whl
fi
