"""
Module: wordy

A completely original word game that will knock your socks off!

Authors:
- Will Dobrzanski - wdobrzanski@sandiego.edu
"""

import string
import json
from typing import Callable
from tkinter import Event

from views import WordyView
from models import WordyModel, NotAWordError


class WordyController:
    """ Controller class for WordyController. """

    WORD_SIZE: int    # number of characters in the correct word
    NUM_GUESSES: int  # number of guesses allowed by the user

    model: WordyModel  # the model used to verify the guess
    view: WordyView    # the GUI view

    # the guess number the user is currently on (starts at 0)
    current_guess_num: int
    current_guess: list[str]  # list of characters in the current guess

    def __init__(self, view: WordyView, model: WordyModel, settings: dict) -> None:
        """ Initialize the controller. """

        self.WORD_SIZE = settings['word_size']
        self.NUM_GUESSES = settings['num_guesses']

        self.model = model

        self.current_guess_num = 0
        self.current_guess = []

        # Create the view
        self.view = view

        # TODO: use the set_key_handler method in your view to set up the
        # event handlers for all of the keyboard keys (A-Z, BACK, ENTER)

        for ch in string.ascii_lowercase:
            self.view.set_key_handler(ch, self.create_letter_handler(ch))

        self.view.set_key_handler('back', self.delete_last_letter)
        self.view.set_key_handler('enter', self.check_solution)
        self.view.create_binding('Control-H', self.show_hint)

        # TODO: use create_binding to set Control-H to show the hint
        # self.view.bind("<Control-h>", self.show_hint)

        # Start GUI
        self.view.start_gui()

    def clear_current_guess(self):
        """ Clears the current guess. """
        for _ in range(len(self.current_guess)):
            self.current_guess.pop()

    def show_hint(self, e: Event):
        """ Secret function to display the answer in the messages frame. """

        self.view.display_message(f'Answer is:{self.model.word}')

    def create_letter_handler(self, letter: str) -> Callable[[], None]:
        """ Creates an event handler function that will.

        (1) Add a letter to the current guess.
        (2) Update the view so that the letter shows up in the appropriate
        spot.

        Note that if the current guess already is already at the WORD_SIZE,
        the handler shouldn't do anything.

        Precondition: letter is a single character.

        Parameters:
            letter (str): The letter to use in the function that is generated.

        Returns:
            Callable[[], None]: A function that will either do the two steps
            above or nothing (if the current guess already has WORD_SIZE
            characters.
        """
        # Define am inner function to update the letter in the current guess
        def update_letter():
            if len(self.current_guess) < self.WORD_SIZE:
                self.current_guess.append(letter)
                self.view.set_letter(
                    letter, self.current_guess_num, len(self.current_guess)-1)
        # Return the inner function as the event handler
        return update_letter


    def delete_last_letter(self) -> None:
        """ An event handler that will delete the last letter from the current
        guess and remove it from the view.

        Note that if the current guess is empty (i.e. doesn't have any
        letters), this handler will do nothing.
        """
        # Check if the current guess is not empty
        if len(self.current_guess) > 0:
            # Remove the last letter from the current guess and the view
            self.view.set_letter('', self.current_guess_num,
                                 len(self.current_guess)-1)
            self.current_guess.pop()

    def check_solution(self) -> None:
        """ Checks the current guess using the wordy model, then updates the
        wordy view to display the result of the guess. This function will act
        as the handler for the "ENTER" button.

        If the current guess doesn't have enough letters, this will do nothing
        except display a message in the view that reads, "Word not finished!".

        If the wordy model indicates that the guess is not a word, this
        function should ONLY display a message in the view that reads, "XXX is
        not a valid word." (where XXX is the guess).

        If the guess was correct, in addition to updating the colors of the
        guess, the view should display a message that reads, "Correct!!! Wordy
        Up, y'all!".

        If the guess was incorrect and was the last available guess, the view
        should display a message that reads, "Darn. You are out of guesses.
        Better luck next time!".

        In the case of a correct guess or running out of guesses, the view's
        game_over method should be called to disable the user from further
        interacting with the keyboard.
        """
        # COnstruct the guess from the current letters
        guess = "".join(self.current_guess)

        # Check if the guess has enough letters
        if len(guess) < self.WORD_SIZE:
            self.view.display_message("Word not finished!")
            return

        try:
            # Check the guess using the wordy model and get the results
            is_correct, guess_word_results, guess_letters_results = self.model.check_guess(
                guess)

        except NotAWordError:
            # Display a message if the guess is not a valid word
            self.view.display_message(f"{guess} is not a valid word.")
            return

        # Display the results of the guess in the view 
        self.view.display_guess_result(
            self.current_guess_num, guess_word_results, guess_letters_results)

        if is_correct:
            # Display a message for a correct guess and end the game
            self.view.display_message("Correct! Nice job. Game over.")
            self.view.game_over

        else:
            # Clear the current guess and move to the next guess
            self.clear_current_guess()
            self.current_guess_num += 1

            if self.current_guess_num == self.NUM_GUESSES:
                # Display a message for running out of guesses and end the game
                self.view.display_guess_result(
                    f"Guesses used up. Word was {self.model.word}. Game over.")
                self.view.game_over


if __name__ == "__main__":
    with open("settings.json", 'r') as settings_file:
        settings = json.load(settings_file)

    # create model, view, then controller
    model = WordyModel(settings['word_size'], settings['word_list_file'])
    view = WordyView(settings)
    controller = WordyController(view, model, settings)
