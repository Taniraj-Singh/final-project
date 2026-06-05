#!/usr/bin/env python3
"""Parse pytest -v output into Silver's {name, status} format."""
import sys
import re

def parse(output: str) -> list:
    results = []
    # Match lines like:  tests/test_hysteresis.py::Class::test_name PASSED
    pattern = re.compile(
        r'^(tests/[\w/]+\.py::[\w:]+)\s+(PASSED|FAILED|ERROR|SKIPPED)',
        re.MULTILINE
    )
    for match in pattern.finditer(output):
        name, verdict = match.group(1), match.group(2)
        status = "pass" if verdict == "PASSED" else "fail"
        results.append({"name": name, "status": status})
    return results

if __name__ == "__main__":
    raw = sys.stdin.read()
    import json
    print(json.dumps(parse(raw)))
