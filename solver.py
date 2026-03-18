from itertools import product
from collections import defaultdict

WORD_LENGTH = 5
GREEN, YELLOW, GRAY = "G", "Y", "X"  # X = gray

def load_words(filename):
    with open(filename, "r") as f:
        return {line.strip().lower() for line in f if len(line.strip()) == WORD_LENGTH}

def get_pattern(guess, answer):
    """Returns a tuple like ('G','Y','X','G','X') for a guess/answer pair."""
    result = [""] * WORD_LENGTH
    answer_chars = list(answer)

    # First pass: greens
    for i in range(WORD_LENGTH):
        if guess[i] == answer[i]:
            result[i] = GREEN
            answer_chars[i] = None

    # Second pass: yellows and grays
    for i in range(WORD_LENGTH):
        if result[i] == "":
            if guess[i] in answer_chars:
                result[i] = YELLOW
                answer_chars[answer_chars.index(guess[i])] = None
            else:
                result[i] = GRAY

    return tuple(result)

def compute_pattern_counts(allowed_file="allowed.txt", answers_file="answers.txt"):
    allowed = load_words(allowed_file)
    answers = load_words(answers_file)

    # All 243 possible patterns
    all_patterns = list(product([GREEN, YELLOW, GRAY], repeat=WORD_LENGTH))

    print(f"Loaded {len(allowed)} allowed words, {len(answers)} answers")
    print(f"Computing pattern counts for each guess word...\n")

    # For each guess word, count how many answers produce each pattern
    results = {}

    for idx, guess in enumerate(sorted(allowed)):
        pattern_counts = defaultdict(int)

        for answer in answers:
            pattern = get_pattern(guess, answer)
            pattern_counts[pattern] += 1

        # Store all 243 patterns (0 if never occurs)
        results[guess] = {p: pattern_counts[p] for p in all_patterns}

        if (idx + 1) % 500 == 0:
            print(f"Processed {idx + 1} words...")

    return results, all_patterns

def print_summary(results, all_patterns, top_n=5):
    """Print a summary for top_n words."""
    print(f"\n{'='*60}")
    print(f"Sample output for first {top_n} words:")
    print(f"{'='*60}")

    for word in list(sorted(results.keys()))[:top_n]:
        print(f"\nWord: {word.upper()}")
        counts = results[word]
        # Only show non-zero patterns
        non_zero = {p: c for p, c in counts.items() if c > 0}
        print(f"  Non-zero patterns: {len(non_zero)} / 243")
        # Show top 3 most common patterns
        top = sorted(non_zero.items(), key=lambda x: -x[1])[:3]
        for pattern, count in top:
            print(f"  {''.join(pattern)} -> {count} answers")

def save_results(results, all_patterns, output_file="pattern_counts.csv"):
    """Save full results to CSV."""
    import csv
    pattern_labels = ["".join(p) for p in all_patterns]

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["word"] + pattern_labels)

        for word in sorted(results.keys()):
            row = [word] + [results[word][p] for p in all_patterns]
            writer.writerow(row)

    print(f"\nFull results saved to {output_file}")
    print(f"Shape: {len(results)} words x 243 patterns")

if __name__ == "__main__":
    results, all_patterns = compute_pattern_counts()
    print_summary(results, all_patterns)
    save_results(results, all_patterns)
