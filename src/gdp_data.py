from pathlib import Path

import numpy as np
import pandas as pd

MIN_YEAR = 1960
MAX_YEAR = 2022
IDENTITY_COLUMNS = ["Country Name", "Country Code"]


def _read_source_csv(path):
    """Read CSV and safely discard only completely empty export columns."""
    raw = pd.read_csv(path)
    raw.columns = [str(column).strip() for column in raw.columns]

    blank_names = [column for column in raw.columns if not column]
    unnamed_columns = [
        column for column in raw.columns
        if column.lower().startswith("unnamed:")
    ]
    removable = blank_names + unnamed_columns
    for column in removable:
        if raw[column].notna().any():
            raise ValueError(
                f"GDP dataset contains a populated blank/unnamed column: {column!r}."
            )
    if removable:
        raw = raw.drop(columns=removable)

    if len(set(raw.columns)) != len(raw.columns):
        raise ValueError("GDP dataset contains duplicate column names.")
    return raw


def load_gdp_data(path):
    """Read wide World Bank-style data and return tidy GDP records."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"GDP dataset not found: {path}")
    raw = _read_source_csv(path)
    missing = set(IDENTITY_COLUMNS).difference(raw.columns)
    if missing:
        raise ValueError(f"GDP dataset is missing columns: {sorted(missing)}")
    if raw.empty:
        raise ValueError("GDP dataset contains no country records.")
    for column in IDENTITY_COLUMNS:
        if raw[column].isna().any() or raw[column].astype(str).str.strip().eq("").any():
            raise ValueError(f"GDP dataset contains blank {column.lower()} values.")
    if raw["Country Code"].duplicated().any():
        raise ValueError("GDP dataset contains duplicate country codes.")
    years = [str(year) for year in range(MIN_YEAR, MAX_YEAR + 1)]
    missing_years = set(years).difference(raw.columns)
    if missing_years:
        raise ValueError(f"GDP dataset is missing year columns: {sorted(missing_years)}")
    result = raw.melt(id_vars=IDENTITY_COLUMNS, value_vars=years, var_name="Year", value_name="GDP")
    result["Year"] = pd.to_numeric(result["Year"], errors="raise").astype(int)
    raw_gdp = result["GDP"]
    numeric_gdp = pd.to_numeric(raw_gdp, errors="coerce")
    invalid_text = raw_gdp.notna() & raw_gdp.astype(str).str.strip().ne("") & numeric_gdp.isna()
    if invalid_text.any():
        raise ValueError("GDP dataset contains non-numeric values in year columns.")
    present = numeric_gdp.dropna()
    if not np.isfinite(present.to_numpy(dtype=float)).all():
        raise ValueError("GDP dataset contains non-finite values.")
    if (present < 0).any():
        raise ValueError("GDP dataset contains negative GDP values.")
    result["GDP"] = numeric_gdp
    return result
