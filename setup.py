from setuptools import setup
from pathlib import Path
from maclogger import __version__


def get_install_requires():
    """Returns requirements.txt parsed to a list"""
    
    fname = Path(__file__).parent / 'requirements.txt'
    targets = []
    if fname.exists():
        with open(fname, 'r') as f:
            targets = f.read().splitlines()
    return targets

setup(
    name='maclogger',
    version=__version__,
    url='https://github.com/surajsinghbisht054/mac-master-logger',
    author='Vaibhav Sharma',
    author_email='asvaibhavsharma@gmail.com',
    install_requires=get_install_requires(),
    py_modules=['maclogger'],
)
