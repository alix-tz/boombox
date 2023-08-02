<img src="./assets/boombox.svg" width="150" align="right">

# BoomBox

BoonBox is a small program which adds noise in TXT or ALTO XML files. It was created for the purpose of an experiment around handwritten text recognition (HTR) related data.

## Set up

Create a virtual environment with [Python's vitualenv](https://docs.python.org/3.9/library/venv.html) or with [Anaconda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands) and use PiPy to install the requirements.

```sh
(venv)~$ pip install -r requirements.txt 
```

## Tuning the boombox

You can adjust different parameters to define the quantity and the type of noise made by the boombox. All of these parameters can be set in the `config.py` file.

### Random Seed

You can make the noise somewhat reproducible by using a seed. <!-- make sure I actually use this info -->

### Word replacement scenario

In an attempt to imitate transcribers' errors, the boombox can delete a word or replace all of its letters with a fixed character (repeat 2 to 5 times). By default, the boombox can give the following outcome when a word replacement scenario is activated:

1. `""`: `this is my example` -> `this is example`
2. `"X"`: `this is my example` -> `this is XXX example`

You can set a probability for on or the other replacement string to be chosen, and you can add more options for replacement strings.

You can also set a probability of the word replacement scenario to occur.

Since this scenario comes after all the other modifications are done to the text, keep in mind that it might overwrite some of the noise induced at character level.

### Typos

The boombox induce realistic typos in the text. Using our own adaptation of the [typo](https://github.com/alix-tz/typo/tree/azerty)[^1] library, there can be 9 different type of typos generated in the text:

- `swap` will swap two adjacent letters: `example` -> `exapmle`
- `delete` will remove 1 letter: `example` -> `examle`
- `insert` will add 1 letter, considered a [keyboard neighbor](https://github.com/alix-tz/typo/blob/b2f65a418c0671ce749ab4cb060acfdb2e6062fa/typo/keyboardlayouts/fr_azerty.py#L3): `example` -> `exampole`
- `nearby` will replace 1 letter with another letter, considered a [keyboard neighbor](https://github.com/alix-tz/typo/blob/b2f65a418c0671ce749ab4cb060acfdb2e6062fa/typo/keyboardlayouts/fr_azerty.py#L3): `example` -> `examole`
- `similar` will replace 1 letter with another letter considered visually [similar](https://github.com/alix-tz/typo/blob/b2f65a418c0671ce749ab4cb060acfdb2e6062fa/typo/keyboardlayouts/fr_azerty.py#L116): `example` -> `examqle`
- `agglomerate` will stick two words together, simulating a forgotten space: `my example` -> `myexample`
- `repeat` will repeat a character: `example` -> `exampple`
- `unichar` will take a double character and replace it with a single character: `happy` -> `hapy`
- `split` will add a random space in the middle of a word: `example` -> `exam ple`

It is possible to deactivate some of these scenarios and to modify how likely one scenario is to occur.

Note that according to the behavior set in the `typo` library, and since we apply several transformation scenario in a row, it is possible that a typo is added on top of another typo (with the risk of cancelling it).

Lastly, you can set how likely it is for a typo (whichever type the typo) to be added in the data.

[^1]: You should consider the fact that our adaptation of the typo library also relies on the addition of an AZERTY configuration for neighboring characters, on top of adapting the visually similar character to the case of handwritten characters.

## Press Play

Make sure you are in the boombox' main directory to run `run.py`, using the following options:

```sh

Boombox: a tool for generating noisy data for HTR training.Use config.py to set the parameters of the noise to be applied.

options:
  -h, --help            show this help message and exit
  -i PATH, --path PATH  path to the folder containing the files to be processed
  -t TYPE, --type TYPE  type of file to be processed: text or alto
  -o PATH_OUT, --path_out PATH_OUT
                        path to the folder where the noisy files will be saved
  --cer CER             character error rate to aim for
  -wr WORD_REPLACE, --word_replace WORD_REPLACE
                        word replacement probability
  --auto_dirname        if activated, automatically name the output directory after the noise level reached
```

You can use `--cer` and `-wr` to replace the values set in `config.py` when calling the script.

The most basic command to let the boombox play would be:

```sh
(venv)~/boombox$ python run.py -i path/to/source/files/ -t txt
```

or 

```sh
(venv)~/boombox$ python run.py  -i path/to/source/files/ -t alto
```

The other options are... optional. 🥁

## Targeted noise level vs. actual noise level

If you set a targeted character error probability to 10% and a word replacement probability to 0%, you will likely not end up with a text containing exactly 10% of noise. This is because of several parameters, the first being that it is just a probability that we are setting. However, this also caused by the fact that, as mentioned above, a typo scenario can occur on a previously modified part of the text. If you swap the same letters twice, you actually cancel the modification. Finally, the word replacement scenario can erase a word that didn't contain any typo, potentially adding a lot of noise in the data at once.

Luckily, the boombox applies a Character Error measure at the end of the transformation process in order to assess the actual noise level added in the text. If you use the `--auto_dirname` option, the new noisy dataset will be added in a folder named after the actually reached noise level.
