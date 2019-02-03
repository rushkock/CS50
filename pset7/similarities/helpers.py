# Ruchella Kock
# 12460796
# This file defines 4 functions:
# lines: compares 2 files based on their lines
# sentences: compares 2 files based on the number of unique sentences
# substrings: compares 2 files based of the number of substrings of length n
# make_substring: makes the substrings that should be compared

from nltk.tokenize import sent_tokenize
import sys


def lines(a, b):
    """Return lines in both a and b"""
    set_a = set(a.split("\n"))
    set_b = set(b.split("\n"))
    return list(set_a.intersection(set_b))


def sentences(a, b):
    """Return sentences in both a and b"""
    set_a = set(sent_tokenize(a))
    set_b = set(sent_tokenize(b))
    return list(set_a.intersection(set_b))


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    if len(a) and len(b) >= n:
        set_a = set(make_substring(a, n))
        set_b = set(make_substring(b, n))
        return list(set_a.intersection(set_b))
    else:
        return []


def make_substring(string, n):
    i = 0
    j = n
    new_string = string[i:j]
    list_of_strings = []
    while (len(new_string) == n):
        new_string = string[i:j]
        list_of_strings.append(new_string)
        i = i + 1
        j = j + 1
    del list_of_strings[-1]
    return list_of_strings