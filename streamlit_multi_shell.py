import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
data = pd.read_csv('asylum-decisions.csv')

# Helper function to get asylum decision counts
def get_asylum_counts(df, group_by_column):
    return df.groupby([group_by_column])[
        ['Recognized decisions', 'Rejected decisions', 'Total decisions']].sum().reset_index()

# Page 1: Overview
def page_overview():
    st.subheader("Global Asylum Decisions by Year Range (Choose Range)")
    # Visualization code will go here

    year_filter = st.slider("Year Range", int(data['Year'].min()), int(data['Year'].max()),
                            (int(data['Year'].min()), int(data['Year'].max())))

    filtered_data = data[(data['Year'] >= year_filter[0]) & (data['Year'] <= year_filter[1])]
    asylum_counts = get_asylum_counts(filtered_data, 'Country of asylum')

    top_countries = asylum_counts.sort_values(by='Total decisions', ascending=False).head(10)

    fig_bar = px.bar(top_countries, x='Total decisions', y='Country of asylum', orientation='h',
                     title="Top 10 Countries by Total Asylum Decisions",
                     color='Total decisions', color_continuous_scale=px.colors.sequential.YlOrRd)
    fig_bar.update_layout(showlegend=False, height=400, yaxis={'categoryorder': 'total ascending'})
    fig_bar.update_coloraxes(showscale=False)  # Remove color scale
    st.plotly_chart(fig_bar)

    top_countries_origins = filtered_data[filtered_data['Country of asylum'].isin(top_countries['Country of asylum'])]
    fig_sunburst = px.sunburst(top_countries_origins, path=['Country of asylum', 'Country of origin'], values='Total decisions',
                               title="Top 10 Countries by Origin Breakdown",
                               color='Total decisions', color_continuous_scale=px.colors.qualitative.Bold)
    fig_sunburst.update_layout(height=600, showlegend=False)
    fig_sunburst.update_coloraxes(showscale=False)  # Remove color scale
    st.plotly_chart(fig_sunburst)

# Page 2: Country-Specific Analysis with Grouped Bar Chart
# Page 2: Country-Specific Analysis with Grouped Bar Chart
def page_country_analysis():
    st.subheader("Country-Specific Analysis")

    country = st.selectbox("Select Country", data['Country of asylum'].unique())
    country_data = data[data['Country of asylum'] == country]

    country_data_long = pd.melt(country_data, id_vars=['Year'],
                                value_vars=['Recognized decisions', 'Rejected decisions'],
                                var_name='Decision Type', value_name='Count')

    fig_grouped_bar = px.bar(country_data_long, x='Year', y='Count', color='Decision Type', barmode='group',
                             title=f"Asylum Decisions for {country} Over the Years",
                             labels={'Count': 'Number of Decisions'},
                             color_discrete_sequence=px.colors.sequential.OrRd)

    fig_grouped_bar.update_layout(height=400, showlegend=True)
    st.plotly_chart(fig_grouped_bar)

    total_decisions = country_data[
        ['Recognized decisions', 'Rejected decisions', 'Total decisions']].sum().reset_index()
    total_decisions.columns = ['Decision Type', 'Count']

    fig_horizontal_bar = px.bar(total_decisions, x='Count', y='Decision Type', orientation='h',
                                title=f"Total Asylum Decisions for {country}",
                                color='Decision Type', color_discrete_sequence=px.colors.sequential.Redor)

    fig_horizontal_bar.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig_horizontal_bar)

# Page 3: Choropleth Mapping
def page_choropleth():
    st.subheader("Global Distribution of Asylum Decisions")

    year = st.selectbox("Select Year", sorted(data['Year'].unique()), key='year_select')

    year_data = data[data['Year'] == year]
    asylum_counts = get_asylum_counts(year_data, 'Country of asylum')

    st.subheader(f"Global Distribution of Asylum Decisions in {year}")
    fig = px.choropleth(asylum_counts, locations="Country of asylum", locationmode='country names',
                        color="Total decisions",
                        hover_name="Country of asylum", color_continuous_scale=px.colors.sequential.YlOrBr)

    fig.update_layout(height=500)
    st.plotly_chart(fig)

    st.subheader(f"Asylum Decisions by Country in {year}")
    sorted_asylum_counts = asylum_counts.sort_values(by='Total decisions', ascending=False)

    st.dataframe(sorted_asylum_counts)

# Main app with navigation
def main():
    st.set_page_config(page_title="Asylum Decisions Dashboard", layout="wide", initial_sidebar_state="expanded")

    st.sidebar.title("Navigation")
    menu_options = ["Global Asylum Decisions", "Country Analysis", "Global Mapping"]
    menu_choice = st.sidebar.selectbox("Go to", menu_options)

    if menu_choice == "Global Asylum Decisions":
        page_overview()
    elif menu_choice == "Country Analysis":
        page_country_analysis()
    elif menu_choice == "Global Mapping":
        page_choropleth()

if __name__ == "__main__":
    main()
