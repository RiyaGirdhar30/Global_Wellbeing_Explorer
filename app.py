import pandas as pd
import streamlit as st
from pathlib import Path

# Configure the application
st.set_page_config(
    page_title="Global Wellbeing Explorer",
    page_icon="🌍",
    layout="wide"
)

# Load the dataset
DATA_PATH = Path(__file__).parent / "data" / "WHR26_Data_Figure_2.1.xlsx"


@st.cache_data
def load_data():
    data = pd.read_excel(DATA_PATH)
    return data


try:
    df = load_data()
except FileNotFoundError:
    st.error("Dataset not found. Please check the data folder.")
    st.stop()
except Exception as error:
    st.error(f"Unable to load the dataset: {error}")
    st.stop()

# Application heading
st.title("🌍 Global Wellbeing Explorer")

st.markdown(
    "Explore life evaluation scores, compare countries, "
    "and discover wellbeing trends across the world."
)

st.divider()

# Display summary metrics
latest_year = int(df["Year"].max())
latest_data = df[df["Year"] == latest_year]

st.divider()

overview_tab, country_tab, insights_tab, rankings_tab = st.tabs([
    "🌍 Overview",
    "🗺️ Country Explorer",
    "📊 Data Insights",
    "🏆 Rankings & Data Quality"
])

with overview_tab:
    st.subheader("🌎 Global Wellbeing at a Glance")

    overview_data = latest_data.dropna(
        subset=["Life evaluation (3-year average)"]
    )

    highest_country_row = overview_data.loc[
        overview_data["Life evaluation (3-year average)"].idxmax()
    ]

    lowest_country_row = overview_data.loc[
        overview_data["Life evaluation (3-year average)"].idxmin()
    ]

    average_score = overview_data[
        "Life evaluation (3-year average)"
    ].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average life evaluation",
        f"{average_score:.2f}"
    )

    col2.metric(
        "Highest-scoring country",
        highest_country_row["Country name"],
        f"Score: {highest_country_row['Life evaluation (3-year average)']:.3f}"
    )

    col3.metric(
        "Lowest-scoring country",
        lowest_country_row["Country name"],
        f"Score: {lowest_country_row['Life evaluation (3-year average)']:.3f}"
    )

    st.markdown("### Latest Year Highlights")

    overview_chart = overview_data.nlargest(
        15, "Life evaluation (3-year average)"
    ).sort_values("Life evaluation (3-year average)")

    st.markdown("#### Top 15 Countries by Life Evaluation")

    st.bar_chart(
        overview_chart.set_index("Country name")[
            "Life evaluation (3-year average)"
        ],
        x_label="Country",
        y_label="Life evaluation score",
        height=450,
        width="stretch"
    )

    st.caption(
        f"Summary based on available country scores for {latest_year}. "
        "Life evaluation scores are reported as three-year averages."
    )

        
    st.divider()

    st.markdown("### ℹ️ About the Data")

    st.write(
        "This dashboard uses data from the World Happiness Report 2026, "
        "specifically its Figure 2.1 dataset covering reporting years "
        "2011–2025."
    )

    st.write(
        "Life evaluation scores represent people's assessments of their "
        "lives. The report also provides explanatory components associated "
        "with these scores."
    )

    st.caption(
        "Correlations show statistical associations, not proof of causation. "
        "The available years and country coverage vary across the dataset."
    )

    st.markdown(
        "[View the official World Happiness Report data-sharing page]"
        "(https://www.worldhappiness.report/data-sharing/)"
    )



with country_tab:

    st.subheader("🌎 Compare Countries")

    # Get the available countries in the latest year
    available_countries = sorted(
        latest_data["Country name"].unique()
    )

    default_countries = [
        country
        for country in ["Finland", "India", "United States"]
        if country in available_countries
    ]

    selected_countries = st.multiselect(
        "Choose countries to compare",
        options=available_countries,
        default=default_countries,
        max_selections=10
    )

    if selected_countries:
        comparison = latest_data[
            latest_data["Country name"].isin(selected_countries)
        ][
            ["Rank", "Country name", "Life evaluation (3-year average)"]
        ].sort_values("Rank")

        st.dataframe(
            comparison,
            width="stretch",
            hide_index=True
        )

        st.subheader("📊 Score Comparison")

        chart_data = comparison.set_index("Country name")[
            "Life evaluation (3-year average)"
        ]

        st.bar_chart(chart_data)

    else:
        st.info("Select at least one country to see the comparison.")


    st.subheader("📈 Historical Wellbeing Explorer")

    historical_country = st.selectbox(
        "Choose a country to explore over time",
        options=available_countries,
        index=available_countries.index("India")
        if "India" in available_countries else 0
    )

    country_history = df[
        df["Country name"] == historical_country
    ].sort_values("Year").copy()

    # Show the historical trend
    st.markdown(f"### Life evaluation trend: {historical_country}")

    st.line_chart(
        country_history.set_index("Year")[
            "Life evaluation (3-year average)"
        ],
        x_label="Year",
        y_label="Life evaluation score"
    )

    # Compare earliest and latest available observations
    if not country_history.empty:
        first_record = country_history.iloc[0]
        last_record = country_history.iloc[-1]

        first_score = first_record["Life evaluation (3-year average)"]
        last_score = last_record["Life evaluation (3-year average)"]

        score_change = last_score - first_score

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Earliest available year",
            int(first_record["Year"])
        )

        col2.metric(
            "Latest available year",
            int(last_record["Year"])
        )

        col3.metric(
            "Score change",
            f"{score_change:+.3f}"
        )

        st.caption(
            "Change is calculated between the earliest and latest available "
            "observations, not necessarily consecutive years. Scores are "
            "three-year averages."
        )

        st.dataframe(
            country_history[
                ["Year", "Rank", "Life evaluation (3-year average)"]
            ],
            width="stretch",
            hide_index=True
        )


with insights_tab:
    st.subheader("🔎 Wellbeing Factor Explorer")

    st.write(
        "Explore how the report's explanatory components relate "
        "to life evaluation in the latest reporting year."
    )

    factor_options = {
        "GDP per capita": "Explained by: Log GDP per capita",
        "Social support": "Explained by: Social support",
        "Healthy life expectancy": "Explained by: Healthy life expectancy",
        "Freedom to make life choices": "Explained by: Freedom to make life choices",
        "Generosity": "Explained by: Generosity",
        "Perceptions of corruption": "Explained by: Perceptions of corruption",
    }

    selected_factor_name = st.selectbox(
        "Choose an explanatory factor",
        options=list(factor_options.keys())
    )

    selected_factor = factor_options[selected_factor_name]
    score_column = "Life evaluation (3-year average)"

    # Use the latest year's records
    factor_data = latest_data[
        ["Country name", score_column, selected_factor]
    ].dropna().copy()

    st.caption(
        f"Using {len(factor_data)} countries with complete values "
        f"for {selected_factor_name} and life evaluation in {latest_year}."
    )

    if len(factor_data) >= 2:
        correlation = factor_data[selected_factor].corr(
            factor_data[score_column]
        )

        metric_col1, metric_col2 = st.columns(2)

        metric_col1.metric(
            "Pearson correlation",
            f"{correlation:.3f}"
        )

        metric_col2.metric(
            "Countries analyzed",
            len(factor_data)
        )

        
        
        chart_data = factor_data[
            [selected_factor, score_column]
        ].rename(
            columns={
                selected_factor: "Factor Value",
                score_column: "Life Evaluation"
            }
        )

        st.scatter_chart(
            chart_data,
            x="Factor Value",
            y="Life Evaluation",
            x_label=selected_factor_name,
            y_label="Life evaluation score",
            height=450,
            width="stretch"
        )



        st.dataframe(
            factor_data.sort_values(score_column, ascending=False),
            width="stretch",
            hide_index=True
        )
    else:
        st.warning("Not enough complete records to calculate a correlation.")


with rankings_tab:
    st.subheader("🏆 Country Ranking Explorer")

    st.write(
        "Explore the highest- and lowest-ranked countries "
        "for any reporting year available in the dataset."
    )

    available_years = sorted(
        df["Year"].unique(),
        reverse=True
    )

    ranking_year = st.selectbox(
        "Select reporting year",
        options=available_years,
        key="ranking_year"
    )

    ranking_type = st.radio(
        "Choose ranking",
        options=["Top countries", "Bottom countries"],
        horizontal=True
    )

    number_of_countries = st.slider(
        "Number of countries",
        min_value=5,
        max_value=20,
        value=10,
        step=5
    )

    year_data = df[df["Year"] == ranking_year].copy()

    if ranking_type == "Top countries":
        ranking_data = year_data.nsmallest(
            number_of_countries, "Rank"
        )
    else:
        ranking_data = year_data.nlargest(
            number_of_countries, "Rank"
        )

    ranking_data = ranking_data[
        ["Rank", "Country name", "Life evaluation (3-year average)"]
    ].sort_values("Rank")

    st.caption(
        f"Showing {len(ranking_data)} countries for {int(ranking_year)}."
    )

    st.dataframe(
        ranking_data,
        width="stretch",
        hide_index=True
    )

    csv_data = ranking_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Rankings as CSV",
        data=csv_data,
        file_name=f"wellbeing_rankings_{int(ranking_year)}.csv",
        mime="text/csv"
    )


    st.bar_chart(
        ranking_data.set_index("Country name")[
            "Life evaluation (3-year average)"
        ],
        x_label="Country",
        y_label="Life evaluation score",
        width="stretch"
    )


    st.subheader("💡 Wellbeing Insights")

    insight_year = st.selectbox(
        "Choose a year for the insights",
        options=sorted(df["Year"].unique(), reverse=True),
        key="insight_year"
    )

    insight_data = df[df["Year"] == insight_year].copy()

    highest = insight_data.loc[
        insight_data["Life evaluation (3-year average)"].idxmax()
    ]

    lowest = insight_data.loc[
        insight_data["Life evaluation (3-year average)"].idxmin()
    ]

    average_score = insight_data[
        "Life evaluation (3-year average)"
    ].mean()

    score_gap = (
        highest["Life evaluation (3-year average)"]
        - lowest["Life evaluation (3-year average)"]
    )


    highest_score = highest["Life evaluation (3-year average)"]
    lowest_score = lowest["Life evaluation (3-year average)"]
    highest_country = highest["Country name"]
    lowest_country = lowest["Country name"]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average life evaluation",
        f"{average_score:.2f}"
    )

    col2.metric(
        "Highest score",
        f"{highest['Life evaluation (3-year average)']:.3f}",
        help=f"Country: {highest['Country name']}"
    )

    col3.metric(
        "Lowest score",
        f"{lowest['Life evaluation (3-year average)']:.3f}",
        help=f"Country: {lowest['Country name']}"
    )

    st.markdown("### What stands out?")

    st.write(
        f"In {int(insight_year)}, **{highest['Country name']}** "
        f"has the highest reported life-evaluation score "
        f"({highest['Life evaluation (3-year average)']:.3f}), "
        f"while **{lowest['Country name']}** has the lowest "
        f"({lowest['Life evaluation (3-year average)']:.3f})."
    )

    st.write(
        f"The difference between these two scores is "
        f"**{score_gap:.3f} points**, across "
        f"{insight_data['Country name'].nunique()} countries."
    )

    st.caption(
        "These are descriptive findings from the selected year's "
        "reported data; they do not explain the causes of the differences."
    )


    st.subheader("🧹 Data Quality Report")

    st.write(
        "Review the completeness and consistency of the source dataset."
    )

    # Overall dataset statistics
    total_rows, total_columns = df.shape
    duplicate_count = int(df.duplicated().sum())
    missing_cell_count = int(df.isna().sum().sum())
    total_cells = total_rows * total_columns

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total records", f"{total_rows:,}")
    col2.metric("Total columns", total_columns)
    col3.metric("Duplicate rows", duplicate_count)
    col4.metric(
        "Missing cells",
        f"{missing_cell_count:,}",
        help=f"Out of {total_cells:,} total cells"
    )

    # Missing values by column
    missing_report = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isna().sum().values,
        "Missing Percentage": (
            df.isna().mean().values * 100
        ).round(2)
    })

    missing_report = missing_report.sort_values(
        "Missing Percentage",
        ascending=False
    )

    st.markdown("### Missing Values by Column")

    st.dataframe(
        missing_report,
        width="stretch",
        hide_index=True
    )

    # Available reporting years
    st.markdown("### Reporting Year Coverage")

    year_counts = (
        df.groupby("Year")["Country name"]
        .nunique()
        .reset_index(name="Countries")
        .sort_values("Year")
    )

    st.dataframe(
        year_counts,
        width="stretch",
        hide_index=True
    )

    # Export the quality report
    quality_csv = missing_report.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Missing-Values Report",
        data=quality_csv,
        file_name="wellbeing_data_quality_report.csv",
        mime="text/csv"
    )
