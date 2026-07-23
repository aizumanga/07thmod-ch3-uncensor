#!/usr/bin/env python3
"""Verify that the installer fork remains narrowly scoped and clearly credited."""

from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parents[1]
CUSTOM_PACKAGE_URL = (
    "https://github.com/aizumanga/07thmod-ch3-uncensor/releases/latest/"
    "download/Tatarigoroshi.Voice.and.Graphics.Patch.zip"
)
CUSTOM_METADATA_URL = (
    "https://github.com/aizumanga/07thmod-ch3-uncensor/releases/latest/"
    "download/installerMetadata.zip"
)
CUSTOM_SCRIPT_VERSION = "6.1.5-ch3u2"
SPRITE_NAMES = ("sa_tn_bi_a1", "sa_tn_hn_a1", "sa_tn_sa_a1")


def fail(errors, message):
    errors.append(message)
    print("ERROR: {}".format(message), file=sys.stderr)


def find_mod(data, mod_name):
    return next(mod for mod in data["mods"] if mod["name"] == mod_name)


def find_submod(mod, submod_name):
    return next(submod for submod in mod["submods"] if submod["name"] == submod_name)


def find_version(data, target_id):
    return next(item for item in data if item["id"] == target_id)


def main():
    errors = []

    install_data = json.loads((ROOT / "installData.json").read_text(encoding="utf-8"))
    tatarigoroshi = find_mod(install_data, "Tatarigoroshi Ch.3")
    full = find_submod(tatarigoroshi, "full")
    script_file = next(item for item in full["files"] if item["name"] == "script")
    if script_file["url"] != CUSTOM_PACKAGE_URL:
        fail(errors, "Tatarigoroshi full/script does not use the custom package URL")

    serialized_install_data = json.dumps(install_data)
    if serialized_install_data.count(CUSTOM_PACKAGE_URL) != 1:
        fail(errors, "custom package URL must appear exactly once in installData.json")

    version_data = json.loads((ROOT / "versionData.json").read_text(encoding="utf-8"))
    full_version = find_version(version_data, "Tatarigoroshi Ch.3/full")
    script_version = next(
        item["version"] for item in full_version["files"] if item["id"] == "script"
    )
    if script_version != CUSTOM_SCRIPT_VERSION:
        fail(errors, "custom script version must be {}".format(CUSTOM_SCRIPT_VERSION))

    cached_sizes = json.loads(
        (ROOT / "cachedDownloadSizes.json").read_text(encoding="utf-8")
    )
    if cached_sizes.get(CUSTOM_PACKAGE_URL, 0) <= 0:
        fail(errors, "cachedDownloadSizes.json is missing the custom package")

    common_text = (ROOT / "common.py").read_text(encoding="utf-8")
    if CUSTOM_METADATA_URL not in common_text:
        fail(errors, "common.py does not use the fork-specific metadata URL")
    if "api.github.com/repos/aizumanga/07thmod-ch3-uncensor/releases" not in common_text:
        fail(errors, "common.py does not check this fork for installer updates")

    target_script = (
        ROOT / "chapter3-overlay" / "Update" / "tata_013_02.txt"
    ).read_text(encoding="utf-8-sig")
    for sprite_name in SPRITE_NAMES:
        if sprite_name not in target_script:
            fail(errors, "{} is not referenced by the target script".format(sprite_name))
        sprite_path = (
            ROOT / "chapter3-overlay" / "OGSprites" / "{}.png".format(sprite_name)
        )
        if not sprite_path.is_file():
            fail(errors, "missing source sprite {}".format(sprite_path.relative_to(ROOT)))

    credit_sources = {
        "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
        "THIRD_PARTY_NOTICES.md": (ROOT / "THIRD_PARTY_NOTICES.md").read_text(
            encoding="utf-8"
        ),
        "httpGUI/index.html": (ROOT / "httpGUI" / "index.html").read_text(
            encoding="utf-8"
        ),
        "httpGUI/installer.html": (ROOT / "httpGUI" / "installer.html").read_text(
            encoding="utf-8"
        ),
        "main.py": (ROOT / "main.py").read_text(encoding="utf-8"),
        "github_actions_changelog_template.md": (
            ROOT / "github_actions_changelog_template.md"
        ).read_text(encoding="utf-8"),
    }
    for path, text in credit_sources.items():
        lowered = text.lower()
        if "07th-mod" not in lowered or "vibe-coded" not in lowered:
            fail(errors, "{} must visibly credit 07th-Mod and disclose vibe-coding".format(path))

    if errors:
        print("\nFork configuration validation failed with {} error(s).".format(len(errors)))
        return 1

    print("Fork configuration validation passed.")
    print("Custom package URL occurrences: 1")
    print("Custom script version: {}".format(CUSTOM_SCRIPT_VERSION))
    print("Editable source sprites: {}".format(len(SPRITE_NAMES)))
    print("Credit surfaces checked: {}".format(len(credit_sources)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
