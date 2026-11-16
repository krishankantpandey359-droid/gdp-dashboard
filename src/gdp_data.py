from pathlib import Path
import pandas as pd

MIN_YEAR = 1960
MAX_YEAR = 2022
IDENTITY_COLUMNS = ["Country Name", "Country Code"]

def load_gdp_data(path):
    """Read wide World Bank-style data and return tidy GDP records."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"GDP dataset not found: {path}")
    raw = pd.read_csv(path)
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
    result["GDP"] = pd.to_numeric(result["GDP"], errors="coerce")
    return result
