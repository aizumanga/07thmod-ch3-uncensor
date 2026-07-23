# Higurashi Chapter 3 Original-Art Script Variant

This is a small overlay/build repository based on the official 07th-Mod
**Tatarigoroshi v6.1.5** scripts. The installer itself does not own the scene
scripts, so keeping this as a Chapter 3 package overlay avoids maintaining an
unrelated full copy of `python-patcher`.

The build workflow checks out the pinned upstream release, applies only the
files stored here, compiles the scripts using `higurashi-assembly`, and emits
the same complete package format expected by the patcher. This preserves the
current voice, ADV/NVL, lip-sync, art-set, audio, censorship, and
installer-facing behavior.

The alternate calls in `Update/tata_013_02.txt` are enabled only when both
conditions are true:

- censorship level is `0` (`GCensor == 0`);
- the selected art set is **Original** (`GArtStyle == 2`).

Every other combination—including Console, Remake/Steam/MangaGamer graphics
and censorship levels 1–5—uses the unchanged v6.1.5 calls.

The three currently included files named `sa_tn_bi_a1`, `sa_tn_hn_a1`, and
`sa_tn_sa_a1` are fully clothed placeholder sprites for integration testing.
They deliberately share a known-good, safe original-art image until final
non-explicit replacements are available.

The older `tata_013_02.txt` supplied as a reference was used only to locate the
nine historical call sites. It was not copied over the modern script.

Run the repository-specific validation with:

```bash
python3 tools/validate_ch3_patch.py
```

Every push and pull request also compiles a complete package and stores it as a
workflow artifact. A version tag creates a draft GitHub release.

## Patcher integration

Once a release asset is available from a URL that the installer can access,
the matching `script` URL for **Tatarigoroshi Ch.3/full** in
`python-patcher/installData.json` can point to this package. A private GitHub
release is not directly downloadable by the unmodified patcher, so the
repository must be public or the asset must be hosted at another public URL
before end-user installer integration is enabled.

## Upstream project information

# PS3 Voice and Graphics Patch
#### For Higurashi No Naku Koro Ni - Chapter 3 Tatarigoroshi

> This repository **only** hosts the script files and a few voice files needed to fix bugs, check our [wiki](https://07th-mod.com/wiki/Higurashi/Higurashi-Getting-started) for instructions on how to install the patch!

This patch aims to combine the efforts of the ps3 voice patch and the ps3 sprites/background patch, and fill in missing voice files not covered by the original voice patch.

# Installing the patch

> [Check our wiki](https://07th-mod.com/wiki/).

# Releases

https://github.com/07th-mod/tatarigoroshi/releases/

This repository is in constant change. Sometimes new releases might get on hold until there is enough content to push a new patch. If the latest patch has a bug that seems to be already fixed in the repository, try downloading the master file. The master file will always have the latest files, regardless of the current release being outdated or not.

# Developing with us

Usually, older contributors are welcome to join the repository and push their own changes without supervision. However, you can also aid the development just by forking the repository and working on your own changes. After you are done, commit the changes, make a pull request and if it's good enough, the changes will be merged. Both approaches are more than welcome!

# Credits

- @DoctorDiablo - For making the graphics mod
- @enumag - For coding the new automation script
- @Grelo - For inserting the CGs and weather sprites
- Anon - For giving us the PS3 files and scripts
