#!/usr/bin/env python3
"""Build the fork-specific installerMetadata.zip from official dynamic metadata."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import argparse
import json
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CUSTOM_PACKAGE_URL = (
    "https://github.com/aizumanga/07thmod-ch3-uncensor/releases/latest/"
    "download/Tatarigoroshi.Voice.and.Graphics.Patch.zip"
)
REQUIRED_OFFICIAL_FILE = "updates.json"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--official-metadata", type=Path, required=True)
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    package_size = args.package.stat().st_size

    with ZipFile(args.official_metadata) as official_zip:
        names = {Path(name).name: name for name in official_zip.namelist()}
        if REQUIRED_OFFICIAL_FILE not in names:
            raise SystemExit(
                "official metadata is missing {}".format(REQUIRED_OFFICIAL_FILE)
            )
        updates_json = official_zip.read(names[REQUIRED_OFFICIAL_FILE])

    cached_sizes = json.loads(
        (ROOT / "cachedDownloadSizes.json").read_text(encoding="utf-8")
    )
    cached_sizes[CUSTOM_PACKAGE_URL] = package_size

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ch3-metadata-") as temp_dir:
        temp_root = Path(temp_dir)
        (temp_root / "installData.json").write_bytes(
            (ROOT / "installData.json").read_bytes()
        )
        (temp_root / "versionData.json").write_bytes(
            (ROOT / "versionData.json").read_bytes()
        )
        (temp_root / "cachedDownloadSizes.json").write_text(
            json.dumps(cached_sizes, indent=4, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (temp_root / "updates.json").write_bytes(updates_json)

        with ZipFile(args.output, "w", ZIP_DEFLATED) as output_zip:
            for filename in (
                "installData.json",
                "versionData.json",
                "cachedDownloadSizes.json",
                "updates.json",
            ):
                output_zip.write(temp_root / filename, filename)

    print("Built {}".format(args.output))
    print("Custom package size: {}".format(package_size))


if __name__ == "__main__":
    main()
