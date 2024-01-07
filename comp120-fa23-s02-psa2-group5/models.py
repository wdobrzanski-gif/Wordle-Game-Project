import random
from enum import Enum, auto
from typing import Optional


class NotAWordError(ValueError):
    pass


class LetterState(Enum):
    INCORRECT = auto()
    MISPLACED = auto()
    CORRECT = auto()


class WordyModel:

    # instance variables
    word_size: int  # size of the word
    word_list: list[str]  # list of valid words
    word: str  # the "hidden" word

    _hidden_word_letter_positions: dict[str, list[int]]

    def __init__(self, word_size, word_list_filename, preselected_word=None):
        
        self.word_size = word_size # Initialize and assign the word_size attribute with the provided word_size

        self.word_list = [] # Initialize an empty list to store words
        self.set_word_list(word_list_filename) # Call a method to set the word list based on the provided filename

        self.word = None # Initialize the word attribute to None
        self.set_word(preselected_word) # Call a method to set the word based on the optional preselected_word

        self.word_letter_positions = self.letter_positions(self.word) # Calculate and store letter positions for the word

    def set_word_list(self, filename: str) -> None:
        """ Sets the word_list instance variable based on all the words of the
        given size (self.word_size) in the word file with name <filename>.

        Parameters:
            self (WordyModel): The object being modified.
            filename (str): name of the file containing a list of valid words.
        """
        self.word_list = [] #Initialize an empty list to store words

        with open(filename, 'r') as f: # Open the file wit hthe provided filename in read mode
            for word in f: # Iterate through each line (word) in the file
                
                word = word.strip() # Remove leading and trailing whitespaces from the word
                
                if len(word) == self.word_size: # Check if the length of the words matches the desired word size
                    
                    self.word_list.append(word) # If the word has the desired size, add it to the word_list

        if len(self.word_list) == 0: # Check if no words of the desired size were found in the file
            raise RuntimeError(
                f"No words of length {self.word_size} found in {filename}") # If no words of the desired size were found, raise a RuntimeError

    def set_word(self, preselected_word: Optional[str]) -> None:
        """ Sets the word, either to the preselected word or a random one from
        the word list if <preselected_word> is None.

        Parameters:
            preselected_word (str): The word to use for this round of the
                game, or None if a random word is to be selected.

        Raises:
            ValueError: When preselected_word isn't the proper size.
            NotAWordError: When preselected_word is not a valid word.
        """
        if preselected_word is None: # Check if preselected_word is None
            
            self.word = random.choice(self.word_list) # If preselected_word is None, randomly choose a word from the word list
        
        else: # If preselected_word is not None

            if len(preselected_word) != self.word_size: # Check if the length of preselected_word matches the desired word size
                
                raise ValueError("preselected word isn't of the correct size") # If the length is incorrect, raise a ValueError
            
            elif self.word in self.word_list: # Check if preselected_word is in the word list (not a valid conditiion)

                raise NotAWordError("preselected word is not in the word list") # If it is, raise a NotAWordError
            else:
                self.word = preselected_word # Set the word to the preselected_word

    def check_guess(self, guess: str) -> tuple[bool, list[LetterState], dict[str, LetterState]]:
        """ Checks the given <guess> against the answer word, returning three
        things.

        (1) Whether the guess was correct
        (2) A list of LetterState to indicate for each letter in the guess
        whether it was correct, incorrect, or a mistplaced letter.
        (3) A dictionary that associates each letter in the guess with its
        state.

        Parameters:
            guess: (str) The guess to check.
        """
        # Log the guess and the word to a CSV file for record-keeping
        with open('guess_log.csv', 'a') as f: 
            f.write(f'{self.word}, {guess}\n')

        # Check if the guess is a valid word
        if guess not in self.word_list:
            raise NotAWordError

        # prrepare returnh value   ???????

        # Initialize variable to store the result
        is_correct = guess == self.word
        letter_states = [None] * self.word_size
        key_states = {}

        # algorithm

        # Iterate through each letter in the guess and compare with the answer word
        for i in range(self.word_size):
            if guess[i] not in self.word:
                # If the letter is not in the answer word, mark as incorrect
                letter_states[i] = LetterState.INCORRECT
                key_states[guess[i]] = LetterState.INCORRECT
            else:
                if guess[i] != self.word[i]:
                    # If the letter is misplaced, ark as misplaced
                    letter_states[i] = LetterState.MISPLACED
                    key_states[guess[i]] = LetterState.MISPLACED
                else:
                    # If the letter is in the correct position, mark as correct
                    letter_states[i] = LetterState.CORRECT
                    key_states[guess[i]] = LetterState.CORRECT

        # TODO: implement this method and remove this line
        return is_correct, letter_states, key_states # Return the result

    def letter_positions(self, word: str) -> dict[str, list[int]]:
        """ Returns a mapping between letters and the indexes at which the
        letter appears in the word.

        Parameters:
            word: (str) The word to analyze.

        Returns:
            (dict[str, list[int]]) Dictionary mapping character to its
            positions (i.e. indexes) in the given word.
        """
        letter_positions = {} # Initialize an empty dictionary to store letter posititons

        for i in range(len(word)): # Iterate through each character in the word
            letter = word[i] # Get the currect character
            
            # If the letter is already a key in the dictionary, append the currect index to
            # the list of positions for that letter, otherwise create a new key-value pair
            letter_positions.setdefault(letter, []).append(i)
        
        # Return the dictionary mapping characters to their positions in the word
        return letter_positions