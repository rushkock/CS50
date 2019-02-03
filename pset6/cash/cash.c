#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float dollars;
    int coins;
    //Prompt user for change needed and make sure its a value bigger than 0
    //Enters a value smaller than 0 ask again for a new value
    do
    {
        dollars = get_float("Change owed: ");
        coins = round(dollars * 100);
    }
    while (coins < 0);

    int modulo_25 = (coins % 25);
    int modulo_25_10 = (coins % 25 % 10);

    //First if statement will only print the amount of coins needed, if the amount of change can be divided by 25
    if (modulo_25 == 0)
    {
        printf("%i \n", coins / 25);
    }
    //Second if statement will only print the amount of coins needed, if the amount of change can be divided by 25 and 10
    else if (coins % 25 % 10 == 0)
    {
        printf("%i \n", ((coins - modulo_25) / 25) + ((modulo_25) / 10));
    }
    //Third if statement will only print the amount of coins needed, if the amount of change can be divided by 25,10 and 5
    else if (coins % 25 % 10 % 5 == 0)
    {
        printf("%i \n", ((coins - modulo_25) / 25) + ((modulo_25 - modulo_25_10) / 10) + ((modulo_25_10) / 5));
    }
    //Fourth if statement will only print the amount of coins needed, if the amount of change can be divided by 25,10, and 1
    else if (coins % 25 % 10 % 5 % 1 == 0)
    {
        printf("%i \n", ((coins - modulo_25) / 25) + ((modulo_25 - modulo_25_10) / 10) + ((modulo_25_10 - coins % 25 % 10 % 5) / 5) + ((
                    coins % 25 % 10 % 5) / 1));
    }
}