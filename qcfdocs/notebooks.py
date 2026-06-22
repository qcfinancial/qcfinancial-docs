"""Regenerate ``docs/*.md`` from the chapter notebooks with nbconvert.

Converts the notebooks **as-is** (no ``--execute``): the markdown reflects the
outputs already saved in each ``.ipynb``. Re-run the notebooks in Jupyter when
you want fresh outputs, then run this. The markdown produced here is exactly the
input contract the site converter (:mod:`qcfdocs.convert`) expects.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

from .chapters import CHAPTERS

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"


def _isolated_env() -> dict[str, str]:
    """nbconvert env that ignores the user's global Jupyter config.

    A stray ``~/.jupyter`` config can enable preprocessors from packages we don't
    install (e.g. jupyter_contrib_nbextensions). Point the config search at an
    empty dir so conversion is deterministic and self-contained.
    """
    empty = tempfile.mkdtemp(prefix="qcfdocs-jupyter-")
    env = dict(os.environ)
    env["JUPYTER_CONFIG_DIR"] = empty
    env["JUPYTER_CONFIG_PATH"] = empty
    return env


def regenerate(docs_dir: Path = DOCS_DIR) -> list[Path]:
    """Run nbconvert over every chapter notebook. Returns the written .md paths."""
    docs_dir.mkdir(parents=True, exist_ok=True)
    env = _isolated_env()
    written: list[Path] = []
    for ch in CHAPTERS:
        ipynb = REPO_ROOT / ch.ipynb_name
        if not ipynb.exists():
            raise FileNotFoundError(f"Notebook not found: {ipynb}")
        cmd = [
            sys.executable, "-m", "nbconvert",
            "--to", "markdown",
            # Drop preprocessors injected by the user/system Jupyter config (stale
            # jupyter_contrib_nbextensions entries). nbconvert still runs its
            # built-in default_preprocessors, so output stays standard markdown.
            "--Exporter.preprocessors=[]",
            str(ipynb),
            "--output-dir", str(docs_dir),
            "--output", ch.src_md,
        ]
        print("  $ " + " ".join(cmd[2:]))
        subprocess.run(cmd, check=True, env=env)
        written.append(docs_dir / ch.md_name)
    return written


if __name__ == "__main__":
    paths = regenerate()
    print(f"Regenerated {len(paths)} markdown files into {DOCS_DIR}/")
