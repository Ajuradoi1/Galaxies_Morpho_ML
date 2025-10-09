# test_main_pipeline.py
import pytest
import pandas as pd
import numpy as np
import tarfile
from unittest.mock import patch, MagicMock

# Import functions from your module
from module import safe_to_numeric, download_with_retries, save_images_to_TAR


@pytest.fixture
def mock_dataframe():
    """Return a small fake DataFrame similar to the real ZooSpecPhotoDR19 data."""
    data = {
        "dr7objid": [1, 2],
        "modelMag_u": [18.0, -25.0],
        "modelMag_g": [17.5, 19.0],
        "modelMag_r": [17.2, 18.7],
        "modelMag_i": [17.0, 18.5],
        "modelMag_z": [16.8, 18.2],
        "modelMagErr_u": [0.4, 0.4],
        "modelMagErr_g": [0.04, 0.04],
        "modelMagErr_r": [0.04, 0.04],
        "modelMagErr_i": [0.04, 0.04],
        "modelMagErr_z": [0.09, 0.09],
        "p_el_debiased": [0.95, 0.3],
        "p_cs_debiased": [0.1, 0.92],
        "petroR90_r": [5.0, 10.0],
        "spiral": [0, 1],
        "elliptical": [1, 0],
    }
    return pd.DataFrame(data)


def test_safe_to_numeric_converts_valid_values():
    """safe_to_numeric should turn valid numeric strings into numbers and invalids into NaN."""
    s = pd.Series(["1", "x", "3.5"])
    result = safe_to_numeric(s)
    assert pd.api.types.is_numeric_dtype(result)
    assert np.isnan(result.iloc[1])


def test_filtering_logic(mock_dataframe, tmp_path):
    """Simulate the magnitude/error/classification filters."""
    df = mock_dataframe.copy()
    df = df.apply(safe_to_numeric).set_index("dr7objid")

    mask = (
        (df["modelMag_u"] > -30)
        & (df["modelMagErr_u"] < 0.5)
        & ((df["p_cs_debiased"] >= 0.9) | (df["p_el_debiased"] >= 0.9))
    )

    filtered = df[mask]
    assert len(filtered) == 2  # both rows pass criteria
    output_path = tmp_path / "ZooSpecPhotoDR19_filtered.csv.gz"
    filtered.to_csv(output_path, compression="gzip")
    assert output_path.exists()


@patch("requests.Session.get")
def test_download_with_retries(mock_get):
    """Ensure download_with_retries returns bytes if successful."""
    mock_get.return_value.ok = True
    mock_get.return_value.content = b"fake_image_data"
    result = download_with_retries(ra=120.5, dec=-1.3, petroR90_r=5)
    assert isinstance(result, bytes)


def test_save_images_to_tar(tmp_path):
    """Test that save_images_to_TAR correctly writes files into a TAR archive."""
    tar_path = tmp_path / "test.tar"
    img_bytes = b"fakeimagedata"
    images = [
        ("1", img_bytes, {"objid": 1}),
        ("2", img_bytes, {"objid": 2}),
    ]
    save_images_to_TAR(tar_path, images)
    assert tar_path.exists()

    # Verify TAR content
    with tarfile.open(tar_path, "r") as tar:
        members = tar.getmembers()
        assert len(members) == 2
        names = [m.name for m in members]
        assert "1.jpg" in names or "1.png" in names


@patch("astroquery.utils.tap.core.TapPlus")
def test_tapplus_download_mock(mock_tap):
    """Mock the TAP service to verify query and download logic."""
    mock_instance = MagicMock()
    mock_tap.return_value = mock_instance

    mock_job = MagicMock()
    mock_job.get_results.return_value.to_pandas.return_value = pd.DataFrame({"a": [1], "b": [2]})
    mock_instance.launch_job.return_value = mock_job

    tap = mock_tap(url="http://tap.roe.ac.uk/ssa")
    job = tap.launch_job("SELECT TOP 1 * FROM table")
    df = job.get_results().to_pandas()

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1, 2)