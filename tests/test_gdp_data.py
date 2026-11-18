import pandas as pd
import pytest
from src.gdp_data import load_gdp_data


def test_load_gdp_data_preserves_country_name_and_tidy_years(tmp_path):
    source = pd.DataFrame({
        "Country Name": ["India", "Japan"],
        "Country Code": ["IND", "JPN"],
        "1960": [37.0, 44.0],
        "1961": [39.0, None],
    })
    path = tmp_path / "gdp.csv"
    source.to_csv(path, index=False)

    result = load_gdp_data(path)

    assert list(result.columns) == ["Country Name", "Country Code", "Year", "GDP"]
    assert len(result) == 4
    india = result[result["Country Code"] == "IND"]
    assert india["Country Name"].eq("India").all()
    assert india["Year"].tolist() == [1960, 1961]
    assert india["GDP"].tolist() == [37.0, 39.0]
    japan = result[result["Country Code"] == "JPN"].sort_values("Year")
    assert japan["Year"].tolist() == [1960, 1961]
    assert pd.isna(japan.iloc[1]["GDP"])


def test_load_gdp_data_rejects_missing_identifiers(tmp_path):
    path = tmp_path / "bad.csv"
    pd.DataFrame({"1960": [1]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="Country Code"):
        load_gdp_data(path)


def test_load_gdp_data_rejects_missing_year_columns(tmp_path):
    path = tmp_path / "bad.csv"
    pd.DataFrame({"Country Name": ["India"], "Country Code": ["IND"]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="no year columns"):
        load_gdp_data(path)


def test_load_gdp_data_rejects_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_gdp_data(tmp_path / "missing.csv")
