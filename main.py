#!/usr/bin/env python3
"""One Star, Written in Sap — make.fun entry.

Writes a single one-line 1-star review, in the voice of a houseplant
reviewing the human who owns it, to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt).

The gate requires UTF-8 text of 1 to 279 characters, not only whitespace,
on a single line. This program self-checks those rules before writing and
re-reads the file after writing to verify the bytes on disk.
"""

import os
import tempfile

ENTRY = (
    "One star. My human waters me like he's apologizing to a plant he "
    "already killed, then parks me in a windowless corner 'for the "
    "aesthetic' and acts betrayed when I start auditioning for compost."
)


def main() -> None:
    text = ENTRY
    if not (1 <= len(text) <= 279):
        raise SystemExit(f"entry is {len(text)} chars, must be 1-279")
    if text.strip() == "":
        raise SystemExit("entry is only whitespace")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    data = (text + "\n").encode("utf-8")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise

    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise SystemExit("verification failed: bytes on disk differ")
    print(f"wrote {path} ({len(text)} chars, 1 line)")


if __name__ == "__main__":
    main()
