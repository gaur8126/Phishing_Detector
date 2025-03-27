from setuptools import setup,find_packages
from typing import List

def get_requirements()->List[str]:


    requirements_lst:List[str] = []
    try:
        with open("requirements.txt","r") as file:
            lines = file.readlines()

            for line in lines: 
                requirement = line.strip()

                if requirement and requirement != "-e .":
                    requirements_lst.append(requirement)
    except FileNotFoundError:
        print("requiremnts.txt file not found")

    return requirements_lst

setup(
    name="phishing_detector",
    version="0.0.1",
    author="lokesh",
    author_email="gaurlokesh1211@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements()
)