
# +--------------------------------------------------+
# |   RANDOM SEED CONFIGS                            |
# +--------------------------------------------------+
SEED = 1234

# +--------------------------------------------------+
# |   WORD REPLACEMENT CONFIGS                       |
# +--------------------------------------------------+
# Set possible characters used to replace unreadable words
# "X" -> "X" * random.randint(2, 5) -> "XXXXX"
# use "" to leave the word blank, which can also happen for unreadable words
# you can use as many options as you want
# Default: 
# WORD_REPLACEMENT_OPTS  = {
#    "X": 0.6, 
#    "" : 0.3, 
# }
WORD_REPLACEMENT_OPTS = {
    "X": 0.6, 
    "" : 0.3, 
}

# Probability of replacing a word with a blank string or a string of Xs (or other characters if specified) 
# Default: 0.005 (0.5%)
WORD_REPLACEMENT_PROB = 0.005

# +--------------------------------------------------+
# |   TYPO CONFIGS                                   |
# +--------------------------------------------------+
# Set probability of typos
# You cannot add more options here, but you can change the weights
# Default:
# TYPO_MODES_OPTS = {
#     "swap": 0.2,
#     "delete": 0.2,
#     "insert": 0.1,
#     "nearby": 0.2,
#     "similar": 0.2,
#     "agglomerate": 0.2,
#     "repeat": 0.1,
#     "unichar": 0.2,
#     "split": 0.1
# }
TYPO_OPTS = {
    "swap": 0.2,
    "delete": 0.2, 
    "insert": 0.1,
    "nearby": 0.2,
    "similar": 0.2,
    "agglomerate": 0.2,
    "repeat": 0.1,
    "unichar": 0.2,
    "split": 0.1
}

# Probability of applying a typo
# Default: 0.1 (10%)
TYPO_PROB = 0.1





