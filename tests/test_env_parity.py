"""Verify setup/colab_bootstrap.py's COLAB_EXTRA_PIP is a subset of setup/environment.yml."""
from __future__ import annotations

import re

import yaml

from conftest import REPO_ROOT


def _parse_env_packages() -> set[str]:
    env = yaml.safe_load((REPO_ROOT / "setup" / "environment.yml").read_text())
    names: set[str] = set()
    for dep in env.get("dependencies", []):
        if isinstance(dep, str):
            names.add(re.split(r"[=<>]", dep, maxsplit=1)[0].strip())
        elif isinstance(dep, dict) and "pip" in dep:
            for sub in dep["pip"]:
                names.add(re.split(r"[=<>]", sub, maxsplit=1)[0].strip())
    return names


def _parse_colab_extras() -> list[str]:
    src = (REPO_ROOT / "setup" / "colab_bootstrap.py").read_text()
    match = re.search(r"COLAB_EXTRA_PIP\s*=\s*\[(.*?)\]", src, re.DOTALL)
    assert match, "Could not find COLAB_EXTRA_PIP in setup/colab_bootstrap.py"
    return re.findall(r'"([^"]+)"', match.group(1))


def test_colab_extras_are_in_environment_yml():
    env_packages = _parse_env_packages()
    for pkg in _parse_colab_extras():
        assert pkg in env_packages, (
            f"'{pkg}' is in COLAB_EXTRA_PIP but missing from environment.yml. "
            "Add it to setup/environment.yml or remove it from COLAB_EXTRA_PIP."
        )
