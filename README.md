# Higurashi Chapter 3 Original-Art Variant

> [!IMPORTANT]
> This is an **unofficial, vibe-coded fork**. The installer infrastructure,
> original mod, engine changes, scripts, voices, graphics packages, and nearly
> all of the work used here were created and maintained by the
> [07th-Mod team](https://github.com/07th-mod). This project only replaces the
> Tatarigoroshi full-patch script package with a narrowly scoped variant.

This repository combines the 07th-Mod `python-patcher` with a custom
Tatarigoroshi Chapter 3 package. The alternate sprite calls are active only
when both of these options are selected:

- censorship level `0` (`GCensor == 0`);
- **Original/Ryukishi art** (`GArtStyle == 2`).

Every other censorship level and art set continues to use the upstream
07th-Mod behavior. Steam/MangaGamer, console, and remake sprites are not
replaced.

## Installation

### Complete installer

Download the installer for your operating system from this repository's
[latest release](https://github.com/aizumanga/07thmod-ch3-uncensor/releases/latest).
It installs the normal 07th-Mod components and downloads this repository's
custom Chapter 3 script package in place of the upstream Tatarigoroshi script
package.

The installer UI deliberately retains the 07th-Mod identity because its
infrastructure and almost all installed content are theirs. A prominent notice
identifies this fork as unofficial and vibe-coded.

### Manual update for an existing 07th-Mod installation

If Chapter 3 is already patched with 07th-Mod, you do not need to reinstall it:

1. Download `Tatarigoroshi.Voice.and.Graphics.Patch.zip` from the
   [latest release](https://github.com/aizumanga/07thmod-ch3-uncensor/releases/latest).
2. Close the game.
3. Extract the archive into the **Tatarigoroshi game directory**, allowing it
   to overwrite existing files.
4. Start the game and select censorship level 0 plus Original/Ryukishi art.

The archive uses the same layout as the upstream full script package. A later
repair or reinstall performed with the official installer can restore the
official script; reapply this package or run this forked installer if that
happens.

## Editing the custom sprites

The editable source files are:

- `chapter3-overlay/OGSprites/sa_tn_bi_a1.png`
- `chapter3-overlay/OGSprites/sa_tn_hn_a1.png`
- `chapter3-overlay/OGSprites/sa_tn_sa_a1.png`

After installation, the active copies are in the Tatarigoroshi game directory:

```text
HigurashiEp03_Data/StreamingAssets/OGSprites/sa_tn_bi_a1.png
HigurashiEp03_Data/StreamingAssets/OGSprites/sa_tn_hn_a1.png
HigurashiEp03_Data/StreamingAssets/OGSprites/sa_tn_sa_a1.png
```

Keep each file as a `1280x960` PNG with the same filename. Editing the installed
copies is convenient for quick testing; editing the files under
`chapter3-overlay/OGSprites` is what changes future release packages.

## What is custom here

- nine guarded call sites in
  `chapter3-overlay/Update/tata_013_02.txt`;
- three currently clothed placeholder sprites under
  `chapter3-overlay/OGSprites`;
- one Tatarigoroshi `full/script` URL in `installData.json`;
- fork-specific metadata and release automation;
- visible unofficial/vibe-coded notices in the GUI, terminal, documentation,
  and release notes.

The custom script version is `6.1.5-ch3u1`. It intentionally differs from the
upstream `6.1.5` value so an existing official installation is offered the
custom script update.

## Validation and development

Run the fork checks with:

```bash
python3 chapter3-overlay/tools/validate_ch3_patch.py
python3 tools/verify_fork_configuration.py
```

Tags build the Chapter 3 package, Windows/Linux/macOS installers, and the
fork-specific `installerMetadata.zip` into one draft GitHub release.

The imported patcher revision is recorded in
`UPSTREAM_PYTHON_PATCHER_COMMIT`. Use the **Import/update python-patcher**
workflow to refresh it; the workflow reapplies the small patch stored in
`fork-overrides/python-patcher.patch`.

## Credits and status

All credit for the patching infrastructure and original mod belongs to the
[07th-Mod team](https://github.com/07th-mod), including the upstream
[`python-patcher`](https://github.com/07th-mod/python-patcher) and
[`tatarigoroshi`](https://github.com/07th-mod/tatarigoroshi) projects.

This fork is unofficial and is not affiliated with or endorsed by 07th-Mod,
07th Expansion, MangaGamer, or the Higurashi copyright holders. Fork-specific
issues should be reported in this repository rather than to the 07th-Mod team.

This version was **vibe-coded with substantial AI assistance**. Its glue code,
automation, documentation, and scoped script edits were produced through a
ChatGPT/Codex-assisted workflow and checked with automated validation. See
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) for provenance details.
