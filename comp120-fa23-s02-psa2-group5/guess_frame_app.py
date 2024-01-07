"""
Simple Tkinter app to test that GuessesFrame is working correctly.

Author: Dr. Sat Garcia (sat@sandiego.edu)
"""

import json
import tkinter as tk
from views import GuessesFrame
from models import LetterState

def main():
    with open("settings.json", 'r') as settings_file:
        settings = json.load(settings_file)

    settings['word_size'] = 3
    settings['num_guesses'] = 4

    app = tk.Tk()

    gf = GuessesFrame(app, settings)

    # set first guess to win
    gf.set_letter("W",0,0)
    gf.set_letter("I",0,1)
    gf.set_letter("N",0,2)

    # set second guess to moo
    gf.set_letter("M",1,0)
    gf.set_letter("O",1,1)
    gf.set_letter("O",1,2)

    # set one letter in third guess
    gf.set_letter("Q",2,0)

    # show guess results for two guesses
    gf.show_guess_result(0, [LetterState.INCORRECT, LetterState.CORRECT, LetterState.MISPLACED])
    gf.show_guess_result(1, [LetterState.CORRECT, LetterState.CORRECT, LetterState.INCORRECT])

    app.mainloop()


if __name__ == "__main__":
    main()
