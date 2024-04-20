import random

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