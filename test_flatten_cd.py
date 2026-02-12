from flatten_cd import extract_data

import os

import pytest

@pytest.fixture(scope="session")
def temp_path(tmp_path_factory):
    return tmp_path_factory.mktemp("temp_path")

@pytest.fixture(scope="session")
def extracted_data(temp_path):
    extract_data(temp_path, "HILIC_POS_5ppm.cdResult", "HILIC_test")

def test_extract_data(temp_path, extracted_data):
    assert len(os.listdir(temp_path)) == 2
    assert os.path.isfile(temp_path / "HILIC_test_flattened.xlsx")
    assert os.path.isfile(temp_path / "HILIC_test_flattened_comp.xlsx")
