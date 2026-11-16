# Garden app

Vusi Sithole · VS26060020556

A console application based on the supplied gardening-advice starter. It asks
for a season and plant type, then combines their advice. Supported seasons are
summer and winter; supported plant types are flower and vegetable. These are
the choices covered by the original starter, not an automatic local calendar.

## Run

Use Python 3.12 or newer. No third-party packages are required.

```bash
python garden_advice.py
python -m unittest -v
```

Choices ignore capitalisation and outer whitespace. Invalid choices display
the supported values and prompt again. Ctrl+C or closed input cancels cleanly.
`get_advice(season, plant_type)` is available for reuse without prompting on
import. Its docstring explains its arguments, result and validation errors.

## Git workflow

The original starter was uploaded before cloning this repository. Issue #1
tracks reusable functions, dictionaries, documentation and validation tests.
Issue #2 tracks interactive input, retries and cancellation. Each change has
its own branch and pull request, tested and reviewed before merging into main.
The closed issues, merged PRs and commits provide the workflow evidence.
