"""
This modules house the API that communicates with chicago_crime BigQuery public dataset.
"""
from datetime import date
from typing import Any, Dict, List, Tuple, Union
from fastapi import FastAPI
import pandas as pd

app = FastAPI()


@app.get("/get_all_chicago_crime_locations")
def get_all_chicago_crime_locations() -> Dict[str, List[Tuple[float, float]]]:
    """
    Retrieves all crime locations.
    Args:
        (empty)
    Returns:
        (Dict[str, List[Tuple[float, float]]]): a dict with 'locations' as key and as value a list of tuples containing the location info of all crimes in the form:
        [(latitude1, longitude1), (latitude2, longitude2)..etc]
    """

    sql_query = """
  SELECT latitude, longitude FROM `bigquery-public-data.chicago_crime.crime`
  WHERE latitude IS NOT NULL
  AND longitude IS NOT NULL
  LIMIT 100
  """
    data = pd.read_gbq(sql_query).to_records(index=False).tolist()

    return {"locations": data}


@app.get("/query")
def query_chicago_crime_locations(
    primary_type: Union[str, None] = None,
    start_date: Union[date, None] = None,
    end_date: Union[date, None] = None,
) -> Dict[str, List[Tuple[float, float]]]:
    """
    Queries data by providing the type of the crime and the interval of time in which it happened.
    Args:
        - primary_type (str): type of crime committed.
        - start_date (date): date at which we consider crimes.
        - end_date (date): date to which we consider crimes.
    Returns:
        (Dict[str, List[Tuple[float, float]]]): a dict with 'locations' as key and as value a list of tuples containing the location info of matching crimes in the form:
        [(latitude1, longitude1), (latitude2, longitude2)..etc]
    """
    sql_query = f"""
  SELECT latitude, longitude FROM `bigquery-public-data.chicago_crime.crime`
  WHERE latitude IS NOT NULL
  AND longitude IS NOT NULL
  AND primary_type LIKE '{primary_type}'
  AND CAST(date AS date) BETWEEN '{start_date}' AND '{end_date}'
  LIMIT 100
  """
    data = pd.read_gbq(sql_query).to_records(index=False).tolist()

    return {"locations": data}


@app.get("/get_meta_data")
def get_meta_data() -> Dict[str, Any]:
    """
    Sends meta-data about the dataset to query it, this includes: 1. all crime types; 2. the earliest crime date; 3. the latest crime date.
    Args:
     (Empty)
    Returns:
      (Dict[str, Any]): A dictionnary with 3 elements corresponding to: 1- a list of the possible types of crimes,
              2- the earliest crime date, 3- the latest crime date.
    """
    all_types_query = """
  SELECT DISTINCT primary_type FROM `bigquery-public-data.chicago_crime.crime`
  WHERE latitude IS NOT NULL
  AND longitude IS NOT NULL
  """
    earliest_crime_query = """
  SELECT MIN(date) FROM `bigquery-public-data.chicago_crime.crime`
  WHERE latitude IS NOT NULL
  AND longitude IS NOT NULL
  """
    latest_crime_query = """
  SELECT MAX(date) FROM `bigquery-public-data.chicago_crime.crime`
  WHERE latitude IS NOT NULL
  AND longitude IS NOT NULL
  """

    primary_types = pd.read_gbq(all_types_query).primary_type.tolist()
    earliest_crime_date = (
        pd.read_gbq(earliest_crime_query).iloc[0, 0].strftime("%Y-%m-%d")
    )
    latest_crime_date = pd.read_gbq(latest_crime_query).iloc[0, 0].strftime("%Y-%m-%d")

    return {
        "primary_types": primary_types,
        "earliest_crime_date": earliest_crime_date,
        "latest_crime_date": latest_crime_date,
    }
