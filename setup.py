import pathlib
from setuptools import setup

exec(open('boombox/version.py').read())

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE/"README.md").read_text()

with open("requirements.txt", encoding="utf-8") as f:
    install_required = f.read().splitlines()

setup(
    name='boombox',
    version=__version__,
    description='A python package to make synthetic noise in HTR datasets.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/alix-tz/boombox',
    author = "Alix Chagué",
    license='MIT',
    python_requires='>=3.8',
    install_requires=install_required,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    packages=['boombox'], 
    keywords=["HTR", "handwritten text recognition", "synthetic noise", "data diminution", "data augmentation"]
)