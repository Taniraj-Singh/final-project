# Bug: Sensor alarm state never clears after recovery

## Background

The `HysteresisManager` class in `hysteresis.py` implements a debounced state machine
for sensor alarm status. It transitions between three states — `OK`, `WARN`, and `ALARM`
— and requires several consecutive readings above or below a threshold before changing
state. This prevents flickering on noisy sensor data.

## The Problem

Once a sensor reaches `ALARM` state and then receives sustained low-anomaly readings
(scores well below the warn threshold), the state machine should eventually return to
`OK`. Currently it does not: the `consecutive_count` counter keeps accumulating but the
status never transitions back to `OK`, leaving the alarm permanently latched.

## Expected Behaviour

Given a `HysteresisManager` instance:

1. Drive it to `ALARM` state by passing anomaly scores at or above `alarm_threshold`
   for `required_consecutive` calls.
2. Then call `get_status()` with a score of `0.1` (well below `warn_threshold`)
   repeatedly — at least `required_consecutive` times.
3. After enough low-score readings the returned status must be `"OK"`.

The `consecutive_count` attribute should be `0` once the transition to `OK` completes,
so that the next anomaly cycle starts with a clean counter.

## Constraints

- Only `hysteresis.py` needs to change.
- Do not alter the threshold values or `required_consecutive`.
- The fix must not affect the OK→WARN or WARN→ALARM transition paths.
