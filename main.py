import random

from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'super secret key'

WORDFILE = "static/dictionary.txt"

images = [
    'flower0.png', 'flower1.png', 'flower2.png', 'flower3.png', 'flower4.png',
    'flower5.png', 'flower6.png', 'flower7.png', 'flower8.png', 'flower9.png'
]


def get_word():
  current_word = None
  words_processed = 0

  with open(WORDFILE, "r") as f:
    for word in f:
      words_processed += 1
      if random.randint(1, words_processed) == 1:
        current_word = word.strip().lower()
  return current_word


@app.route('/reset', methods=['POST'])
def reset():
  session.clear()  # This clears the session, effectively resetting the game.
  return redirect(
      '/')  # Redirects the user to the main game page to start over.


@app.route('/', methods=['GET', 'POST'])
def user_input():
  if 'word' not in session:
    # Initialize game
    session['word'] = get_word()
    session['word_completion'] = "_" * len(session['word'])  # No spaces
    session['guessed_letters'] = []
    session['guessed_words'] = []
    session['tries'] = 10

  guessed = False
  message = ''

  if request.method == 'POST':
    guess = request.form['letter'].lower()

    if len(guess) == 1 and guess.isalpha():
      if guess in session['guessed_letters']:
        message = "You have already guessed the letter " + guess
      elif guess not in session['word']:
        message = guess + " is not in the word."
        session['tries'] -= 1
        session['guessed_letters'].append(guess)
      else:
        message = "Good job, " + guess + " is in the word!"
        session['guessed_letters'].append(guess)
        # Update word_completion to reflect guessed letter
        word_as_list = list(session['word_completion'])
        indices = [
            i for i, letter in enumerate(session['word']) if letter == guess
        ]
        for index in indices:
          word_as_list[index] = guess
        session['word_completion'] = "".join(word_as_list)
        if "_" not in session['word_completion']:
          guessed = True

    elif len(guess) == len(session['word']) and guess.isalpha():
      if guess in session['guessed_words']:
        message = "You already guessed the word " + guess
      elif guess != session['word']:
        message = guess + " is not the word."
        session['tries'] -= 1
        session['guessed_words'].append(guess)
      else:
        guessed = True
        session['word_completion'] = session['word']

    else:
      message = "Not a valid guess."

    if guessed:
      message = "Congrats, you guessed the word! You win!"
    elif session['tries'] <= 0:
      message = "Sorry, you ran out of tries. The word was " + session[
          'word'] + ". Maybe next time!"

    session.modified = True  # Ensure the session is marked as modified

  return render_template("user_input.html",
                         tab_title="Grow the flower!",
                         page_title="Guess the word before the flower grows!",
                         word_completion=session['word_completion'],
                         message=message,
                         tries=session['tries'],
                         guessed_letters=session['guessed_letters'],
                         guessed_words=session['guessed_words'],
                         word=session['word'])


if __name__ == '__main__':
  app.run()
