#include <iostream>

using namespace std;

void getValidGuess(char&, vector<char>, string, int, string);

//Ask the user and get a valid guess
void getValidGuess(char &userguess, vector<char> userguesses, string guess, int miss, string errMsg)
{
    string guessedString;

    clearScreen();
    printMan(miss);
    cout << endl;
    cout << guess << "   " << errMsg << endl;
    errMsg = ""; //Reset the Error State

    cout << "Enter Guess [a ~ z]: ";
    cin >> guessedString;
    cout << endl;

    if (!isOneCharLong(guessedString)) //Check if the input is one character long
    {
        errMsg = "Guess has to be one character long!";
        getValidGuess(userguess, userguesses, guess, miss, errMsg);
    }
    else
    {
        userguess = guessedString[0];
        if (!isalpha(userguess)) //Check if it is an alphabet
        {   
            errMsg = "Guess has to be an alphabet!";
            getValidGuess(userguess, userguesses, guess, miss, errMsg);
        }
        else
        {
            if (guessedAlready(userguess, userguesses)) //Check if the guess hasn't been guessed already
            {
                errMsg += userguess;
                errMsg += " has been guessed already";
                getValidGuess(userguess, userguesses, guess, miss, errMsg);
            }
        }
    }
}