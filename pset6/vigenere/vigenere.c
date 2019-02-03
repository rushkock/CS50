/*
Ruchella Kock
12460796

This programs takes an alphabetical key in the command line argument 1, it uses this key to encipher a word the user fills in

*/

#include <cs50.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define A 65
#define a 97
// function to encipher each character of a string
int cipher(char each_character, char each_key_character, int x, int y)
{
    int alphabetical_value_key = (int) each_key_character - x;
    int alphabetical_value = (int) each_character - y;
    int alphabetical_cipher = (alphabetical_value + alphabetical_value_key) % 26;
    int ASCII = (alphabetical_cipher + y);
    printf("%c", ASCII);
    return ASCII;
}

int main(int argc, string argv[])
{
    // program will stop if 1 or more than 2 arguments are filled in command line
    if (argc == 1 || argc > 2)
    {
        printf("Error\n");
        return 1;
    }

    // program will not run if there is an integer in the key
    string key = argv[1];
    for (int i = 0, num = strlen(key); i < num; i++)
    {
        if (isdigit(key[i]))
        {
            printf("Error\n");
            return 1;
        }
    }

    // prompt user for a string to encipher
    string plain_text = get_string("plaintext: ");
    printf("ciphertext: ");

    // iterate over each character of the string the user filled in
    for (int i = 0, j = 0, n = strlen(plain_text); i < n; i++)
    {
        char each_character = (plain_text[i]);
        // if the character of the string is upper case then determine if key is upper case or lower case
        if (isupper(each_character))
        {
            // depending on whether key is upper or lower case the parameters of function cipher changes
            char each_key_character = (key[j % strlen(key)]);
            if (isupper(each_key_character))
            {
                cipher(each_character, each_key_character, A, A);
                j++;
            }
            if (islower(each_key_character))
            {
                cipher(each_character, each_key_character, a, A);
                j++;
            }
        }
        // if the character of the string is lower case then determine if key is upper case or lower case
        else if (islower(each_character))
        {
            char each_key_character = (key[j % strlen(key)]);
            // depending on whether key is upper or lower case the parameters of function cipher changes
            if (islower(each_key_character))
            {
                cipher(each_character, each_key_character, a, a);
                j++;
            }
            else if (isupper(each_key_character))
            {
                cipher(each_character, each_key_character, A, a);
                j++;
            }
        }
        // if the character is not an alphabetical value then print that character
        else if (isalpha(each_character) != 1)
        {
            printf("%c", each_character);
        }
    }
    printf("\n");
}