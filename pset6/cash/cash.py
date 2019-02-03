# Ruchella Kock
# 12460796
# this program will give the least amount of coins that can be given
from cs50 import get_float

while True:
    dollars = get_float("Change owed: ")
    coins = round(dollars * 100)
    # make sure you have a positive amount of change owed if not ask again
    if dollars < 0:
        continue
    else:
        break
change = 0
# determine how many quarters fit in coins
while coins >= 25:
    coins = coins - 25
    change = change + 1

# determine how many dimes fit in coins
while coins >= 10:
    coins = coins - 10
    change = change + 1

# determine how many quarters fit in coins
while coins >= 5:
    coins = coins - 5
    change = change + 1

# determine how many penny's fit in coins
change = change + coins

print(f"{change}")