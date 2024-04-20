from flask import Flask, render_template, request, redirect

import random

app = Flask(__name__)
WORDFILE = "static/dictionary.txt"

def get_word():
    current_word = None
    words_processed = 0

    with open(WORDFILE, "r") as f:
      for word in f:
          words_processed += 1
          if random.randint(1, words_processed) == 1:
              current_word = word.strip().lower()
    return current_word

def play_game(word):
  word_completion = "_" * len(word)
  guessed = False
  guessed_letters = []
  wrong_guesses = []
  tries = 10

  while not guessed and tries > 0:
    guess = request.form['letter'].lower()
    if len(guess) == 1 and guess.isalpha():
        if guess in guessed_letters:
            message = "You already guessed the letter " + guess
        elif guess not in word:
            message = guess, "is not in the word."
            tries -= 1
            guessed_letters.append(guess)
        else:
            message = "Good job,", guess, "is in the word!"
            guessed_letters.append(guess)
            word_as_list = list(word_completion)
            indices = [i for i, letter in enumerate(word) if letter == guess]
            for index in indices:
                word_as_list[index] = guess
            word_completion = "".join(word_as_list)
            if "_" not in word_completion:
                guessed = True
    elif len(guess) == len(word) and guess.isalpha():
        if guess in guessed_words:
            print("You already guessed the word", guess)
        elif guess != word:
            print(guess, "is not the word.")
            tries -= 1
            guessed_words.append(guess)
        else:
            guessed = True
            word_completion = word
    else:
        print("Not a valid guess.")
    print(display_hangman(tries))
    print(word_completion)
    print("\n")
  if guessed:
    print("Congrats, you guessed the word! You win!")
  else:
    print("Sorry, you ran out of tries. The word was " + word + ". Maybe next time!")
  
@app.route('/')
def index():
    return 'Hello from Flask!'


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
