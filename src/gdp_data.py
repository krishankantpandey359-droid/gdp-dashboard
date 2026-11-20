from pathlib import Path

import csv
import numpy as np
import pandas as pd

MIN_YEAR = 1960
MAX_YEAR = 2022
IDENTITY_COLUMNS = ["Country Name", "Country Code"]
INDICATOR_NAME_COLUMN = "Indicator Name"
INDICATOR_CODE_COLUMN = "Indicator Code"
EXPECTED_INDICATOR_NAME = "GDP (current US$)"
EXPECTED_INDICATOR_CODE = "NY.GDP.MKTP.CD"


def _read_gdp_source(path):
    """Read the source CSV, allowing only completely empty export columns."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle), [])

    if not header:
        raise ValueError("GDP dataset has an empty CSV header.")

    normalized_header = [str(name).strip() for name in header]
    nonblank_header = [name for name in normalized_header if name]
    if len(nonblank_header) != len(set(nonblank_header)):
        raise ValueError("GDP dataset contains duplicate column names.")

    blank_positions = [i for i, name in enumerate(normalized_header) if not name]
    raw = pd.read_csv(path)

    if raw.shape[1] != len(header):
        raise ValueError("GDP dataset header and data columns do not match.")

    for position in blank_positions:
        if raw.iloc[:, position].notna().any():
            raise ValueError("GDP dataset contains a populated blank column.")

    if blank_positions:
        keep_positions = [i for i in range(raw.shape[1]) if i not in blank_positions]
        raw = raw.iloc[:, keep_positions]

    raw.columns = normalized_header[:len(normalized_header)]
    if blank_positions:
        raw.columns = [name for i, name in enumerate(normalized_header) if i not in blank_positions]

    if len(set(raw.columns)) != len(raw.columns):
        raise ValueError("GDP dataset contains duplicate column names.")
    return raw


def load_gdp_data(path):
    """Read the bundled World Bank GDP indicator and return tidy records."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"GDP dataset not found: {path}")
    raw = _read_gdp_source(path)

    required = set(IDENTITY_COLUMNS + [INDICATOR_NAME_COLUMN, INDICATOR_CODE_COLUMN])
    missing = required.difference(raw.columns)
    if missing:
        raise ValueError(f"GDP dataset is missing metadata columns: {sorted(missing)}")
    if raw.empty:
        raise ValueError("GDP dataset contains no country records.")

    for column in IDENTITY_COLUMNS + [INDICATOR_NAME_COLUMN, INDICATOR_CODE_COLUMN]:
        if raw[column].isna().any() or raw[column].astype(str).str.strip().eq("").any():
            raise ValueError(f"GDP dataset contains blank {column.lower()} values.")
        raw[column] = raw[column].astype(str).str.strip()

    if raw[INDICATOR_NAME_COLUMN].nunique() != 1 or not raw[INDICATOR_NAME_COLUMN].eq(
        EXPECTED_INDICATOR_NAME
    ).all():
        raise ValueError(f"Expected indicator name: {EXPECTED_INDICATOR_NAME}")
    if raw[INDICATOR_CODE_COLUMN].nunique() != 1 or not raw[INDICATOR_CODE_COLUMN].eq(
        EXPECTED_INDICATOR_CODE
    ).all():
        raise ValueError(f"Expected indicator code: {EXPECTED_INDICATOR_CODE}")
    if raw["Country Code"].duplicated().any():
        raise ValueError("GDP dataset contains duplicate country codes after trimming whitespace.")

    years = [str(year) for year in range(MIN_YEAR, MAX_YEAR + 1)]
    missing_years = set(years).difference(raw.columns)
    if missing_years:
        raise ValueError(f"GDP dataset is missing year columns: {sorted(missing_years)}")

    result = raw.melt(
        id_vars=IDENTITY_COLUMNS, value_vars=years,
        var_name="Year", value_name="GDP",
    )
    result["Year"] = pd.to_numeric(result["Year"], errors="raise").astype(int)
    raw_gdp = result["GDP"]
    numeric_gdp = pd.to_numeric(raw_gdp, errors="coerce")
    invalid_text = (
        raw_gdp.notna()
        & raw_gdp.astype(str).str.strip().ne("")
        & numeric_gdp.isna()
    )
    if invalid_text.any():
        raise ValueError("GDP dataset contains non-numeric values in year columns.")
    present = numeric_gdp.dropna()
    if not np.isfinite(present.to_numpy(dtype=float)).all():
        raise ValueError("GDP dataset contains non-finite values.")
    if (present < 0).any():
        raise ValueError("GDP dataset contains negative GDP values.")
    result["GDP"] = numeric_gdp
    return result


def nominal_change_percent(start_value, end_value):
    """Return nominal endpoint change as a percent, or None if undefined.

    This is a change in current-US-dollar GDP between two selected years.
    It is not inflation-adjusted real GDP growth.
    """
    if start_value is None or end_value is None:
        return None
    try:
        start = float(start_value)
        end = float(end_value)
    except (TypeError, ValueError, OverflowError):
        return None
    if not np.isfinite([start, end]).all() or start <= 0:
        return None
    change = (end / start - 1.0) * 100.0
    return change if np.isfinite(change) else None
