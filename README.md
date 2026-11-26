# World GDP Dashboard

An interactive Streamlit dashboard for exploring annual GDP observations from the World Bank's World Development Indicators (WDI).

## Features

- Select a year range from 1960 to 2022.
- Select countries by ISO-style country code.
- Compare country GDP trends over time.
- View selected-country GDP values and nominal endpoint percentage changes for the selected period.
- Display country names in the chart legend while retaining codes for filtering.

## Dataset and provenance

The bundled file is `data/gdp_data.csv`. Its rows identify the World Bank indicator:

| Field | Value |
|---|---|
| Provider | The World Bank |
| Source | World Development Indicators |
| Source ID | 2 |
| Indicator name | GDP (current US$) |
| Indicator code | `NY.GDP.MKTP.CD` |
| Unit | Current US dollars (US$) |
| Price basis | Current prices, not adjusted for inflation |
| Years in bundled file | 1960–2022 |
| Country/aggregate rows | 266 |

The World Bank indicator metadata defines the measure as gross domestic product and states that it is expressed in current prices and US dollars. Since the values are not inflation-adjusted, comparing nominal values across years does not measure real GDP growth.

Official links:

- Indicator page: https://data.worldbank.org/indicator/NY.GDP.MKTP.CD
- Indicator metadata API: https://api.worldbank.org/v2/indicator/NY.GDP.MKTP.CD?format=json
- Data API for the bundled year range: https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?date=1960:2022&format=json
- World Bank data terms: https://data.worldbank.org/summary-terms-of-use

The World Bank's default data terms are CC BY 4.0 unless indicator or dataset metadata identifies a different restriction. Attribute the World Bank and its data providers when reusing values. The repository's Apache-2.0 code licence does not replace the dataset's source terms.

### Snapshot limitation

The original download date and exact vintage of the bundled CSV are not recorded. The final year, 2022, is the coverage end date, not evidence of the date when the file was downloaded. This is explicitly recorded as unknown in `data/metadata.json`. The CSV is not silently refreshed or overwritten by this documentation change.

## Validation and transformation

The loader reshapes the wide table into tidy records with `Country Name`, `Country Code`, `Year` and `GDP`.

It validates required identity fields, unique country codes, complete year-column coverage, and numeric GDP observations. Blank GDP cells remain missing values. Non-numeric text, infinite values and negative GDP values are rejected.

## Run locally

```bash
python -m pip install -r requirements.txt pytest
pytest -q
streamlit run streamlit_app.py
```

Open the local Streamlit URL printed in the terminal.

## Project structure

- `streamlit_app.py`: interactive dashboard.
- `data/gdp_data.csv`: bundled GDP snapshot.
- `data/metadata.json`: indicator, coverage, terms and known snapshot limitations.
- `src/gdp_data.py`: reusable data loading, reshaping and validation.
- `tests/test_gdp_data.py`: automated data-loader tests.
- `.github/workflows/gdp-dashboard-checks.yml`: CI validation, data checks and Streamlit smoke test.

## Interpretation notes and limitations

- Values are nominal GDP in current US dollars, not constant-price/real GDP.
- The dataset includes countries and regional aggregates. Do not treat all 266 rows as independent sovereign countries.
- Annual observations preserve missing values; missing years are not interpolated.
- Nominal endpoint percentage change is calculated only when both endpoint observations are available and the starting value is positive. It is not a compound annual growth rate or real GDP growth.
- GDP growth ratios are descriptive comparisons. They do not explain the causes of economic change.
- Use the same data vintage for fair comparisons. The exact retrieval date of this local snapshot remains undocumented.

## Technology

Python, pandas, Streamlit and pytest.

## Latest GitHub Actions validation

Latest successful main-branch workflow run verified on 26 November 2026: [GitHub Actions run #45798717179](https://github.com/krishankantpandey359-droid/gdp-dashboard/actions/runs/45798717179). This confirms the configured automated checks, not every manual or deployment feature.
