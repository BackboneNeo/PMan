# PMan downstream changelog

This file records BackboneNeo downstream changes only. For PartCAD history, see
the upstream release notes and `.github/CHANGELOG.md`.

## 0.1.0 - Unreleased

- Created the BackboneNeo governance layer for the PMan fork.
- Added a visible downstream notice without renaming upstream packages, CLI,
  or PartCAD formats.
- Pinned downstream `main` to PartCAD `devel` commit
  `137ff5b17d0d5dbd12b4f287b59c34a8a484fedd`.
- Added fail-closed guards that prevent PartCAD packages, tags, container
  images, plugin artifacts, and releases from being published by this fork.
- Pinned sandbox CadQuery to the exact official `v2.8.0` Git commit because the
  tag exists but its distribution is not available from the package index.
- Added the exact CadQuery import dependency closure, including the explicit
  VTK runtime, to clean conda sandboxes and per-package virtual environments;
  CadQuery's source installer omits `install_requires` whenever
  `CONDA_PREFIX` is present.
- Extended the sandbox pin regression test to treat a 40-character Git commit
  reference as an exact dependency pin.
- Preserved OCCT compound topology in the SVG/PNG wrapper and added a safe
  assembly path that projects child edges on one view plane. Mesh-backed
  children without explicit edges are normalized through STL first; this
  avoids native HLR crashes while leaving exported geometry unchanged.
