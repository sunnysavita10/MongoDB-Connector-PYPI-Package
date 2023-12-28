from setuptools import setup, find_packages
from typing import List
<<<<<<< HEAD

=======
   
>>>>>>> 4dce55b5c0eb4e567f13dd5b9ac65c707a83ed99
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()     
   

__version__ = "0.0.4"
REPO_NAME = "mongodbconnectorpkg"
PKG_NAME= "Mongo-Connect"
AUTHOR_USER_NAME = "sunnysavita10"
AUTHOR_EMAIL = "sunny.savita@ineuron.ai"

setup(
    name=PKG_NAME,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A python package for connecting with database.",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
<<<<<<< HEAD
    packages=find_packages(where="src"),
)
=======
    packages=find_packages(where="src")
)
>>>>>>> 4dce55b5c0eb4e567f13dd5b9ac65c707a83ed99
