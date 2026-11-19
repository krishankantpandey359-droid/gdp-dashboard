import streamlit as st
import pandas as pd
import math
from pathlib import Path
from src.gdp_data import load_gdp_data, nominal_change_percent

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='GDP dashboard',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_gdp_data():
    """Load and reshape GDP data while retaining country names and codes."""
    data_path = Path(__file__).parent / "data" / "gdp_data.csv"
    try:
        return load_gdp_data(data_path)
    except (FileNotFoundError, ValueError) as exc:
        st.error(str(exc))
        st.stop()

gdp_df = get_gdp_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_americas: GDP dashboard

Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. As you'll
notice, the data only goes to 2022 right now, and datapoints for certain years are often missing.
But it's otherwise a great (and did I mention _free_?) source of data.
'''

# Add some spacing
''
''

min_value = gdp_df['Year'].min()
max_value = gdp_df['Year'].max()

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

countries = gdp_df['Country Code'].unique()

if not len(countries):
    st.warning("Select at least one country")

selected_countries = st.multiselect(
    'Which countries would you like to view?',
    countries,
    ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN'])

''
''
''

# Filter the data
filtered_gdp_df = gdp_df[
    (gdp_df['Country Code'].isin(selected_countries))
    & (gdp_df['Year'] <= to_year)
    & (from_year <= gdp_df['Year'])
]

st.caption('GDP is measured in current US dollars. The endpoint change is nominal and is not adjusted for inflation.')\n\nst.header('GDP over time', divider='gray')

''

st.line_chart(
    filtered_gdp_df,
    x='Year',
    y='GDP',
    color='Country Name',
)

''
''


first_year = gdp_df[gdp_df['Year'] == from_year]
last_year = gdp_df[gdp_df['Year'] == to_year]

st.header(f'GDP in {to_year}', divider='gray')

''

cols = st.columns(4)

for i, country in enumerate(selected_countries):
    col = cols[i % len(cols)]

    with col:
        country_data = gdp_df[gdp_df['Country Code'] == country]

        first_values = country_data.loc[
            country_data['Year'] == from_year, 'GDP'
        ].dropna()
        last_values = country_data.loc[
            country_data['Year'] == to_year, 'GDP'
        ].dropna()

        if last_values.empty:
            value = 'N/A'
            growth = 'n/a'
            delta_color = 'off'
        else:
            last_gdp = last_values.iloc[0] / 1_000_000_000
            value = f'{last_gdp:,.0f}B'

            if first_values.empty:
                growth = 'n/a'
                delta_color = 'off'
            else:
                change_pct = nominal_change_percent(
                    first_values.iloc[0], last_values.iloc[0]
                )
                if change_pct is None:
                    growth = 'n/a'
                    delta_color = 'off'
                else:
                    growth = f'{change_pct:+.1f}% nominal change'
                    delta_color = 'normal'

        st.metric(
            label=f'{country} GDP',
            value=value,
            delta=growth,
            delta_color=delta_color
        )
