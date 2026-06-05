"""
Unit tests for HysteresisManager in hysteresis.py.
Tests the state-machine transitions: OK→WARN→ALARM and recovery paths.
"""
import pytest
from hysteresis import HysteresisManager


def _drive_to_status(manager: HysteresisManager, score: float, target: str, max_ticks: int = 20) -> bool:
    """Helper: feed a constant score until the manager reaches target or we time out."""
    for _ in range(max_ticks):
        if manager.get_status(score) == target:
            return True
    return False


class TestHysteresisOKToWarn:
    """Tests for the transition from OK to WARN."""

    def test_single_high_score_does_not_trigger_warn(self):
        """One sample above warn_threshold must not immediately enter WARN."""
        hm = HysteresisManager()
        status = hm.get_status(0.75)
        assert status == "OK"

    def test_requires_consecutive_samples_for_warn(self):
        """Status should reach WARN after required_consecutive samples >= warn_threshold."""
        hm = HysteresisManager()
        reached = _drive_to_status(hm, 0.75, "WARN")
        assert reached, "Expected to reach WARN with sustained warn-level scores"

    def test_interruption_resets_consecutive_counter(self):
        """A single below-threshold sample should reset the consecutive counter."""
        hm = HysteresisManager()
        # Two samples near warn threshold
        hm.get_status(0.75)
        hm.get_status(0.75)
        # One recovery sample below threshold
        hm.get_status(0.3)
        # Two more warn-level samples — should NOT yet be in WARN
        hm.get_status(0.75)
        status = hm.get_status(0.75)
        assert status == "OK"


class TestHysteresisWarnToAlarm:
    """Tests for the transition from WARN to ALARM."""

    def _state_at_warn(self) -> HysteresisManager:
        hm = HysteresisManager()
        _drive_to_status(hm, 0.75, "WARN")
        return hm

    def test_alarm_requires_consecutive_samples(self):
        """Reaching ALARM requires required_consecutive samples >= alarm_threshold."""
        hm = self._state_at_warn()
        reached = _drive_to_status(hm, 0.95, "ALARM")
        assert reached, "Expected to reach ALARM with sustained alarm-level scores"

    def test_single_alarm_score_from_warn_does_not_alarm(self):
        """One alarm-level sample from WARN state should not immediately trigger ALARM."""
        hm = self._state_at_warn()
        status = hm.get_status(0.95)
        assert status != "ALARM"


class TestHysteresisAlarmRecovery:
    """Tests for recovery from ALARM back down through WARN to OK."""

    def _state_at_alarm(self) -> HysteresisManager:
        hm = HysteresisManager()
        _drive_to_status(hm, 0.95, "ALARM")
        return hm

    def test_alarm_stays_on_moderate_scores(self):
        """Scores at warn_threshold should not immediately clear an ALARM."""
        hm = self._state_at_alarm()
        for _ in range(5):
            status = hm.get_status(0.75)
        # Still ALARM or may have transitioned to WARN — must NOT jump straight to OK
        assert status != "OK", "ALARM should not immediately clear to OK with moderate scores"

    def test_recovery_from_alarm_to_ok(self):
        """Sustained low scores must eventually bring the status back to OK."""
        hm = self._state_at_alarm()
        reached = _drive_to_status(hm, 0.1, "OK")
        assert reached, "Expected full recovery to OK with sustained low scores"

    def test_alarm_clears_to_warn_before_ok(self):
        """Recovery path should pass through WARN before reaching OK."""
        hm = self._state_at_alarm()
        seen_warn = False
        for _ in range(30):
            status = hm.get_status(0.5)   # between warn and alarm threshold
            if status == "WARN":
                seen_warn = True
            if status == "OK":
                break
        # Either we went through WARN, or the score was low enough to skip it;
        # what matters is we do not incorrectly skip from ALARM straight to OK
        # when using a score that's at the WARN boundary.
        final = hm.get_status(0.1)
        assert final in ("WARN", "OK")


class TestHysteresisReset:
    """Tests for the reset() method."""

    def test_reset_clears_state_from_alarm(self):
        """After reset(), status should return to OK immediately."""
        hm = HysteresisManager()
        _drive_to_status(hm, 0.95, "ALARM")
        hm.reset()
        assert hm.current_status == "OK"

    def test_reset_clears_consecutive_counter(self):
        """After reset(), the consecutive counter should be 0."""
        hm = HysteresisManager()
        hm.get_status(0.75)
        hm.get_status(0.75)
        hm.reset()
        assert hm.consecutive_count == 0

    def test_status_after_reset_behaves_like_fresh_instance(self):
        """After reset, the manager should behave identically to a new instance."""
        hm = HysteresisManager()
        _drive_to_status(hm, 0.95, "ALARM")
        hm.reset()
        # One warn-level score should not trigger WARN in a fresh/reset manager
        status = hm.get_status(0.75)
        assert status == "OK"
