"""Generate Markov text from text files."""

import sys
from random import choice


def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    the_file = open(file_path).read()

    return the_file


def make_chains(text_string, n):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita hi there buddy stue")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """
    words = text_string.split()

    chains = {}

    for i in range(len(words) - n):

        tuple_key = []

        for x in range(n):

            tuple_key.append(words[x+i])

        tuple_key = tuple(tuple_key)

        chains.setdefault(tuple_key, [])

        if i == (len(words) - n):
            chains[tuple_key].append(None)
        else:
            chains[tuple_key].append(words[i + n])

        # elif (words[i], words[i + 1]) in chains:
        #     chains[(words[i], words[i + 1])].append(words[i + 2])
        # else:
        #     chains[(words[i], words[i + 1])] = [words[i + 2]]

    return chains


def make_text(chains):
    """Return text from chains."""

    words = []

    random_tuple = choice(chains.keys())
    random_word = choice(chains[random_tuple])

    while random_word is not None:

        words.append(random_word)

        random_tuple = list(random_tuple)

        random_tuple.append(random_tuple[1:])

        random_tuple.append(random_word)

        random_tuple = tuple(random_tuple)

        random_word = choice(chains[random_tuple])

    return " ".join(words)


input_path = sys.argv[1]

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text, 3)

print chains

# Produce random text
#random_text = make_text(chains)

#print random_text
