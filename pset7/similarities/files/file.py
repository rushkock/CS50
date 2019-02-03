import sys
def main():
    make_substring("Hoi")
def make_substring(string):
    n = 4
    if len(string) > n:
        print("No")
        sys.exit()
    i = 0
    j = n
    new_string = string[i : j]
    list_of_strings = []
    while (len(new_string) == n):
        new_string = string[i:j]
        list_of_strings.append(new_string)
        i = i + 1
        j = j + 1
    del list_of_strings[-1]
    print(list_of_strings)

if __name__ == "__main__":
    main()