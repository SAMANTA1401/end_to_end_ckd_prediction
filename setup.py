from setuptools import find_packages, setup
from typing import List
import ez_setup
ez_setup.use_setuptools()

HYPEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]: #return filepath as list of string
    ''' This function will return the list of requirements'''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        [req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

__version__ = "0.0.1"

REPO_NAME = "ckd_prediction"
AUTHOR_USER_NAME = "Shubhankar"
SRC_REPO = "annClassifier"
AUTHOR_EMAIL = ""

setup(
    name=REPO_NAME,
    version=__version__ ,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    package_dir={"":"src"},
    packages=find_packages(where="src"),
    install_requires=get_requirements('requirements.txt')

    
)