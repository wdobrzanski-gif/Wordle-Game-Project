"""
Simple Tkinter app to test that GuessLetter is working correctly.

Author: Dr. Sat Garcia (sat@sandiego.edu)
"""

import json
import tkinter as tk
from views import GuessLetter
from models import LetterState

def main():
    with open("settings.json", 'r') as settings_file:
        settings = json.load(settings_file)

    app = tk.Tk()

    l1 = GuessLetter(app, 0, 0, settings)
    l1.set_letter('S')
    l1.set_status(LetterState.CORRECT)

    settings['ui']['guesses']['letter_font_size'] = 20
    l2 = GuessLetter(app, 0, 1, settings)
    l2.set_letter('A')
    l2.set_status(LetterState.INCORRECT)

    settings['ui']['guesses']['letter_font_size'] = 35
    l3 = GuessLetter(app, 1, 0, settings)
    l3.set_letter('T')
    l3.set_status(LetterState.MISPLACED)

    l4 = GuessLetter(app, 1, 1, settings)
    l4.set_letter('!')

    app.mainloop()


if __name__ == "__main__":
    main()
