# Path: run.py

import os
import argparse

from boombox.boombox import BoomBox
from config import *


# set argparser
parser = argparse.ArgumentParser(description="Boombox: a tool for generating noisy data for HTR training. Use config.py to set the parameters of the noise to be applied.")
parser.add_argument("-i", "--path", help="path to the folder containing the files to be processed", required=True)
parser.add_argument("-t", "--type", help="type of file to be processed: text or alto", required=True)
parser.add_argument("-o", "--path_out", help="path to the folder where the noisy files will be saved")

args = parser.parse_args()

# set input and output paths
path_in = args.path
file_type = args.type
if args.path_out:
    path_out = args.path_out
else:
    path_out = None

# get list of files to be processed
files = [f for f in os.listdir(path_in) if os.path.isfile(os.path.join(path_in, f))]
if file_type == "text":
    files = [f for f in files if f.endswith(".txt")]
elif file_type == "alto" or file_type == "xml":
    files = [f for f in files if f.endswith(".xml")]

if len(files) == 0:
    raise ValueError("No files found in the input folder")

# get noise options from config
try:
    noise_opts = {
        "typo_prob": TYPO_PROB,
        "typo_opts": TYPO_OPTS,
        "word_replacement_prob": WORD_REPLACEMENT_PROB,
        "word_replacement_opts": WORD_REPLACEMENT_OPTS,
    }

except NameError:
    raise ValueError("Incorrect settings in config.py")

# process files
original = []
noisy = []

for f in files:
    boom = BoomBox(os.path.join(path_in, f), file_type=file_type)
    boom.add_noise(noise_opts, save=True, path_out=path_out)
    original.extend(boom.original)
    noisy.extend(boom.noisy)
    print("File processed: {}".format(f))
    print("Resulting CER: {}".format(boom.get_cer()))

# get overall CER
# note for later: create a class called capharnaum that will contain all the functions for calculating CER
# and other metrics


