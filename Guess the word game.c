#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <ctype.h>

#define MAX_TRIES 6
#define WORD_COUNT 10
#define MAX_WORD_LEN 20
int i;
/* * Function to display the current state of the word
 * masked_word: The word with guessed letters revealed and others as underscores
 */
void printWordState(char *masked_word) {
    printf("\nWord: ");
    
    for (i = 0; masked_word[i] != '\0'; i++) {
        printf("%c ", masked_word[i]);
    }
    printf("\n");
}

/*
 * Main game logic
 */
int main() {
    // 1. Data Initialization
    char wordList[WORD_COUNT][MAX_WORD_LEN] = {
        "COMPUTER", "PROGRAMMING", "LANGUAGE", "VARIABLE", 
        "POINTER", "FUNCTION", "COMPILE", "MEMORY", 
        "SYNTAX", "ALGORITHM"
    };

    char secretWord[MAX_WORD_LEN];
    char maskedWord[MAX_WORD_LEN];
    int wrongGuesses = 0;
    int wordLength;
    int letterFound;
    int gameWon = 0;
    
    // Seed the random number generator
    srand(time(NULL));

    // 2. Select a random word
    int randomIndex = rand() % WORD_COUNT;
    strcpy(secretWord, wordList[randomIndex]);
    wordLength = strlen(secretWord);

    // Initialize masked word with underscores
    for (i = 0; i < wordLength; i++) {
        maskedWord[i] = '_';
    }
    maskedWord[wordLength] = '\0';

    printf("Welcome to 'Guess the Word' (C Project)\n");
    printf("You have %d attempts to guess the word.\n", MAX_TRIES);

    // 3. Main Game Loop
    while (wrongGuesses < MAX_TRIES && !gameWon) {
        printWordState(maskedWord);
        printf("Attempts remaining: %d\n", MAX_TRIES - wrongGuesses);
        printf("Enter a letter: ");

        char guess;
        scanf(" %c", &guess);
        guess = toupper(guess); // Handle case sensitivity

        letterFound = 0;

        // Check if the guessed letter exists in the secret word
        for (i = 0; i < wordLength; i++) {
            if (secretWord[i] == guess) {
                if (maskedWord[i] == '_') {
                    maskedWord[i] = guess;
                    letterFound = 1;
                } else {
                    // Letter already guessed correctly previously
                    letterFound = 2; 
                }
            }
        }

        // 4. Update Game State
        if (letterFound == 1) {
            printf("Good job! '%c' is in the word.\n", guess);
        } else if (letterFound == 2) {
            printf("You already guessed '%c'. Try another.\n", guess);
        } else {
            printf("Sorry, '%c' is not there.\n", guess);
            wrongGuesses++;
        }

        // Check if user has won
        if (strcmp(secretWord, maskedWord) == 0) {
            gameWon = 1;
        }
    }

    // 5. End Game Result
    if (gameWon) {
        printWordState(maskedWord);
        printf("\nCONGRATULATIONS! You guessed the word: %s\n", secretWord);
    } else {
        printf("\nGAME OVER. You ran out of tries.\n");
        printf("The word was: %s\n", secretWord);
    }

    return 0;
}
