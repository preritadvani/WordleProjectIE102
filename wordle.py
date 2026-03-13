import random

WORD_LENGTH = 5
MAX_ATTEMPTS = 6

GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RESET = "\033[0m"


def load_words(filename):
    with open(filename, "r") as f:
        return {line.strip().lower() for line in f if len(line.strip()) == WORD_LENGTH}


def get_feedback(guess, answer):
    result = [""] * WORD_LENGTH
    answer_chars = list(answer)

    # First pass: correct position
    for i in range(WORD_LENGTH):
        if guess[i] == answer[i]:
            result[i] = GREEN + guess[i] + RESET
            answer_chars[i] = None

    # Second pass: misplaced letters
    for i in range(WORD_LENGTH):
        if result[i] == "":
            if guess[i] in answer_chars:
                result[i] = YELLOW + guess[i] + RESET
                answer_chars[answer_chars.index(guess[i])] = None
            else:
                result[i] = GRAY + guess[i] + RESET

    return " ".join(result)


def play():
    answers = list(load_words("answers.txt"))
    allowed = load_words("allowed.txt")

    answer = random.choice(answers)

    print("WORDLE (CLI)")
    print("Guess the 5-letter word")

    for attempt in range(1, MAX_ATTEMPTS + 1):

        while True:
            guess = input(f"\nAttempt {attempt}/{MAX_ATTEMPTS}: ").lower()

            if len(guess) != WORD_LENGTH:
                print("Word must be 5 letters")
                continue

            if guess not in allowed:
                print("Not in word list")
                continue

            break

        feedback = get_feedback(guess, answer)
        print(feedback)

        if guess == answer:
            print("\n🎉 Correct!")
            return

    print(f"\nGame Over! Answer was: {answer}")


if __name__ == "__main__":
    play()
