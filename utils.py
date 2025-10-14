import os
import re
import sys
from collections import Counter
from urllib.request import urlretrieve

_WORDS_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
_PATTERN_RE = re.compile(r"^[a-z?]{5}$")


def fmt(msg, fmt_type="info"):
    if isinstance(msg, list):
        if not msg:
            msg = "[empty list]"
        elif len(msg) <= 10:
            msg = ", ".join(map(str, msg))
        else:
            msg = ", ".join(map(str, msg[:10])) + f" ... ({len(msg)} total)"
    colors = {
        "error": "\033[91m", "success": "\033[92m", "warning": "\033[93m",
        "info": "\033[94m", "hint": "\033[94m",
    }
    color = colors.get(fmt_type.lower(), "\033[95m")
    reset = "\033[0m"
    suffix = "" if fmt_type.lower() in colors else " (UNKNOWN MSG TYPE)"
    return f"{color}{msg}{reset}{suffix}"


def _app_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def _default_words_path() -> str:
    return os.path.join(_app_dir(), "words.txt")


_WORDS_FILE = os.getenv("WORDS_FILE", _default_words_path())


def get_words_file_path() -> str:
    return _WORDS_FILE


def get_validated_input(prompt: str | None = None) -> str:
    if prompt is None:
        prompt = f"Define a word pattern (use {fmt('?', 'hint')} for unknowns) > "
    while True:
        s = input(prompt).strip().lower()
        if s == "":
            return ""
        if _PATTERN_RE.fullmatch(s):
            return s
        print(fmt("Invalid pattern. Use only a–z and '?', length must be 5.", "warning"))


def _letters_only(s: str) -> str:
    return "".join(ch for ch in s.lower() if ch.isalpha())


def parse_letter_counts(s: str) -> dict[str, int]:
    s = _letters_only(s)
    return Counter(s) if s else {}


def respects_letter_counts(word: str, include: str, exclude: str) -> bool:
    wl = word.lower()
    wc = Counter(wl)
    rc = parse_letter_counts(include)
    ec = parse_letter_counts(exclude)

    for c in rc.keys() & ec.keys():
        if wc[c] != rc[c]:
            return False
    for c in rc.keys() - ec.keys():
        if wc[c] < rc[c]:
            return False
    for c in ec.keys() - rc.keys():
        if wc[c] != 0:
            return False
    return True


_WORDS_CACHE: list[str] | None = None


def load_words() -> list[str]:
    global _WORDS_CACHE, _WORDS_FILE
    if _WORDS_CACHE is not None:
        return _WORDS_CACHE

    target_dir = os.path.dirname(_WORDS_FILE) or "."
    os.makedirs(target_dir, exist_ok=True)

    if not os.path.exists(_WORDS_FILE):
        print(fmt("Word list not found.", "warning"), fmt("Downloading…", "hint"))
        try:
            urlretrieve(_WORDS_URL, _WORDS_FILE)
            print(fmt("Download complete.", "success"))
            print(fmt(f"Saved to: {_WORDS_FILE}", "hint"))
        except Exception:
            fallback = os.path.join(os.getcwd(), "words.txt")
            try:
                urlretrieve(_WORDS_URL, fallback)
                print(fmt("Download complete (fallback).", "success"))
                print(fmt(f"Saved to: {fallback}", "hint"))
                _WORDS_FILE = fallback  # safely reassign here
            except Exception as e2:
                raise RuntimeError(f"Failed to download word list: {e2}")

    with open(_WORDS_FILE, "r", encoding="utf-8", errors="ignore") as f:
        words = [w.strip().lower() for w in f if w.strip() and w[0].isalpha()]

    if not words:
        raise RuntimeError("Word list file is empty or invalid.")

    _WORDS_CACHE = words
    return _WORDS_CACHE
