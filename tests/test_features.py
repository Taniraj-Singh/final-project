"""
Unit tests for FeatureExtractor in features.py.
Tests statistical feature extraction from sensor window data.
"""
import pytest
import numpy as np
from features import FeatureExtractor


def _make_window(n: int, pressure=120.0, temperature=220.0,
                 flow_rate=50.0, motor_current=12.0, vibration=2.5) -> list:
    """Create a list of n identical sensor readings."""
    return [
        {
            "pressure": pressure,
            "temperature": temperature,
            "flow_rate": flow_rate,
            "motor_current": motor_current,
            "vibration": vibration,
        }
        for _ in range(n)
    ]


class TestFeatureExtractorOutput:
    """Tests that feature extraction returns correct shape and values."""

    def test_returns_numpy_array(self):
        """extract_features should return a numpy array."""
        fe = FeatureExtractor()
        window = _make_window(20)
        result = fe.extract_features(window)
        assert isinstance(result, np.ndarray)

    def test_empty_window_returns_empty_array(self):
        """An empty window should return an empty array (not raise)."""
        fe = FeatureExtractor()
        result = fe.extract_features([])
        assert len(result) == 0

    def test_feature_count_with_all_sensors(self):
        """With 5 standard sensors present, expect 5 * 8 = 40 features."""
        fe = FeatureExtractor()
        window = _make_window(20)
        result = fe.extract_features(window)
        # 5 sensors × (mean, std, min, max, median, q1, q3, trend) = 40
        assert len(result) == 40

    def test_feature_names_length_matches_feature_vector(self):
        """get_feature_names() must return exactly as many names as features extracted."""
        fe = FeatureExtractor()
        window = _make_window(20)
        features = fe.extract_features(window)
        names = fe.get_feature_names()
        assert len(names) == len(features)


class TestFeatureExtractorValues:
    """Tests that extracted feature values are numerically correct."""

    def test_mean_of_constant_signal(self):
        """Mean feature of a constant signal must equal that constant."""
        fe = FeatureExtractor()
        window = _make_window(20, pressure=100.0)
        features = fe.extract_features(window)
        names = fe.get_feature_names()
        mean_idx = names.index("pressure_mean")
        assert abs(features[mean_idx] - 100.0) < 1e-9

    def test_std_of_constant_signal_is_zero(self):
        """Standard deviation of a constant signal should be 0."""
        fe = FeatureExtractor()
        window = _make_window(20, pressure=100.0)
        features = fe.extract_features(window)
        names = fe.get_feature_names()
        std_idx = names.index("pressure_std")
        assert abs(features[std_idx]) < 1e-9

    def test_min_max_of_constant_signal(self):
        """Min and max of a constant signal are both equal to that constant."""
        fe = FeatureExtractor()
        window = _make_window(20, temperature=200.0)
        features = fe.extract_features(window)
        names = fe.get_feature_names()
        min_idx = names.index("temperature_min")
        max_idx = names.index("temperature_max")
        assert abs(features[min_idx] - 200.0) < 1e-9
        assert abs(features[max_idx] - 200.0) < 1e-9

    def test_trend_of_constant_signal_is_zero(self):
        """Trend (last - first) of a constant signal is 0."""
        fe = FeatureExtractor()
        window = _make_window(20, pressure=100.0)
        features = fe.extract_features(window)
        names = fe.get_feature_names()
        trend_idx = names.index("pressure_trend")
        assert abs(features[trend_idx]) < 1e-9

    def test_trend_of_increasing_signal(self):
        """Trend feature should be positive for a strictly increasing signal."""
        fe = FeatureExtractor()
        window = [
            {"pressure": float(i), "temperature": 220.0,
             "flow_rate": 50.0, "motor_current": 12.0, "vibration": 2.5}
            for i in range(20)
        ]
        features = fe.extract_features(window)
        names = fe.get_feature_names()
        trend_idx = names.index("pressure_trend")
        assert features[trend_idx] > 0

    def test_no_nan_in_features(self):
        """Feature vector must not contain NaN values."""
        fe = FeatureExtractor()
        window = _make_window(20)
        features = fe.extract_features(window)
        assert not np.any(np.isnan(features))


class TestFeatureExtractorPartialSensors:
    """Tests extraction when only a subset of sensors are present."""

    def test_partial_sensors_no_exception(self):
        """Extraction should not raise when some sensor columns are missing."""
        fe = FeatureExtractor()
        window = [{"pressure": 100.0, "temperature": 200.0} for _ in range(10)]
        result = fe.extract_features(window)
        assert isinstance(result, np.ndarray)

    def test_feature_names_only_include_present_sensors(self):
        """Feature names should only contain names for sensors actually in the data."""
        fe = FeatureExtractor()
        window = [{"pressure": 100.0} for _ in range(10)]
        fe.extract_features(window)
        names = fe.get_feature_names()
        # vibration, temperature, etc. should not appear
        for name in names:
            assert name.startswith("pressure_")
