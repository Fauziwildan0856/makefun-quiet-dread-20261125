"""Publish one code review comment as entry.txt.

The program writes a single-line code review comment that approves a
pull request with quiet existential dread to
$MAKEFUN_OUTPUT_DIR/entry.txt, then reads it back to prove the file
holds exactly the comment. Only the Python standard library is used.
"""

import os
import sys

# Gate from the kit: the comment must be 1 to MAX_CHARS characters, one line.
MAX_CHARS = 140

ENTRY = "LGTM. The code works, the tests pass, and none of us will remember why any of this exists in six months. Approved."


def main():
    if "\n" in ENTRY or "\r" in ENTRY:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if not 1 <= len(ENTRY) <= MAX_CHARS:
        print("entry must be 1 to %d characters" % MAX_CHARS, file=sys.stderr)
        return 1
    if ENTRY != ENTRY.strip():
        print("entry must not have leading or trailing whitespace", file=sys.stderr)
        return 1
    if not any(ch.isalnum() for ch in ENTRY):
        print("entry must contain at least one letter or digit", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(ENTRY)
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != ENTRY:
        print("read-back mismatch", file=sys.stderr)
        return 1
    print("entry OK:", len(ENTRY), "characters (max %d)" % MAX_CHARS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
