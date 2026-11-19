# World GDP Dashboard

An interactive Streamlit dashboard for exploring annual GDP observations by country and year.

## Features

- Select a year range from 1960 to 2022.
- Select countries by ISO-style country code.
- Compare country GDP trends over time.
- View selected-country GDP values and endpoint growth ratios for the chosen period.
- Display country names in the chart legend while retaining codes for filtering.

## Dataset and indicator

The bundled file is `data/gdp_data.csv`. Its metadata identifies the World Bank World Development Indicators series:

- Indicator name: GDP (current US$)
- Indicator code: `NY.GDP.MKTP.CD`
- Coverage in this file: 1960–2022

GDP is expressed in current US dollars, not constant dollars or purchasing-power-parity units. Current-dollar GDP is affected by price-level and exchange-rate changes, so it should not be interpreted as real GDP growth. The exact source download date and licence are not recorded in the repository and remain to be documented.

The loader validates country identity fields, unique country codes, exact indicator metadata, complete year-column coverage, and numeric GDP observations. Blank GDP cells remain missing. Non-numeric text, infinite values and negative GDP values are rejected.

## Run locally

```bash
python -m pip install -r requirements.txt pytest
pytest -q
streamlit run streamlit_app.py
```

## Project structure

- `streamlit_app.py`: interactive dashboard.
- `data/gdp_data.csv`: bundled source data.
- `src/gdp_data.py`: reusable data loading, reshaping and validation.
- `tests/test_gdp_data.py`: automated loader tests.
- `.github/workflows/gdp-dashboard-checks.yml`: CI validation, data checks and Streamlit smoke test.

## Interpretation and limitations

- The dashboard shows current-US-dollar GDP. It does not calculate inflation-adjusted or PPP GDP.
- The dashboard uses annual observations and preserves missing values. Missing years are not interpolated.
- Endpoint growth ratios are calculated only when both selected endpoint observations are available and the starting value is non-zero.
- Endpoint ratios do not represent a compound annual growth rate and do not explain the causes of economic change.
- The source download date and dataset licence must be confirmed before formal redistribution or research use.
- Aggregates and country records are both present in the source. Treat regional/income aggregates as aggregates, not as individual countries.

## Technology

Python, pandas, Streamlit and pytest.
