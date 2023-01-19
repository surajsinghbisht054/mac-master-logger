from setuptools import setup, find_packages
from maclogger import __version__

# Setting up
setup(
    name="maclogger",
    version=__version__,
    author="Vaibhav Sharma",
    author_email="asvaibhavsharma@gmail.com",
    description="Package for communicating to MacMaster",
    packages=find_packages(),
    install_requires=['requests-async']
)