# wordle.py
"""
Simple Wordle Game Engine
Run: python wordle.py
"""

import random

WORD_LENGTH = 5
MAX_ATTEMPTS = 6

# Example word list (replace with larger list if needed)

allowed=[]
with open("allowed.txt") as f:
    allowed = [w.strip() for w in f]
WORD_LIST = allowed

GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"


def choose_word():
    """Select a random word."""
    return random.choice(WORD_LIST)


def validate_guess(guess):
    """Check if guess is valid."""
    return len(guess) == WORD_LENGTH and guess.isalpha()


def get_feedback(guess, target):
    """
    Return colored feedback similar to Wordle.
    Green = correct position
    Yellow = correct letter wrong position
    Gray = not in word
    """
    feedback = []
    target_remaining = list(target)

    # First pass for greens
    for i in range(WORD_LENGTH):
        if guess[i] == target[i]:
            feedback.append(GREEN + guess[i] + RESET)
            target_remaining[i] = None
        else:
            feedback.append(None)

    # Second pass for yellows/grays
    for i in range(WORD_LENGTH):
        if feedback[i] is None:
            if guess[i] in target_remaining:
                feedback[i] = YELLOW + guess[i] + RESET
                target_remaining[target_remaining.index(guess[i])] = None
            else:
                feedback[i] = GRAY + guess[i] + RESET

    return " ".join(feedback)


def play():
    """Main game loop."""
    target = choose_word()
    attempts = 0

    print("Welcome to Wordle (CLI Version)")
    print(f"Guess the {WORD_LENGTH}-letter word!")

    while attempts < MAX_ATTEMPTS:
        guess = input(f"\nAttempt {attempts + 1}/{MAX_ATTEMPTS}: ").lower()

        if not validate_guess(guess):
            print("Invalid guess. Enter a 5-letter word.")
            continue

        attempts += 1
        feedback = get_feedback(guess, target)
        print(feedback)

        if guess == target:
            print("\n🎉 You guessed the word!")
            return

    print(f"\nGame Over! The word was: {target}")


if __name__ == "__main__":
    play()
