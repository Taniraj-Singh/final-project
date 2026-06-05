# Reference Plan

## What's actually broken and why

The bug is a single missing line in `HysteresisManager.get_status()`.

Look at the branch that runs when `anomaly_score` falls below `warn_threshold` — the
"clearly normal" range. When the current status is anything other than `OK`, this
branch counts consecutive normal readings and transitions to `"OK"` once the count
hits `required_consecutive`. That part works. The problem is that after the transition
fires, `consecutive_count` is left sitting at `required_consecutive` (which is 3)
instead of being reset to 0.

On the very next call, the status is now `OK`, so the code takes the `else` path and
zeroes the counter there. That might look like it fixes itself, but it doesn't — the
counter is 3 when the transition fires, which means the condition
`self.consecutive_count >= self.required_consecutive` is already true at the start
of the next iteration. In sequences where scores oscillate near the threshold, this
stale counter corrupts the count for the next cycle and the status can get stuck
because the recovery condition fires but doesn't fully commit.

In the simplest reproduction path: feed alarm-level scores until status reaches
`ALARM`, then feed low scores. The counter increments from 0 toward 3, hits 3, sets
`current_status = "OK"` but leaves `consecutive_count = 3`. The next call sees
`current_status == "OK"` and resets it to 0, which hides the bug in simple tests.
But in an oscillating signal, the transition never cleanly fires and the system stays
stuck in `ALARM`.

## The fix

One line added immediately after `self.current_status = "OK"` inside the recovery
branch:

```python
self.consecutive_count = 0
```

That's it. The counter resets when the status transitions, just like it does in every
other branch of the method. The ALARM→WARN and WARN→ALARM paths both reset the
counter correctly — the OK recovery path just forgot to.

## Why the tests catch this

`test_recovery_from_alarm_to_ok` drives the state machine to ALARM and then feeds it
a sustained run of low-scoring readings. It asserts the final status is `"OK"`. At
`base_commit` this fails because the status never clears.

`test_reset_clears_consecutive_counter` checks that after calling `reset()`, the
counter is 0. This one is indirect — but it also verifies that the counter contract
holds across the API boundary, so a related regression won't sneak through.

The `pass_to_pass` tests cover OK→WARN and WARN→ALARM transitions to confirm the
fix doesn't disturb the escalation direction.

## Difficulty assessment

An agent reading the code sees three branches with similar-looking counter logic.
All three reset the counter after a transition in the escalation direction; only one
fails to do so in the recovery direction. The symptom (stuck in ALARM) points at the
recovery logic, but the root cause requires understanding that the counter state
persists across calls and that the `else` path on the following call masks the
problem in simple step-through analysis. This should land in the 1–4/10 range.
