"""Validated loader for the bundled World Bank-style wide GDP CSV."""
from pathlib import Path
import pandas as pd

ID_COLUMNS = ["Country Name", "Country Code"]


def load_gdp_data(path: str | Path) -> pd.DataFrame:
    """Load wide GDP data and return a tidy Country-Year-GDP dataframe."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"GDP dataset not found: {path}")

    raw = pd.read_csv(path)
    missing_ids = set(ID_COLUMNS).difference(raw.columns)
    if missing_ids:
        raise ValueError(f"GDP dataset is missing columns: {sorted(missing_ids)}")

    year_columns = sorted(
        [column for column in raw.columns if str(column).isdigit()],
        key=lambda value: int(value),
    )
    if not year_columns:
        raise ValueError("GDP dataset contains no year columns.")

    if raw.empty:
        raise ValueError("GDP dataset is empty.")
    if raw["Country Code"].isna().all():
        raise ValueError("GDP dataset has no country codes.")

    tidy = raw.melt(
        id_vars=ID_COLUMNS,
        value_vars=year_columns,
        var_name="Year",
        value_name="GDP",
    )
    tidy["Year"] = pd.to_numeric(tidy["Year"], errors="raise").astype(int)
    tidy["GDP"] = pd.to_numeric(tidy["GDP"], errors="coerce")
    tidy["Country Name"] = tidy["Country Name"].astype("string").str.strip()
    tidy["Country Code"] = tidy["Country Code"].astype("string").str.strip()
    tidy = tidy.sort_values(["Country Code", "Year"], kind="stable").reset_index(drop=True)
    return tidy
