import sys

def get_twenties(amount):
    twentyBills = 0
    while True:
        if amount < 20:
            break
        amount -= 20
        twentyBills += 1
    return twentyBills

def get_tens(amount):
    bills = 0
    while True:
        if amount < 10:
            break
        amount -= 10
        bills += 1
    return bills

def get_fives(amount):
    bills = 0
    while True:
        if amount < 5:
            break
        amount -= 5
        bills += 1
    return bills

def get_ones(amount):
    bills = 0
    while True:
        if amount < 1:
            break
        amount -= 1
        bills += 1
    return bills

def get_quarters(amount):
    coins = 0
    while True:
        if amount < 0.25:
            break
        amount -= 0.25
        coins += 1
    return coins

def get_dimes(amount):
    coins = 0
    while True:
        if amount < 0.10:
            break
        amount -= 0.10
        coins += 1
    return coins

def get_nickels(amount):
    coins = 0
    while True:
        if amount < 0.05:
            break
        amount -= 0.05
        coins += 1
    return coins

def get_pennies(amount):
    coins = 0
    while True:
        if amount < 0.01:
            break
        amount -= 0.01
        coins += 1
    return coins

if __name__ == '__main__':
    changeStr = input("Provide an amount in change (<=$100): $")
    change = float(changeStr)

    if change > 100:
        print("Error: Amount too large")
        sys.exit()

    twenties = get_twenties(change)
    change = change - (twenties * 20)

    tens = get_tens(change)
    change = change - (tens * 10)

    fives = get_fives(change)
    change = change - (fives * 5)

    ones = get_ones(change)
    change = change - ones

    quarters = get_quarters(change)
    change = change - (quarters * 0.25)

    dimes = get_dimes(change)
    change = change - (dimes * 0.10)

    nickels = get_nickels(change)
    change = change - (nickels * 0.05)

    pennies = get_pennies(change)
    change = change - (pennies * 0.01)

    print("Change to give back:")
    print("\tTwenties($20): " + str(twenties))
    print("\tTens($10): " + str(tens))
    print("\tFives($5): " + str(fives))
    print("\tOnes($1): " + str(ones))
    print("\tQuarters(25¢): " + str(quarters))
    print("\tDimes(10¢): " + str(dimes))
    print("\tNickels(5¢): " + str(nickels))
    print("\tPennies(1¢): " + str(pennies))
