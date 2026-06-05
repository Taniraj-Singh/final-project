# Reference Plan

## Root Cause

In `HysteresisManager.get_status()`, the `else` branch (scores below `warn_threshold`)
increments `consecutive_count` and transitions `current_status` to `"OK"` when the
count reaches `required_consecutive`, but then **does not reset `consecutive_count` to
0**. On the next call the counter sits at `required_consecutive` (e.g. 3), and since
the branch checks `if self.consecutive_count >= self.required_consecutive` before
incrementing, the condition is never satisfied again on the path that resets state — in
practice the counter keeps climbing but the intended reset never fires cleanly.

More precisely: after the transition fires, `consecutive_count` equals
`required_consecutive`. The very next low-score call falls into `current_status != "OK"`
(now False since we just set it to OK), so it hits the `else: self.consecutive_count = 0`
path — which accidentally zeroes the counter, masking the bug in some call sequences.
The canonical manifestation is when scores oscillate: the counter accumulates toward
`required_consecutive`, fires the transition, but leaves a stale non-zero count that
corrupts the next state cycle.

The fix is one line: add `self.consecutive_count = 0` immediately after
`self.current_status = "OK"` inside the recovery branch.

## Intended Fix

```python
if self.consecutive_count >= self.required_consecutive:
    self.current_status = "OK"
    self.consecutive_count = 0   # <-- add this line
```

## Test Plan

- `test_recovery_from_alarm_to_ok`: drive to ALARM, then feed `required_consecutive`
  low scores; assert final status is `"OK"`.
- `test_consecutive_count_reset_after_ok_transition`: after recovery, assert
  `consecutive_count == 0`.
- `pass_to_pass` tests cover the OK→WARN and WARN→ALARM paths to confirm they are
  unaffected.
