# World GDP Dashboard

An interactive Streamlit dashboard for exploring World Bank-style GDP observations by country and year.

## Features

- Select a year range from 1960 to 2022.
- Select countries by ISO-style country code.
- Compare country GDP trends over time.
- View selected-country GDP values and growth ratios for the chosen period.
- Display country names in the chart legend while retaining codes for filtering.

## Dataset

The bundled file is `data/gdp_data.csv`. It contains country names, country codes and annual GDP fields from 1960 through 2022. The loader reshapes the wide table into tidy records with `Country Name`, `Country Code`, `Year` and `GDP`.

The loader validates required identity fields, unique country codes, complete year-column coverage, and numeric GDP observations. Blank GDP cells are retained as missing observations. Non-numeric text, infinite values and negative GDP values are rejected.

## Run locally

```bash
python -m pip install -r requirements.txt pytest
pytest -q
streamlit run streamlit_app.py
```

Open the local Streamlit URL printed in the terminal.

## Project structure

- `streamlit_app.py`: interactive dashboard.
- `data/gdp_data.csv`: bundled GDP dataset.
- `src/gdp_data.py`: reusable data loading, reshaping and validation.
- `tests/test_gdp_data.py`: automated data-loader tests.
- `.github/workflows/gdp-dashboard-checks.yml`: CI validation, data checks and Streamlit smoke test.

## Interpretation notes and limitations

- GDP values are shown in the units provided by the bundled source. Confirm the source metadata before comparing or quoting monetary values.
- The dashboard uses annual observations and preserves missing values. Missing years are not interpolated.
- Growth ratios are calculated only when both selected endpoint observations are available and the starting value is non-zero.
- GDP growth ratios are descriptive comparisons. They do not explain the causes of economic change.
- Verify the bundled dataset's exact World Bank indicator, download date and licence before using the results in formal research.

## Technology

Python, pandas, Streamlit and pytest.
