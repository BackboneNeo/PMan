# Contributing to PMan

PMan is an upstream-compatible BackboneNeo fork of PartCAD. The Python package
names, the `partcad` and `pc` commands, and PartCAD file formats remain
unchanged.

Use the upstream contribution guide for product development and the rules below
for downstream changes:

1. Link every change to a GitHub Issue.
2. Branch from downstream `main`; never commit downstream changes to `devel`.
3. Submit a pull request to `main` and record risk, version impact, checks, and
   rollback steps in the pull-request template.
4. Run validation and commits inside the repository devcontainer as required by
   `AGENTS.md`.
5. Keep IVINS-P models, metadata, and other private artifacts out of this public
   repository.
6. Synchronize upstream only through the procedure in
   `docs/downstream/UPSTREAM.md` and rerun the complete validation suite.

Releases and package publication are disabled in this fork. Enabling them is a
separate High-risk change and requires explicit owner approval.
