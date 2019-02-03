# Ruchella Kock
# 12460796
# this program will take a given height and print a pyramid with two spaces in between

from cs50 import get_int

# prompt user for positive integer
while True:
    height = get_int("height: ")
    if height > 23 or height < 0:
        continue
    else:
        break

# do this height times
for x in range(height):
    # calculate the number of spaces
    number_of_spaces = height - (x + 1)
    for y in range(number_of_spaces):
        print(" ", end="")

    # calculate the number of #'s
    hashtag = 1 + x
    for y in range(hashtag):
        print("#", end="")

    # print two spaces in between
    print("  ", end="")

    # print the other hashes
    for y in range(hashtag):
        print("#", end="")

    # make a space to go to the next line
    print()