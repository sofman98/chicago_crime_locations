"""
This module hosts the code for the dashboard UI.
"""
import streamlit as st
import functions

if __name__=="__main__":
    title = st.title('Display of crime locations in Chicago')

    # Get meta-data
    primary_types, earliest_crime_date, latest_crime_date = functions.get_meta_data()

    # initalize original data (entire dataset)
    ## Alternatively, we can get all data with query_crimes('ALL', earliest_crime_date, latest_crime_date)
    if 'data' not in st.session_state:
        st.session_state['data'] = functions.get_all_crime_locations()

    filter_header = st.header("Filter crimes")

    # Query filterers 
    # date pickers
    start_date = st.date_input(
        "Crimes that happened after",
        value=earliest_crime_date,
        min_value=earliest_crime_date
    )
    end_date = st.date_input(
        "Crimes that happened before",
        value=latest_crime_date,
        min_value=earliest_crime_date,
        max_value=latest_crime_date
    )
    # adding the option to select all types
    primary_type = st.selectbox('Select type of crime', ['ALL'] + primary_types)

    btn_column = st.columns(2)

    with btn_column[0]:
        query_button = st.button('FILTER')

    with btn_column[1]:
        show_all_button = st.button('SHOW ALL CRIME LOCATIONS')

    # do the query and retrieve the data
    if query_button:
        st.session_state.data = functions.query_crimes(primary_type, start_date, end_date)

    # Reset dashboard to show all data
    if show_all_button:
        st.session_state.data = functions.get_all_crime_locations()

    # map
    map_header = st.header("Map")
    map = st.map(st.session_state.data, zoom=9)