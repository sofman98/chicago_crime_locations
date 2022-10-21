"""
This module hosts the functions that communicate with the api.
"""
from datetime import datetime, date
from typing import List, Tuple, Union
import requests
import streamlit as st
import pandas as pd
import json
import urls

@st.cache
def get_meta_data() -> Tuple[List[str], date, date]:
    """
    Communicates with API to retrieve meta-data about the dataset.
    Args:
        (empty)
    Returns:
        (Tuple[List[str], date, date]): Respectively: 1- a list of the possible types of crimes, 
            2- the earliest crime date, 3- the latest crime date.
    """
    byte_content = requests.get(urls.GET_META_DATA_URL).content
    data_dict = json.loads(byte_content)

    primary_types = data_dict['primary_types']
    earliest_crime_date = datetime.strptime(data_dict['earliest_crime_date'], "%Y-%m-%d")
    latest_crime_date = datetime.strptime(data_dict['latest_crime_date'], "%Y-%m-%d")

    return primary_types, earliest_crime_date, latest_crime_date

@st.cache
def get_all_crime_locations() -> Union[pd.DataFrame, None]:
    """
    Communicates with API to retrieve all crime locations. Returns None if no data.
    Args:
        (empty)
    Returns:
        (Union[pd.DataFrame, None]): Dataframe with columns "latitude" and "longitude" containing
            the location info of all crimes. Returns None if no data.
    """
    byte_content = requests.get(urls.GET_ALL_CRIMES_URL).content
    data_dict = json.loads(byte_content)
    locations = data_dict['locations']
    if locations:
        data = pd.DataFrame(locations, columns=['latitude', 'longitude'])
        return data

    return None

@st.cache
def query_crimes(
        primary_type: str,
        start_date: date,
        end_date: date
    ) -> Union[pd.DataFrame, None]:
    """
    Communicates with API to query data by providing the type of the crime and the interval of time in which it happened.
    Args:
        - primary_type (str): type of crime committed.
        - start_date (date): date at which we consider crimes.
        - end_date (date): date to which we consider crimes.
    Returns:
        (Union[pd.DataFrame, None]): Dataframe with columns "latitude" and "longitude" containing
            the location info of matching crimes. Returns None if no data.
    """
    # give the "ALL" option the regex code for all possible names
    if primary_type == 'ALL':
        primary_type = '%'

    url = urls.QUERY_CRIMES_URL.format(primary_type=primary_type, start_date=start_date, end_date=end_date)

    byte_content = requests.get(url).content
    data_dict = json.loads(byte_content)
    locations = data_dict['locations']
    if locations:
        data = pd.DataFrame(locations, columns=['latitude', 'longitude'])
        return data

    return None