from utils import *


def strict_match(word: str, pattern: str) -> bool:
    return len(word) == len(pattern) and all(p == '?' or p == w for p, w in zip(pattern, word))


def _ask_continue() -> bool:
    resp = input(f"{fmt('Continue?', 'hint')} {fmt('[Y/n]', 'info')} > ").strip().lower()
    return resp in ("", "y", "yes")


def main():
    print(fmt("Welcome to the Wordle Helper CLI, by AsbestosSoup.", "success"))

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

    try:
        while True:
            pattern = get_validated_input(
                prompt=f"Define a word pattern (use {fmt('?', 'hint')} for unknowns) > "
            )
            if not pattern:
                print(fmt("Goodbye!", "info"))
                break

            include = input(
                f"{fmt('Include letters', 'info')} (e.g., 'ae' or 'oo' for 2 o's, blank for none) > ").strip().lower()
            exclude = input(
                f"{fmt('Exclude letters', 'warning')} (letters not present, blank for none) > ").strip().lower()

            by_len = [w for w in words if len(w) == len(pattern)]
            print(fmt(f"Candidates of length {len(pattern)}: {len(by_len)}", "hint"))

            filtered = [
                w for w in by_len
                if strict_match(w, pattern)
                   and respects_letter_counts(w, include, exclude)
            ]

            if filtered:
                print(fmt(f"Matches: {len(filtered)}", "success"))
                print(fmt(filtered, "info"))
            else:
                print(fmt("No matches found.", "warning"))
            print()

            if not _ask_continue():
                print(fmt("Exiting...", "warning"))
                break
    finally:
        words_file = get_words_file_path()
        if os.path.exists(words_file):
            try:
                os.remove(words_file)
                print(fmt(f"Deleted cached dictionary: {words_file}", "info"))
            except Exception as e:
                print(fmt(f"Could not delete {words_file}: {e}", "error"))

        print(fmt("Goodbye!", "success"))


if __name__ == "__main__":
    main()
