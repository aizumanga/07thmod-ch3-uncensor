#!/usr/bin/env python3
"""Static validation for the narrowly gated Chapter 3 sprite-call variant."""

from collections import Counter
from pathlib import Path
import struct
import sys


ROOT = Path(__file__).resolve().parents[1]
TARGET_SCRIPT = ROOT / "Update" / "tata_013_02.txt"
SPRITE_NAMES = {
    "sa_tn_bi_a1": 2,
    "sa_tn_hn_a1": 3,
    "sa_tn_sa_a1": 4,
}
EXPECTED_SIZE = (1280, 960)
MARKER = "CH3_UNCENSOR_GUARD:"


def fail(message):
    print("ERROR: {}".format(message), file=sys.stderr)
    return 1


def png_size(path):
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("not a PNG with an IHDR header")
    return struct.unpack(">II", data[16:24])


def main():
    errors = 0
    script = TARGET_SCRIPT.read_text(encoding="utf-8-sig")

    if script.count(MARKER) != 9:
        errors += fail("expected 9 guarded call-site markers")

    if script.count("if (GetGlobalFlag(GCensor) == 0) {") != 9:
        errors += fail("each call site must have an explicit GCensor == 0 guard")

    if script.count("if (GetGlobalFlag(GArtStyle) == 2) {") != 9:
        errors += fail("each call site must have an explicit Original-art guard")

    actual_calls = Counter()
    for name in SPRITE_NAMES:
        actual_calls[name] = script.count('"{}"'.format(name))
    if actual_calls != Counter(SPRITE_NAMES):
        errors += fail(
            "unexpected target call counts: expected {}, got {}".format(
                dict(SPRITE_NAMES), dict(actual_calls)
            )
        )

    for path in (ROOT / "Update").glob("*.txt"):
        if path == TARGET_SCRIPT:
            continue
        text = path.read_text(encoding="utf-8-sig")
        for name in SPRITE_NAMES:
            if name in text:
                errors += fail("{} leaked into {}".format(name, path.relative_to(ROOT)))

    for name in SPRITE_NAMES:
        sprite = ROOT / "OGSprites" / "{}.png".format(name)
        if not sprite.is_file():
            errors += fail("missing placeholder {}".format(sprite.relative_to(ROOT)))
            continue
        try:
            size = png_size(sprite)
        except ValueError as exc:
            errors += fail("{}: {}".format(sprite.relative_to(ROOT), exc))
            continue
        if size != EXPECTED_SIZE:
            errors += fail(
                "{} must be {}x{}, got {}x{}".format(
                    sprite.relative_to(ROOT),
                    EXPECTED_SIZE[0],
                    EXPECTED_SIZE[1],
                    size[0],
                    size[1],
                )
            )

    if errors:
        return 1

    print("Chapter 3 patch validation passed.")
    print("Guarded call sites: 9")
    print("Target calls: {}".format(dict(actual_calls)))
    print("Placeholder sprites: 3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
