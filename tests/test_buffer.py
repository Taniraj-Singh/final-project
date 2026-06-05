"""
Unit tests for RingBuffer in buffer.py.
Tests core ring buffer behaviour: capacity, eviction, readiness, and clear.
"""
import pytest
from buffer import RingBuffer


class TestRingBufferCapacity:
    """Tests for the ring buffer's fixed-size window behaviour."""

    def test_buffer_respects_window_size(self):
        """Buffer should never grow beyond window_size elements."""
        buf = RingBuffer(window_size=5)
        for i in range(10):
            buf.add_data({"value": i})
        assert buf.current_size() == 5

    def test_oldest_element_is_evicted(self):
        """When the buffer is full, the oldest element is evicted first."""
        buf = RingBuffer(window_size=3)
        buf.add_data({"value": 1})
        buf.add_data({"value": 2})
        buf.add_data({"value": 3})
        buf.add_data({"value": 4})   # evicts {"value": 1}
        window = buf.get_window()
        values = [d["value"] for d in window]
        assert values == [2, 3, 4]

    def test_partial_fill_preserves_order(self):
        """Elements are returned in insertion order before the buffer is full."""
        buf = RingBuffer(window_size=5)
        for v in [10, 20, 30]:
            buf.add_data({"value": v})
        window = buf.get_window()
        assert [d["value"] for d in window] == [10, 20, 30]


class TestRingBufferReadiness:
    """Tests for the is_ready() method."""

    def test_not_ready_when_empty(self):
        """A freshly created buffer should not be ready."""
        buf = RingBuffer(window_size=5)
        assert buf.is_ready() is False

    def test_not_ready_below_window_size(self):
        """Buffer is not ready until it has exactly window_size entries."""
        buf = RingBuffer(window_size=5)
        for i in range(4):
            buf.add_data({"value": i})
        assert buf.is_ready() is False

    def test_ready_at_window_size(self):
        """Buffer becomes ready exactly when window_size entries are present."""
        buf = RingBuffer(window_size=5)
        for i in range(5):
            buf.add_data({"value": i})
        assert buf.is_ready() is True

    def test_ready_stays_true_after_overflow(self):
        """is_ready() stays True after elements are evicted."""
        buf = RingBuffer(window_size=5)
        for i in range(10):
            buf.add_data({"value": i})
        assert buf.is_ready() is True


class TestRingBufferClear:
    """Tests for the clear() method."""

    def test_clear_resets_size(self):
        """After clear(), current_size() should return 0."""
        buf = RingBuffer(window_size=5)
        for i in range(5):
            buf.add_data({"value": i})
        buf.clear()
        assert buf.current_size() == 0

    def test_clear_resets_readiness(self):
        """After clear(), is_ready() should return False."""
        buf = RingBuffer(window_size=5)
        for i in range(5):
            buf.add_data({"value": i})
        buf.clear()
        assert buf.is_ready() is False

    def test_clear_empties_window(self):
        """After clear(), get_window() should return an empty list."""
        buf = RingBuffer(window_size=5)
        for i in range(5):
            buf.add_data({"value": i})
        buf.clear()
        assert buf.get_window() == []

    def test_add_after_clear_works(self):
        """Buffer should accept new data normally after being cleared."""
        buf = RingBuffer(window_size=3)
        for i in range(3):
            buf.add_data({"value": i})
        buf.clear()
        buf.add_data({"value": 99})
        assert buf.current_size() == 1
        assert buf.get_window() == [{"value": 99}]


class TestRingBufferGetWindow:
    """Tests for the get_window() method."""

    def test_get_window_returns_copy(self):
        """Mutating the returned list must not affect the internal buffer."""
        buf = RingBuffer(window_size=3)
        buf.add_data({"value": 1})
        window = buf.get_window()
        window.append({"value": 999})
        assert buf.current_size() == 1

    def test_get_window_empty_when_no_data(self):
        """get_window() on a new buffer returns an empty list."""
        buf = RingBuffer(window_size=5)
        assert buf.get_window() == []
