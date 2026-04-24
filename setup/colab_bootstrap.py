"""Colab bootstrap for ARCTIC SciSynth 2026 RWD notebooks.

Every notebook's first executable cell calls ``bootstrap()``:

    import urllib.request, sys
    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/arctic-gsu/arctic-scisynth-2026-rwd-public/main/setup/colab_bootstrap.py",
        "/tmp/colab_bootstrap.py",
    )
    sys.path.insert(0, "/tmp")
    from colab_bootstrap import bootstrap
    bootstrap()

In Google Colab: clones the repo to ``/content/arctic-scisynth-2026-rwd-public``
(skip if already cloned), ``os.chdir``s into it, and ``pip install``s the
runtime dependencies that Colab doesn't ship with (skip if already
importable). Running it from every cell is cheap — the clone check, pip
check, and version print are all gated so repeat calls are no-ops.

Locally (no ``google.colab`` module), ``bootstrap()`` is a no-op and
assumes the ``arctic-scisynth-2026-rwd`` conda env is already active.
"""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

REPO_URL = "https://github.com/arctic-gsu/arctic-scisynth-2026-rwd-public.git"
REPO_DIR = "/content/arctic-scisynth-2026-rwd-public"

# Deps Colab's default stack lacks. Keep in sync with setup/environment.yml.
COLAB_EXTRA_PIP = [
    "folium",
    "geopy",
    "nbformat",
]

_SENTINEL = Path("/content/.arctic_bootstrap_done")


def _in_colab() -> bool:
    try:
        import google.colab  # type: ignore[import-not-found]  # noqa: F401
    except Exception:
        return False
    return True


def _clone_if_needed() -> None:
    if Path(REPO_DIR, ".git").is_dir():
        return
    print(f"Cloning {REPO_URL} to {REPO_DIR} ...")
    subprocess.run(
        ["git", "clone", "--depth", "1", REPO_URL, REPO_DIR],
        check=True,
    )


def _all_extras_installed() -> bool:
    return all(importlib.util.find_spec(p) is not None for p in COLAB_EXTRA_PIP)


def _pip_install_extras_if_needed() -> None:
    if _all_extras_installed():
        return
    print(f"Installing Colab-only deps: {', '.join(COLAB_EXTRA_PIP)} ...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--quiet", *COLAB_EXTRA_PIP],
        check=True,
    )


def _print_versions() -> None:
    import importlib

    print(f"Python {sys.version.split()[0]}")
    for pkg in ("pandas", "numpy", "matplotlib", "folium", "geopy"):
        try:
            mod = importlib.import_module(pkg)
            print(f"  {pkg:12s} {getattr(mod, '__version__', '?')}")
        except ImportError:
            print(f"  {pkg:12s} (not installed)")


def bootstrap() -> None:
    """Bootstrap the notebook environment. Idempotent."""
    if not _in_colab():
        return

    if _SENTINEL.exists():
        os.chdir(REPO_DIR)
        return

    _clone_if_needed()
    os.chdir(REPO_DIR)
    _pip_install_extras_if_needed()
    _print_versions()
    _SENTINEL.touch()
    print(f"\n✅ Colab bootstrap complete. Working directory: {os.getcwd()}")


if __name__ == "__main__":
    bootstrap()
