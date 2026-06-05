#!/usr/bin/env bash
set -euo pipefail

LOGS_DIR="/logs/verifier"
mkdir -p "$LOGS_DIR"

# Apply test_patch if non-empty (adds test files at base_commit)
PATCH=$(python3 -c "
import json, sys
cfg = json.load(open('/app/tests/config.json'))
print(cfg.get('test_patch', ''))
")
if [ -n "$PATCH" ]; then
    echo "$PATCH" | git apply --whitespace=fix
fi

# Run the test suite
bash /app/tests/run_script.sh 2>&1 | tee /tmp/runner_output.txt

# Parse output
RESULTS=$(python3 /app/tests/parser.py < /tmp/runner_output.txt)
echo "Parsed results: $RESULTS"

# Check every required test
REWARD=1
CONFIG=$(cat /app/tests/config.json)

check_tests() {
    local key="$1"
    local required_status="$2"
    python3 - <<PYEOF
import json, sys
cfg = json.loads('''$CONFIG''')
results = json.loads('''$RESULTS''')
result_map = {r['name']: r['status'] for r in results}
tests = cfg.get('$key', [])
for t in tests:
    got = result_map.get(t, 'missing')
    if got != '$required_status':
        print(f"FAIL: {t}  expected=$required_status  got={got}", file=sys.stderr)
        sys.exit(1)
print("OK: all $key tests have status=$required_status")
PYEOF
}

if ! check_tests "fail_to_pass" "pass"; then
    REWARD=0
fi

if ! check_tests "pass_to_pass" "pass"; then
    REWARD=0
fi

echo "$REWARD" > "$LOGS_DIR/reward.txt"
echo "Reward: $REWARD"
