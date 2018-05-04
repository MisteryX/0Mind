# Installation

0Mind can be installed on any OS/platform which supports **Python 3** and target machine learning frameworks

Install Git to clone project repository.

Go to the directory where 0Mind should be (For example /home/user/Projects) and clone repository.
```
git clone git@github.com:MisteryX/0Mind.git 0Mind
```
Now you have all files of the project in the directory **0Mind**. 
After that you should install all required Python packages.
```
cd 0Mind
pip3 install -r requirements.txt
```

## Special cases
If you want to work with **caffe2** framework, you should install it manually using Conda\Miniconda and after that execute **pip install -r requirements.txt** in the Conda environment.