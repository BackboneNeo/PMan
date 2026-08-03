# Upstream relationship and synchronization

## Pin

- Upstream: `https://github.com/partcad/partcad.git`
- Upstream branch: `devel`
- Pinned commit: `137ff5b17d0d5dbd12b4f287b59c34a8a484fedd`
- Downstream default branch: `main`
- Mirror branch: `devel`

The `devel` branch is an unmodified mirror of `upstream/devel`. PMan changes
must never be committed to it. The Git remote named `upstream` is fetch-only in
the managed local clone, while `origin` is the push default.

## Synchronization procedure

1. Open a Change Issue and review upstream changes, licenses, release workflows,
   dependency changes, and security implications.
2. Fetch `upstream` and verify the intended commit is on `upstream/devel`.
3. Fast-forward the fork's `devel` to that exact commit without modifying it.
4. Create a dedicated `sync/<commit>` branch from downstream `main` and merge
   the pinned upstream commit into that branch.
5. Reapply or update downstream governance and release guards if upstream
   workflows changed.
6. Run the complete upstream devcontainer suite: unit tests, Behave,
   pre-commit, and relevant AI-agent skill tests.
7. Open a pull request from the sync branch to `main`; never push the merge
   directly to `main`.
8. After review and successful required checks, update the pin in this document
   in the same pull request.

Do not publish tags or releases as part of an upstream synchronization.

## Temporary downstream compatibility override

The pinned upstream commit sets sandbox CadQuery to `2.8.0`, which is not
available from the configured package index. PMan installs the exact official
`v2.8.0` tag commit `fb4c6d41863aee270c46ab64397f0d2675e74be0`
from `CadQuery/cadquery` while preserving the upstream Python 3.11 and OCP 7.9
contract. Every upstream sync must check whether the distribution is published
and replace the direct reference with the normal version pin once the complete
suite passes without it.

CadQuery's source `setup.py` deliberately suppresses `install_requires` in a
conda environment. Because PartCAD uses conda as the sandbox interpreter but
installs the pinned source with pip, PMan explicitly installs the exact
`runtype`, `multimethod`, `casadi`, VTK, and `ezdxf` versions needed by
`import cadquery`. VTK and `ezdxf` are explicit because per-package virtual
environments can otherwise observe satisfied base guards without inheriting
`vtkmodules` or the DXF importer dependency. Keep those pins and the Git commit
as one compatibility unit; validate them in a newly created sandbox rather
than relying on an accumulated developer cache.

## Downstream assembly-render compatibility

The pinned renderer could pass a heterogeneous assembly compound to OCCT
hidden-line removal as a `Solid`, which can terminate the render subprocess.
PMan preserves the original OCCT topology and projects each assembly leaf's
topological edges on one common view plane. A triangulation-only leaf is first
normalized through STL so that it has projectable edges. This compatibility
path intentionally does not infer hidden lines between separate components;
individual part rendering retains normal face-aware hidden-line removal, and
all export paths continue to use the unmodified source geometry.

Every upstream sync must run the compound topology regression and render a
multi-component assembly before updating this override.
