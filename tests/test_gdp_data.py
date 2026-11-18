from pathlib import Path
import sys

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.gdp_data import load_gdp_data


def sample_csv(path):
    years = {str(year): [float(year), None] for year in range(1960, 2023)}
    frame = pd.DataFrame({
        "Country Name": ["Alpha", "Beta"],
        "Country Code": ["AAA", "BBB"],
        **years,
    })
    frame.to_csv(path, index=False)


def test_load_gdp_data_preserves_country_names_and_tidy_years(tmp_path):
    source = tmp_path / "gdp.csv"
    sample_csv(source)
    result = load_gdp_data(source)
    assert {"Country Name", "Country Code", "Year", "GDP"} <= set(result.columns)
    assert set(result["Country Name"]) == {"Alpha", "Beta"}
    assert result["Year"].min() == 1960
    assert result["Year"].max() == 2022
    assert len(result) == 2 * 63


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_gdp_data(tmp_path / "missing.csv")


def test_missing_year_column_raises(tmp_path):
    source = tmp_path / "gdp.csv"
    frame = pd.DataFrame({"Country Name": ["Alpha"], "Country Code": ["AAA"]})
    frame.to_csv(source, index=False)
    with pytest.raises(ValueError, match="missing year columns"):
        load_gdp_data(source)


def test_duplicate_country_code_raises(tmp_path):
    source = tmp_path / "gdp.csv"
    years = {str(year): [1.0, 2.0] for year in range(1960, 2023)}
    frame = pd.DataFrame({"Country Name": ["Alpha", "Beta"], "Country Code": ["AAA", "AAA"], **years})
    frame.to_csv(source, index=False)
    with pytest.raises(ValueError, match="duplicate country codes"):
        load_gdp_data(source)


def test_non_numeric_year_value_raises(tmp_path):
    source = tmp_path / "gdp.csv"
    frame = pd.DataFrame({
        "Country Name": ["Alpha"],
        "Country Code": ["AAA"],
        **{str(year): [float(year)] for year in range(1960, 2023)},
    })
    frame.loc[0, "1960"] = "not-a-number"
    frame.to_csv(source, index=False)
    with pytest.raises(ValueError, match="non-numeric values"):
        load_gdp_data(source)


def test_negative_gdp_value_raises(tmp_path):
    source = tmp_path / "gdp.csv"
    frame = pd.DataFrame({
        "Country Name": ["Alpha"],
        "Country Code": ["AAA"],
        **{str(year): [float(year)] for year in range(1960, 2023)},
    })
    frame.loc[0, "1960"] = -1
    frame.to_csv(source, index=False)
    with pytest.raises(ValueError, match="negative GDP"):
        load_gdp_data(source)


def test_infinite_gdp_value_raises(tmp_path):
    source = tmp_path / "gdp.csv"
    frame = pd.DataFrame({
        "Country Name": ["Alpha"],
        "Country Code": ["AAA"],
        **{str(year): [float(year)] for year in range(1960, 2023)},
    })
    frame.loc[0, "1960"] = float("inf")
    frame.to_csv(source, index=False)
    with pytest.raises(ValueError, match="non-finite values"):
        load_gdp_data(source)
