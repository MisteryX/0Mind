# Installation

0Mind can be installed on any OS/platform which supports **Python 3** and target machine learning frameworks

Install Git to clone project repository.

Go to the directory where 0Mind should be (For example /home/user/Projects) and clone repository.
```
git clone git@github.com:MisteryX/0Mind.git 0Mind
```
Now you have all files of the project in the directory **0Mind**. 
After that you should install all required Python packages.
```bash
cd 0Mind
pip3 install -r requirements.txt
```
or if you use Conda
```bash
conda install --yes --file requirements.txt
```

## Frameworks
0Mind supports [a lot of ML frameworks](ML_FRAMEWORKS.MD), but in production environment usually are used one or two,
so we don't include all supported frameworks to requirements file. 
To activate support of particular framework in 0Mind, you should install and configure required tool manually.