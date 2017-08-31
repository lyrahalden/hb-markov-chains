"""Generate Markov text from text files."""

import sys
import twitter
import os
from random import choice

api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
                  consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
                  access_token_key=os.environ["TWITTER_ACCESS_TOKEN_KEY"],
                  access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"])


def open_and_read_file(file_path_1, file_path_2):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    the_file_1 = open(file_path_1).read()
    the_file_2 = open(file_path_2).read()

    the_file = the_file_1 + the_file_2

    return the_file


def make_chains(text_string, n):
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

    for i in range(len(words) - (n-1)):

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

    list_of_starting_capitals = []

    for chain in chains:
        if chain[0].istitle():
            list_of_starting_capitals.append(chain)

    random_tuple = choice(list_of_starting_capitals)

    words = [random_tuple[0], random_tuple[1]]

    random_word = choice(chains[random_tuple])

    list_of_punctuation = ["/", "?", "!", "."]

    while random_word is not None:

        if random_word[-1] in list_of_punctuation:
            words.append(random_word)
            break

        words.append(random_word)

        random_tuple = list(random_tuple)

        random_tuple = (random_tuple[1:] + [random_word])

        random_tuple = tuple(random_tuple)

        random_word = choice(chains[random_tuple])

    return " ".join(words)


def tweet(chains):

    user_choice = raw_input("Enter to tweet. q to quit >>> ")

    while user_choice != 'q':
        random_text = make_text(chains)
        new_tweet = random_text[:140]
        print new_tweet
        user_choice = raw_input("Do you want to publish this tweet? [y/n] >>> ")

        if user_choice == 'y':
            print api.VerifyCredentials()
            status = api.PostUpdate(new_tweet)
            print status.text
            print "Your tweet was published!"
            user_choice = raw_input("Enter to tweet. q to quit >>> ")
        else:
            user_choice = raw_input("Enter to tweet. q to quit >>> ")


input_path = sys.argv[1]
input_path_2 = sys.argv[2]

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path, input_path_2)

# Get a Markov chain
chains = make_chains(input_text, 2)

# Produce random text
#random_text = make_text(chains)

#print random_text[:140]

tweet(chains)


# This will print info about credentials to make sure
# they're correct


# If you updated secrets.sh, you can go to your Twitter
# timeline to see it.