# GDP Dashboard

A Streamlit dashboard for exploring country-level GDP data from the bundled CSV. The dashboard keeps country names and ISO-style country codes, reshapes the wide annual dataset into tidy country-year records, and lets users compare selected countries across available years.

## Data source and scope

- Input file: `data/gdp_data.csv`
- Expected identifier columns: `Country Name` and `Country Code`
- Annual GDP columns are detected from the numeric year headers in the file. The app does not hard-code a maximum year.
- Missing GDP values remain missing. They are not replaced with zero.
- The dashboard displays the dataset values as supplied. Check the source dataset metadata for units and price basis before interpreting GDP amounts.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Dashboard

1. Choose a year range from the years available in the CSV.
2. Select country codes to compare.
3. Review GDP trends and the latest available selected-year values.
4. A missing value for a country/year is displayed as unavailable, not as zero.

## Data validation and tests

The reusable loader in `src/gdp_data.py` checks that the file exists, required country identifiers are present, and at least one year column is available. It preserves country names, converts year labels to integers, parses GDP values numerically, and sorts the tidy result by country and year.

Run tests:

```bash
python -m pytest -q
```

GitHub Actions runs the loader tests, compiles the Streamlit app, and validates the bundled dataset schema and year coverage.

## Limitations

- The CSV is a static snapshot. The dashboard does not fetch live World Bank data.
- GDP units, current/constant price basis, and any transformations depend on the bundled source file.
- The dashboard supports descriptive comparisons. It does not establish causal explanations for GDP changes.
