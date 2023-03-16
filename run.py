# Path: run.py

import os
import argparse

from art import text2art

from boombox.boombox import BoomBox
from config import *


# set argparser
parser = argparse.ArgumentParser(
    description="Boombox: a tool for generating noisy data for HTR training. Use config.py to set the parameters of the noise to be applied."
)
parser.add_argument(
    "-i",
    "--path",
    help="path to the folder containing the files to be processed",
    required=True,
)
parser.add_argument(
    "-t", "--type", help="type of file to be processed: text or alto", required=True
)
parser.add_argument(
    "-o", "--path_out", help="path to the folder where the noisy files will be saved"
)
parser.add_argument("--cer", help="character error rate to aim for", type=float)

args = parser.parse_args()

# welcome message
print(text2art("\nBoomBox", font="tarty2"))

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

files = [f for f in files if not f.endswith("_noisy.xml")]

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

if args.cer:
    noise_opts["typo_prob"] = args.cer

# process files
original = []
noisy = []
cers = []

# make directory if it doesn't exist
if path_out:
    if not os.path.exists(path_out):
        os.makedirs(path_out)

for f in files:
    if not path_out:
        if f.endswith(".txt"):
            path_out_f = path_in.replace(".txt", "_noisy.txt")
        elif f.endswith(".xml"):
            path_out_f = path_in.replace(".xml", "_noisy.xml")
    else:
        path_out_f = os.path.join(path_out, f)
    boom = BoomBox(os.path.join(path_in, f), file_type=file_type)
    boom.add_noise(noise_opts, save=True, path_out=path_out_f)
    if boom.original:
        original.extend(boom.original)
    if boom.noisy:
        noisy.extend(boom.noisy)
    if boom.get_cer():
        cers.append(boom.get_cer())
    print("File processed: {}".format(f))
    print("Resulting CER: {}".format(boom.get_cer()))

avg_cer = 0
# get average CER
if sum(cers) > 0 and len(cers) > 0:
    avg_cer = (sum(cers) / len(cers)) * 100    

n = 9
if avg_cer <= 10.0:
    n += 1

print("+-----------------------------+")
print(f"| Average CER: {avg_cer:.2f}%{' '*n}|")
print("+-----------------------------+\n")




