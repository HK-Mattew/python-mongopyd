#!/usr/bin/env python
from typing import (
    List
)
from pathlib import Path
from setuptools import setup, find_packages




def get_requirements() -> List[str]:
    """Build the requirements list for this project"""
    requirements_list = []

    with Path("requirements.txt").open(encoding="UTF-8") as reqs:
        for install in reqs:
            if install.startswith("#"):
                continue
            requirements_list.append(install.strip())

    return requirements_list




setup(
      name='python-mongopyd',
      version='0.1',
      description='Simple and efficient Pydantic-based models for MongoDB (PyMongo & Motor)',
      long_description=Path('README.md').read_text(encoding='UTF-8'),
      author='HK-Mattew',
      author_email='not-found@localhost.local',
      url='https://github.com/HK-Mattew/python-mongopyd',
      packages=find_packages(),
      requires=get_requirements(),
      license='MIT license',
      keywords=['mongodb orm', 'mongodb model', 'pymongo', 'motor', 'pydantic']
      )
