# Path: run.py

import os
import argparse
from collections import Counter
from datetime import datetime

from art import text2art
import pandas as pd
from tabulate import tabulate

from boombox.boombox import BoomBox
from config import *


def get_eligible_files(path_in, file_type):
    files = [f for f in os.listdir(path_in) if os.path.isfile(os.path.join(path_in, f))]
    if file_type == "text":
        files = [f for f in files if f.endswith(".txt")]
        files = [f for f in files if not f.endswith("_noisy.txt")]
    elif file_type == "alto" or file_type == "xml":
        files = [f for f in files if f.endswith(".xml")]
        files = [f for f in files if not f.endswith("_noisy.xml")]
    return files


def get_path_out(po):
    if po:
        return po
    else:
        return None


def get_file_path_out(path_in, path_out, f):
    if not path_out:
        if f.endswith(".txt"):
            path_out_f = path_in.replace(".txt", "_noisy.txt")
        elif f.endswith(".xml"):
            path_out_f = path_in.replace(".xml", "_noisy.xml")
    else:
        path_out_f = os.path.join(path_out, f)
    return path_out_f


def get_noise_opts():
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
    return noise_opts


def make_outdir_if_needed(path_out):
    if path_out:
        if not os.path.exists(path_out):
            os.makedirs(path_out)


def make_cer_msg(avg_cer):
    n = 20
    if avg_cer <= 10.0:
        n += 1
    return f"+----------------------------------------+\n" + \
            f"| Average CER: {avg_cer:.2f}%{' '*n}|\n" + \
            f"+----------------------------------------+\n"

def compare_strings(original_list, noisy_list):
    count_original_str = Counter("".join(original_list))
    count_noisy_str = Counter("".join(noisy_list))

    all_chars = set(list(count_original_str.keys()) + list(count_noisy_str.keys()))
    # make a pd table with 4 columns: the list of all chars, the count in the original string, the count in the noisy string, and the difference
    chars_table = pd.DataFrame(
        columns=["char", "original", "noisy", "diff"]
    )
    for char in all_chars:
        chars_table = chars_table.append(
            {
                "char": char,
                "original": count_original_str[char],
                "noisy": count_noisy_str[char],
                "diff": count_noisy_str[char] - count_original_str[char],
            },
            ignore_index=True,
        )
    # sort by diff
    chars_table = chars_table.sort_values(by="diff", ascending=False)
    return chars_table

def make_report(chars_table, avg_cer_msg):
    # get date and time for report
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    table_as_str = tabulate(chars_table, headers='keys', tablefmt='psql', showindex=False)
    print(avg_cer_msg)
    print(table_as_str)
    report = "".join([f"\n\n{'#'*10} {dt_string} {'#'*10}\n", avg_cer_msg, table_as_str])
    report_file_name = "boombox_" + now.strftime("%Y-%m-%d") + ".log"
    with open(report_file_name, "a+", encoding="utf8") as fh:
        fh.write(report)


def main(args):
    # welcome message
    print(text2art("\nBoomBox", font="tarty2"))

    # set input and output paths
    path_in = args.path
    file_type = args.type
    path_out = get_path_out(args.path_out)
    files = get_eligible_files(path_in, file_type)

    if len(files) == 0:
        raise ValueError("No files found in the input folder")
    
    noise_opts = get_noise_opts()
    if args.cer:
        noise_opts["typo_prob"] = args.cer

    # make directory if it doesn't exist
    make_outdir_if_needed(path_out)

    # process files
    original = []
    noisy = []
    cers = []

    for f in files:
        path_out_f = get_file_path_out(path_in, path_out, f)
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
    
    # get overall stats
    avg_cer = 0
    # get average CER
    if sum(cers) > 0 and len(cers) > 0:
        avg_cer = (sum(cers) / len(cers)) * 100
    
    # build report
    avg_cer_msg = make_cer_msg(avg_cer)
    chars_report = compare_strings(original, noisy)
    make_report(chars_report, avg_cer_msg)



# set argparser
parser = argparse.ArgumentParser(
    description="Boombox: a tool for generating noisy data for HTR training.Use config.py to set the parameters of the noise to be applied."
)
parser.add_argument("-i", "--path", required=True,
                    help="path to the folder containing the files to be processed")
parser.add_argument("-t", "--type", required=True,
                    help="type of file to be processed: text or alto")
parser.add_argument("-o", "--path_out", 
                    help="path to the folder where the noisy files will be saved")
parser.add_argument("--cer", help="character error rate to aim for", type=float)

args = parser.parse_args()


if __name__ == "__main__":
    main(args)