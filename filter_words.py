from __future__ import print_function
import re
import sys
import time

def debug_time(msg, init, now):
    print("{} [{}ms]".format(msg, int(round((now-init)*1000*1000))/1000.0), file=sys.stderr)

####################
# CMD LINE PARSING #
####################
argc = len(sys.argv)
argv = sys.argv

# List of cmdline flag variables
FLAGS = set([])

# Number of required arguments
REQUIRED_ARGS = ["word_list"]
OPTIONAL_ARGS = {
    "words": "white_list"
}

############################################
# PARSING CMD LINE STUFF - no need to edit #
############################################
NUM_REQUIRED_ARGS = len(REQUIRED_ARGS) + 1
# --> [executable name, word list file name]
args = []

# Flags/Optional Arguments
flags = set()
optional_args = {key: None for key in OPTIONAL_ARGS.keys()}
undefined_args = []

def print_usage():
    print("Usage: python " + args[0], end='')
    for arg in REQUIRED_ARGS:
        print(" <{}>".format(arg), end='')
    if (len(OPTIONAL_ARGS) > 0):
        for k, v in OPTIONAL_ARGS.items():
            print(" -{} <{}>".format(k, v), end='')
    if (len(FLAGS) > 0):
        print(' [', end='')
        for f in FLAGS:
            print(" -{}".format(f), end='')
        print(' ]', end='')
    print('')

# We scan through command line arguments and place them into the correct types
arg_i = 0
while (arg_i < argc):
    if ('-' == argv[arg_i][0]):
        flag = argv[arg_i][1:]
        if (flag in FLAGS):
            # Argument format: -flag
            flags.add(flag)
        elif (flag in optional_args):
            # Argument format: -flag <string>
            optional_args[argv[arg_i][1:]] = argv[arg_i+1]
            arg_i += 1
        else:
            undefined_args.append(argv[arg_i])
    else:
        args.append(argv[arg_i])
    arg_i += 1

if (len(args) < NUM_REQUIRED_ARGS):
    print_usage()
    exit()
#############################################################################
# END OF PARSING - arguments in: args, optional_args, undefined_args, flags #
#############################################################################

# word pair .csv file
WORD_FILE = args[1]
WHITE_LIST = optional_args['words']

# Declared replacement policy ruleset
filter_rules = {
    # Remove all trailing plurals
    "s$": "",
    "es$": "",
    # Remove action verbs
    "ing$": "",
    "er$": ""
}

#TODO: Have these as separate config files
# Direct replacement mapping (prints after every scan - save time for later scans)
replacement_rules = {
    "axe": "ax",
    "appartment": "apartment",
    "seats": "seat",
    "seeds": "seed",
    "chopping": "chop",
    "cutting": "cut",
    "logs": "log",
    "crying": "cry",
    "soother": "sooth",
    "handles": "handle",
    "cookies": "cookie",
    "cupcakes": "cupcake",
    "pastries": "pastry",
    "muffins": "muffin",
    "bouncing": "bounce",
    "swimming": "swim",
    "claws": "claw",
    "berries": "berry",
    "tubing": "tube",
    "sails": "sail",
    "paddles": "paddle",
    "muscles": "muscle",
    "machines": "machine",
    "bars": "bar",
    "gifts": "gift",
    "presents": "present",
    "candles": "candle",
    "arabs": "arab",
    "driving": "drive",
    "wheels": "wheel",
    "tires": "tire",
    "bricks": "brick",
    "stones": "stone",
    "benches": "bench",
    "pews": "pew",
    "big shoes": "big shoe",
    "speakers": "speaker",
    "gems": "gem",
    "diamonds": "diamond",
    "jewels": "jewel",
    "pyramids": "pyramid",
    "scrubs": "scrub",
    "walking": "walk",
    "barking": "bark",
    "pills": "pill",
    "magazines": "magazine",
    "germs": "germ",
    "garbage bins": "garbage bin",
    "wrapping": "wrap",
    "dolls": "doll",
    "wrinkles": "wrinkle",
    "mittens": "mitten",
    "palms": "palm",
    "riding": "ride",
    "hooves": "hoof",
    "horseshoes": "horseshoe",
    "sprinkles": "sprinkle",
    "knights": "knight",
    "fixes": "fix",
    "fixing": "fix",
    "overalls": "overall",
    "vines": "vine",
    "filling": "fill",
    "goggles": "goggle",
    "utensils": "utensil",
    "boxes": "box",
    "packages": "package",
    "stamps": "stamp",
    "jumping": "jump",
    "hopping": "hop",
    "elves": "elf",
    "books": "book",
    "lockers": "locker",
    "students": "student",
    "classmates": "classmate",
    "dogs": "dog",
    "herder": "herd",
    "shoelaces": "shoelace",
    "laces": "lace",
    "high heels": "high heel",
    "heels": "heel",
    "soles": "sole",
    "studying": "study",
    "textbooks": "textbook",
    "teaching": "teach",
    "branches": "branch",
    "roots": "root",
    "tips": "tip",
    "pacifier": "pacify",
    "steering": "steer",
    "bins": "bin",
    "rocking": "rock",
    "getting": "get",
    "clothing": "cloth"
}

# Declared white-list of words - Ignores fixing these words
white_list = set([
    "cash register",
    "bank teller",
    "comforter",
    "stinger",
    "penis",
    "platter",
    "candleholder",
    "wrapper",
    "tim hortons",
    "starbucks",
    "diamond ring",
    "pain killer",
    "letter opener",
    "sharpener",
    "police officer",
    "school bus",
    "dark clothing",
    "hortons"
])

if (WHITE_LIST is not None):
    with open(WHITE_LIST, 'r') as fin:
        for line in fin:
            white_list.add(line.strip().lower())

############################
# READ WORD LIST FROM FILE #
############################
word_t = time.time()
word_list = set()
fixed_words = dict()
with open(WORD_FILE, 'r') as fin:
    for line in fin:
        prime, target = line.strip().split(',')
        # Check if whitelisted
        if (prime in white_list):
            pass
        # Check if we have fixed this word before
        elif (prime in fixed_words):
            prime = fixed_words[prime]
        # Check if not yet fixed this run but have direct replacement available
        elif (prime in replacement_rules):
            prime = replacement_rules[prime]
        else:
            # Run through our list of rules
            for pattern, replacement in filter_rules.items():
                match_list = re.search(pattern, prime)
                if (match_list is not None):
                    fixed_prime = prime[:match_list.span()[0]] + replacement
                    print("Matched: {} ({}) Fix: {}->{}?".format(match_list.group(), pattern, prime, fixed_prime), end="")
                    fixed_word = input().strip()
                    if (len(fixed_word) > 1):
                        fixed_words[prime] = fixed_word
                        replacement_rules[prime] = fixed_word
                        prime = fixed_word
                        break
                    elif (fixed_word.lower() == 'y'):
                        fixed_words[prime] = fixed_prime
                        replacement_rules[prime] = fixed_prime
                        prime = fixed_prime
                        break
            fixed_words[prime] = prime
        # Check if whitelisted
        if (target in white_list):
            pass
        # Check if we have fixed this word before
        elif (target in fixed_words):
            target = fixed_words[target]
        # Check if not yet fixed this run but have direct replacement available
        elif (target in replacement_rules):
            target = replacement_rules[target]
        else:
            # Run through our list of rules
            for pattern, replacement in filter_rules.items():
                match_list = re.search(pattern, target)
                if (match_list is not None):
                    fixed_target = target[:match_list.span()[0]] + replacement
                    print("Matched: {} ({}) Fix: {}->{}?".format(match_list.group(), pattern, target, fixed_target), end="")
                    fixed_word = input().strip()
                    if (len(fixed_word) > 1):
                        fixed_words[target] = fixed_word
                        replacement_rules[target] = fixed_word
                        target = fixed_word
                        break
                    elif (fixed_word.lower() == 'y'):
                        fixed_words[target] = fixed_target
                        replacement_rules[target] = fixed_target
                        target = fixed_target
                        break
            fixed_words[target] = target
        word_list.add((prime, target))

word_list = sorted(list(word_list))
print("Following replacements are applied:\n")
print("replacement_rules = {")
for key, value in replacement_rules.items():
    print("    \"{}\": \"{}\",".format(key, value))
print("}\n")

debug_time("Finished fixing word pairs...", word_t, time.time())

###################
# WRITE WORD LIST #
###################
# Write our filtered pairs to file
OUTPUT_FIXED_WORDS = "{}_{}.csv".format('.'.join(WORD_FILE.split('.')[:-1]), "fixed")
print("Writing to: ", OUTPUT_FIXED_WORDS, file=sys.stderr)
with open(OUTPUT_FIXED_WORDS, 'w+') as fout:
    for prime, target in word_list:
        # Output to csv format
        fout.write("{},{}\n".format(prime, target))