"""
Unit tests for ModelManager in model_manager.py.
Tests model training, saving, loading, and prediction behaviour.
"""
import os
import shutil
import pytest
import numpy as np
from model_manager import ModelManager


@pytest.fixture
def tmp_model_dir(tmp_path):
    """Provide a clean temporary directory for model artefacts."""
    yield str(tmp_path / "models")
    # tmp_path is automatically removed by pytest


class TestModelManagerTrainAndLoad:
    """Tests for training, saving, and reloading models."""

    def test_train_succeeds(self, tmp_model_dir):
        """train_models() should return True and set models_loaded."""
        mm = ModelManager(model_dir=tmp_model_dir)
        result = mm.train_models()
        assert result is True
        assert mm.models_loaded is True

    def test_model_files_created(self, tmp_model_dir):
        """Training must create isolation_forest.pkl, pca_model.pkl, and scaler.pkl."""
        mm = ModelManager(model_dir=tmp_model_dir)
        mm.train_models()
        expected_files = ["isolation_forest.pkl", "pca_model.pkl", "scaler.pkl"]
        for fname in expected_files:
            assert os.path.exists(os.path.join(tmp_model_dir, fname)), \
                f"Expected model file {fname} not found"

    def test_metadata_json_created(self, tmp_model_dir):
        """Training must create a metadata.json file."""
        mm = ModelManager(model_dir=tmp_model_dir)
        mm.train_models()
        metadata_path = os.path.join(tmp_model_dir, "metadata.json")
        assert os.path.exists(metadata_path)

    def test_load_after_train(self, tmp_model_dir):
        """A freshly trained model set should load successfully."""
        mm = ModelManager(model_dir=tmp_model_dir)
        mm.train_models()

        mm2 = ModelManager(model_dir=tmp_model_dir)
        result = mm2.load_models()
        assert result is True
        assert mm2.models_loaded is True

    def test_load_triggers_training_when_no_files(self, tmp_model_dir):
        """load_models() on an empty directory should auto-train and succeed."""
        mm = ModelManager(model_dir=tmp_model_dir)
        result = mm.load_models()
        assert result is True
        assert mm.models_loaded is True


class TestModelManagerPredict:
    """Tests for the predict_anomaly() method."""

    @pytest.fixture(autouse=True)
    def trained_manager(self, tmp_model_dir):
        """Train a fresh model for every test in this class."""
        self.mm = ModelManager(model_dir=tmp_model_dir)
        self.mm.train_models()

    def _normal_features(self) -> np.ndarray:
        """Return a 24-feature vector representative of normal operation."""
        return np.array([
            100.0, 2.0, 95.0, 105.0, 100.0,  # pressure stats
            200.0, 3.0, 193.0, 207.0, 200.0,  # temperature stats
            12.0, 0.5, 11.0, 13.0, 12.0,       # current stats
            0.7, 0.6, 0.1,                      # correlations
            0.0, 0.0, 0.0,                      # z-scores
            0.3, 0.4, 0.2,                      # IQRs
        ])

    def test_predict_returns_dict(self):
        """predict_anomaly() should return a dictionary."""
        result = self.mm.predict_anomaly(self._normal_features())
        assert isinstance(result, dict)

    def test_predict_has_required_keys(self):
        """Result must contain anomaly_score, status, and confidence."""
        result = self.mm.predict_anomaly(self._normal_features())
        for key in ("anomaly_score", "status", "confidence"):
            assert key in result, f"Missing key: {key}"

    def test_anomaly_score_in_unit_interval(self):
        """anomaly_score must be in [0, 1]."""
        result = self.mm.predict_anomaly(self._normal_features())
        assert 0.0 <= result["anomaly_score"] <= 1.0

    def test_status_is_valid_string(self):
        """status must be one of OK, WARN, or ALARM."""
        result = self.mm.predict_anomaly(self._normal_features())
        assert result["status"] in ("OK", "WARN", "ALARM")

    def test_predict_without_loaded_models_returns_safe_defaults(self, tmp_model_dir):
        """Calling predict when no models are loaded must return OK with score 0."""
        mm = ModelManager(model_dir=tmp_model_dir + "_empty")
        # Don't load or train — force unloaded state
        mm.models_loaded = False
        result = mm.predict_anomaly(self._normal_features())
        assert result["status"] == "OK"
        assert result["anomaly_score"] == 0.0

    def test_1d_and_2d_feature_arrays_accepted(self):
        """predict_anomaly should handle both 1-D and 2-D input arrays."""
        features_1d = self._normal_features()
        features_2d = features_1d.reshape(1, -1)
        result_1d = self.mm.predict_anomaly(features_1d)
        result_2d = self.mm.predict_anomaly(features_2d)
        # Both should succeed and return the same score
        assert abs(result_1d["anomaly_score"] - result_2d["anomaly_score"]) < 1e-9
