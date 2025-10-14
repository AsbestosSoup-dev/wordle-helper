from utils import *


def strict_match(word: str, pattern: str) -> bool:
    return len(word) == len(pattern) and all(p == '?' or p == w for p, w in zip(pattern, word))


def main():
    print("Welcome to the Wordle Helper CLI, by AsbestosSoup.")

    try:
        words = load_words()
        print(fmt(f"Loaded {len(words)} words.", "success"))
        print(fmt(f"Dictionary: {get_words_file_path()}", "hint"))
        print()
    except Exception as e:
        print(fmt(str(e), "error"))
        return

    print(fmt("Tip:", "hint"), "Use letters in", fmt("Include", "info"),
          "and", fmt("Exclude", "warning"),
          "to enforce counts; if a letter is in both, its count is exact.")
    print()

    while True:
        pattern = get_validated_input(
            prompt=f"Define a word pattern (use {fmt('?', 'hint')} for unknowns) > "
        )
        if not pattern:
            print(fmt("Goodbye!", "info"))
            break

        include = input(
            f"{fmt('Include letters', 'info')} (e.g., 'ae' or 'oo' for 2 o's, blank for none) > ").strip().lower()
        exclude = input(f"{fmt('Exclude letters', 'warning')} (letters not present, blank for none) > ").strip().lower()
        print()

        by_len = [w for w in words if len(w) == len(pattern)]

        filtered = [
            w for w in by_len
            if strict_match(w, pattern)
               and respects_letter_counts(w, include, exclude)
        ]

        if filtered:
            print(f"Matches: {fmt(f"{len(filtered)}", "success")}")
            print(fmt(filtered, "success"))
        else:
            print(fmt("No matches found.", "warning"))
        print()


if __name__ == "__main__":
    main()
