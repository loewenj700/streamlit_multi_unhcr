import streamlit as st

# Page 1: Overview
def page_overview():
    st.subheader("Global Asylum Decisions by Year Range (Choose Range)")
    # Visualization code will go here


# Page 2: Country-Specific Analysis with Grouped Bar Chart
def page_country_analysis():
    st.subheader("Country-Specific Analysis")

# Page 3: Choropleth Mapping
def page_choropleth():
    st.subheader("Global Distribution of Asylum Decisions")

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
