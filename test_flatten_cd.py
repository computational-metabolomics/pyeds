from flatten_cd import extract_data

import os

import pandas as pd
import pytest

@pytest.fixture(scope="session")
def temp_path(tmp_path_factory):
    return tmp_path_factory.mktemp("temp_path")

@pytest.fixture(scope="session")
def extracted_data(temp_path):
    extract_data(temp_path, "HILIC_POS_5ppm.cdResult", "HILIC_test")

def test_output_generated(temp_path, extracted_data):
    assert len(os.listdir(temp_path)) == 2
    assert os.path.isfile(temp_path / "HILIC_test_flattened.xlsx")
    assert os.path.isfile(temp_path / "HILIC_test_flattened_comp.xlsx")

def test_content_equal(temp_path, extracted_data):
    expected = pd.read_excel("HILIC_POS_5ppm_flattened.xlsx")
    actual = pd.read_excel(temp_path / "HILIC_test_flattened.xlsx")
    pd.testing.assert_frame_equal(expected, actual)

def test_comp_content_equal(temp_path, extracted_data):
    expected = pd.read_excel("HILIC_POS_5ppm_comp_flattened.xlsx")
    actual = pd.read_excel(temp_path / "HILIC_test_flattened_comp.xlsx")
    pd.testing.assert_frame_equal(expected, actual)
