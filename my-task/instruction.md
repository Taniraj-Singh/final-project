# Alarm state stays stuck even after sensor readings recover

## A bit of background

This codebase monitors industrial sensors on a factory floor. Every reading coming
off a sensor gets scored from 0 to 1 — low scores mean everything is running
normally, high scores mean something is off. The system uses a class called
`HysteresisManager` in `hysteresis.py` to decide what the current alarm status is.

The reason it exists is to stop the alarm from flickering. Noisy sensors can bounce
around unpredictably, so rather than reacting to every single reading, the system
requires a run of consistent readings before it commits to changing state. You need
several high readings in a row before it trips to `WARN`, then several more before
it goes to `ALARM`. The same logic applies going the other direction — you should
need a run of consistently low, normal readings before the alarm clears back to `OK`.

## What's actually going wrong

The problem is that once a sensor has escalated all the way to `ALARM`, it never
comes back down to `OK` on its own — even if the sensor behaves perfectly normally
for a long time afterward.

You can reproduce it like this: create a fresh `HysteresisManager`, feed it enough
high-scoring readings to push it into `ALARM`, then start feeding it readings with
scores around 0.1 — clearly in the normal range, nothing borderline. Keep going for
as long as you want. The status never changes. It stays stuck at `ALARM` forever.

That's the first part of the bug.

The second part is connected: once a recovery does eventually happen (say, via the
`reset()` method), the internal counter that tracks consecutive readings should be
sitting at zero. If it's not, the very next anomaly cycle will behave strangely —
either triggering too early or requiring extra readings to escalate. So the recovery
path needs to leave the counter clean.

## What should happen instead

When a sensor that's been in `ALARM` starts producing consistently low anomaly
readings, the `HysteresisManager` should eventually return `"OK"` from `get_status()`.
The number of consecutive low readings required to trigger that transition is the
same count the class already uses for every other state change — nothing new needs
to be added or configured.

Once `get_status()` starts returning `"OK"`, the debounce counter inside the manager
should be at zero. The next time anomaly scores start climbing again, the escalation
sequence should run from scratch, unaffected by whatever happened during the previous
recovery.

## Where to look

Everything relevant is inside `hysteresis.py`. The `get_status()` method has three
separate branches depending on where the incoming score falls. The branch that handles
scores clearly in the normal range — below both thresholds — is where the recovery
logic lives. Something in that branch goes wrong specifically when the transition to
`"OK"` fires.

The `reset()` method is fine as-is. The threshold values are correct and should stay
the same. The fix is contained to a single spot in the recovery branch.
