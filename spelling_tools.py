#!.venv/bin/python
"""
Creates `new_words.txt` with words that failed a spellcheck.

If the `--merge` flag is given, the content of that file is merged in the
spelling dictionary instead.

Run `make spelling` to run the actual spellcheck.
"""
import argparse
import sys
from collections import Counter
from pathlib import Path
from typing import List
from typing import Optional


*_, EPILOG = __doc__.strip().split("\n")
DESCRIPTION = "\n".join(_)

BASE_PATH = Path(__file__).parent.absolute()
NEW_WORDS_FILE = BASE_PATH / "new_words.txt"
SPELLCHECK_DIR = BASE_PATH / "build/spelling"
WORDLIST_FILE = BASE_PATH / "source/dict.txt"


def get_misspelled_words(error_dir: Path) -> Counter:
    """Return counter for misspelled words form files in *error_dir*."""
    words = Counter()
    for error_file in (e for e in error_dir.glob("*.spelling")):
        lines = error_file.read_text().split("\n")
        for line in (line for l in lines if (line := l.strip())):
            try:
                word = line.split("(")[1].split(")")[0]
            except IndexError:
                print("failed to parse line: {line}", file=sys.stderr)
                continue
            words[word] += 1
    return words


def merge_wordfiles(*files: List[Path], out_file: Optional[Path] = None) -> List:
    """Combine words form *files*, return sorted results and write to *out_file* if set."""
    words = set()
    for wordfile in (f for f in files if f.exists()):
        with wordfile.open() as f:
            for line in (line for l in f if (line := l.strip())):
                words.add(line)
    words = sorted(words, key=lambda word: (word.lower(), word))
    if out_file is not None:
        out_file.write_text("\n".join(words) + "\n")
    return words


def write_errors_to_newlist(error_dir: Path, outfile: Path) -> Counter:
    """Write errors found in *error_dir* to *outfile*, sorted by hit count."""
    if not (error_dir.exists() and error_dir.is_dir()):
        raise ValueError(f"'{error_dir}' not found")
    error_counter = get_misspelled_words(error_dir)
    outfile.write_text("\n".join((t[0] for t in error_counter.most_common())))
    return error_counter


def merge_newlist_to_wordlist(newlist: Path, wordlist: Path) -> List:
    """Merge *newlist* to *wordlist* and return the results."""
    if not (newlist.exists() and newlist.is_file()):
        raise ValueError(f"'{newlist}' not found")
    return merge_wordfiles(newlist, wordlist, out_file=wordlist)


def get_args(argv=None):
    ap = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
    ap.add_argument(
        "--merge", action="store_true", help="merge new words to dictionary"
    )
    return ap.parse_args(argv)


def main(
    merge=False,
    newlist: Path = NEW_WORDS_FILE,
    wordlist: Path = WORDLIST_FILE,
    error_dir: Path = SPELLCHECK_DIR,
):
    """
    Write errors found in *error_dir* to *newlist*, sorted by hit count.

    Or merge *newlist* to *wordlist* instead, if *merge* is set.
    """
    if merge:
        try:
            words = merge_newlist_to_wordlist(newlist, wordlist)
            print(f"Wrote {len(words)} words to dictionary '{wordlist}'.")
        except ValueError:
            print(
                f"[ERROR] no wordlist found in '{newlist}'.\n",
                "You can run without the `--merge` flag, to create it.",
                file=sys.stderr,
            )
            return 4
    else:
        try:
            error_counter = write_errors_to_newlist(error_dir, newlist)
            print(
                f"Found {len(error_counter)} unique words in a total of "
                f"{sum(error_counter.values())} misspelled words."
            )
        except ValueError:
            print(
                f"[ERROR] no spellcheck results found in '{error_dir}'.\n",
                "You can run `make spelling` to create them.",
                file=sys.stderr,
            )
            return 3

    return 0


if __name__ == "__main__":
    args = get_args()
    sys.exit(main(**vars(args)))
