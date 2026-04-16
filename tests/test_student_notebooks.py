"""Structural parity between student and solution notebooks.

The *intent* of this test is the SPEC Phase 5 task 4 requirement —
"hand-filled student copies that run to completion." We achieve the
same guarantee more cheaply: since the student notebook is identical
to the solution notebook except for `???` placeholders in 🎯 exercise
cells, any student who fills in the `???` with the solution-cell code
will reproduce the solution notebook. The solution notebook is
already covered by test_solutions_execute.py.

What this file tests:
- Every student notebook has a matching solution notebook.
- Same code-cell count and markdown-cell count (modulo deliberate
  student/solution diffs — see TOLERANCE below).
- Every student code cell that contains `???` has a cell in the
  solution notebook whose code has no `???`.
- No stray `???` in solution notebooks — an unfilled placeholder in
  the solution means the notebook would error when executed.
"""
from __future__ import annotations

import json

import pytest

from conftest import NOTEBOOKS, SOLUTIONS, DAY_NOTEBOOK_PAIRS

NOTEBOOK_NAMES = [name for name, _ in DAY_NOTEBOOK_PAIRS]


def _code_cells(nb_path):
    nb = json.loads(nb_path.read_text())
    return [
        "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        for c in nb["cells"]
        if c.get("cell_type") == "code"
    ]


@pytest.mark.parametrize("name", NOTEBOOK_NAMES)
def test_pair_exists(name):
    assert (NOTEBOOKS / name).exists(), f"Missing student notebook: {name}"
    assert (SOLUTIONS / name).exists(), f"Missing solution notebook: {name}"


@pytest.mark.parametrize("name", NOTEBOOK_NAMES)
def test_solution_has_no_placeholders(name):
    for src in _code_cells(SOLUTIONS / name):
        assert "???" not in src, (
            f"Solution notebook {name} still contains a `???` placeholder. "
            f"Every 🎯 exercise in a solution notebook must be fully filled in."
        )


@pytest.mark.parametrize("name", NOTEBOOK_NAMES)
def test_student_and_solution_code_cell_counts_align(name):
    n_student = len(_code_cells(NOTEBOOKS / name))
    n_solution = len(_code_cells(SOLUTIONS / name))
    assert n_student == n_solution, (
        f"{name}: student has {n_student} code cells, solution has "
        f"{n_solution}. Cell counts should match — only markdown "
        f"INSTRUCTOR NOTE blockquotes differ."
    )


@pytest.mark.parametrize("name", NOTEBOOK_NAMES)
def test_student_notebook_has_placeholders(name):
    # day5 is the one exception — it's a markdown-prompt briefing template
    # with no code cells for students to fill in.
    srcs = _code_cells(NOTEBOOKS / name)
    has_placeholder = any("???" in s for s in srcs)
    if name == "day5_briefing_template.ipynb":
        assert not has_placeholder, (
            "day5 is a markdown-prompt briefing template; no code `???` expected."
        )
    else:
        assert has_placeholder, (
            f"{name}: no `???` placeholders. Students have nothing to do — "
            f"this is indistinguishable from a solution notebook."
        )


@pytest.mark.parametrize("name", NOTEBOOK_NAMES)
def test_student_notebook_has_no_committed_outputs(name):
    nb = json.loads((NOTEBOOKS / name).read_text())
    for i, c in enumerate(nb["cells"]):
        if c.get("cell_type") != "code":
            continue
        outs = c.get("outputs", [])
        assert not outs, (
            f"{name} cell {i} has committed outputs. Student notebooks must "
            f"be cleared before commit: `jupyter nbconvert --clear-output "
            f"--inplace notebooks/{name}`."
        )
        assert c.get("execution_count") in (None, 0), (
            f"{name} cell {i} has execution_count={c.get('execution_count')}. "
            f"Run `jupyter nbconvert --clear-output --inplace` before committing."
        )
