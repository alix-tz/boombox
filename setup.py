import pathlib
from setuptools import setup

exec(open('boombox/version.py').read())

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE/"README.md").read_text()

#with open("requirements.txt", encoding="utf-8") as f:
#    install_required = f.read().splitlines()

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
    install_requires=[
        "lxml==4.9.2",
        "textdistance==4.5.0",
        "typo @ git+https://github.com/alix-tz/typo@b2f65a418c0671ce749ab4cb060acfdb2e6062fa",
        "tabulate==0.9.0",
        "art==5.8",
        "pandas==1.3.5",
    ],
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