/*
Ruchella Kock
12460796

This program prompts the user for a height between 0 and 23 and draws one full pyramid with 2 spaces in between

*/
#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;
    //ask for height and stop if its a number between 23 and 0.. otherwise ask again
    do
    {
        height = get_int("height: ");
    }
    while (height > 23 || height < 0);
    //make a loop that will calculate the number of spaces
    int current_space_number;
    int current_line_number;
    int current_hash_number;


    for (current_line_number = 0; current_line_number < height ; current_line_number++)
    {
        //make a loop that will print the number of spaces calculated above
        int number_of_spaces = (height - (current_line_number + 2));
        for (current_space_number = 0; current_space_number <= number_of_spaces; current_space_number++)
        {
            printf(" ");
        }
        //make a loop that will calculate the number of #'s
        int hash = (current_line_number);
        for (current_hash_number = 0; current_hash_number <= hash; current_hash_number++)
        {
            printf("#");
        }
        //make the spaces between the two pyramids
        for (current_space_number = 0; current_space_number <= 1; current_space_number++)
        {
            printf(" ");
        }
        //make the hash of the second pyrmids
        for (current_hash_number = 0; current_hash_number <= hash; current_hash_number++)
        {
            printf("#");
        }
        //make a space to go to the next line
        printf("\n");
    }
}