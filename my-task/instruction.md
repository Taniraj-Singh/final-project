# Alarm state does not clear after sensor readings return to normal

## Context

This system monitors industrial sensors in real time. Each sensor reading produces an
anomaly score between 0 and 1. A score near 0 means the sensor is behaving normally;
a score near 1 means something is wrong.

To avoid false alarms on noisy data, the system uses a debounce mechanism — it only
changes the alarm status after several consecutive readings in agreement. This is
handled by `HysteresisManager` in `hysteresis.py`. The manager maintains three
states for each sensor:

- **OK** — normal operation
- **WARN** — elevated readings detected, watching closely
- **ALARM** — confirmed anomaly, action required

The idea is that you can't trigger an alarm on a single spike, and you can't clear an
alarm on a single good reading either. A sustained run of readings is required to move
the status in either direction.

## What's broken

When a sensor has been in `ALARM` and then starts producing consistently low anomaly
scores — the kind that should indicate a return to normal — the `HysteresisManager`
never transitions back to `OK`. The alarm stays latched indefinitely, even after many
readings that are clearly in the normal range.

To reproduce: create a `HysteresisManager`, push it into `ALARM` state by feeding it
several high-anomaly readings, then feed it a long run of clearly normal readings
(anomaly score around `0.1`). The status should eventually become `"OK"` but it
doesn't — it stays stuck.

Once the status does correctly recover to `"OK"`, the internal debounce counter should
also be back at zero, so the next anomaly cycle starts cleanly. Currently that is not
happening either.

## Expected behaviour

After a sensor has been in `ALARM` and anomaly scores drop back to a clearly normal
level and stay there for the required number of consecutive readings, `get_status()`
must return `"OK"`.

The number of consecutive readings required to exit `ALARM` back to `OK` is the same
`required_consecutive` value already used for all other transitions in the class — no
new configuration is needed.

Once the `"OK"` transition completes, the internal counter tracking consecutive
readings must be reset to zero. A subsequent high-anomaly run should trigger the
full escalation sequence from the beginning, not be affected by leftover state from
the previous recovery.

## Where to look

The bug is in `hysteresis.py`. The `get_status()` method handles each of the three
score ranges as separate branches. The branch that handles scores in the clearly-normal
range is where the recovery logic lives — and where something goes wrong when the
transition to `"OK"` finally fires.

The `reset()` method and the threshold values are correct and should not be changed.
