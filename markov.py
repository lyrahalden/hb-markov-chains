"""Generate Markov text from text files."""

from random import choice


def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    the_file = open(file_path).read()

    return the_file


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

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

    for i in range(len(words) - 1):

        tuple_key = (words[i], words[i + 1])

        chains.setdefault(tuple_key, [])

        if i == (len(words) - 2):
            chains[tuple_key].append(None)
        else:
            chains[tuple_key].append(words[i + 2])

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

    while random_word != None:

        random_tuple = (random_tuple[1], random_word)

        words.extend(random_tuple[1], random_word)

        random_word = choice(chains[random_tuple])



        #new_random_key = choice(chains[new_tuple])






    return " ".join(words)


input_path = "green-eggs.txt"

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text)

print chains

# Produce random text
#random_text = make_text(chains)

#print random_text
