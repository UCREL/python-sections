# ucrel_sections

Lightweight, colourised console sections, timers and inline unit tests.

## Install

```bash
pip install ucrel_sections
# or straight from GitHub
pip install git+https://github.com/UCREL/python-sections.git
```

Requires Python 3.10+.

## Usage

```python
from ucrel_sections import Section

with Section("Loading data") as s:
    with s.timer("read csv"):
        rows = load_rows()

    s.tryAssert(len(rows) > 0, "no rows loaded", name="non-empty")

    with s.test("schema", canFail=True) as t:
        t.reject("id" not in rows[0], "missing id column")
```

## Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Releasing

The version comes from git tags (via `hatch-vcs`). To publish to PyPI:

1. Tag and push: `git tag v0.1.0 && git push origin v0.1.0`
2. Create a GitHub Release from that tag. The `Publish` workflow builds and uploads to PyPI.
