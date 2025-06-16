# Tipsy Coder Website

This repository contains the source for the Tipsy Coder static website.

## Running Tests

A simple test script is provided under the `tests/` directory. The script
parses `index.html` for basic HTML issues and checks that any image URLs are
reachable.

To run the test, execute:

```bash
python tests/test_index.py
```

The script will exit with a non-zero status if it detects a problem.
