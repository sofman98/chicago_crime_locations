"""
This modules house the API that communicates with chicago_crime BigQuery public dataset.
"""
from datetime import date
from typing import Any, Dict, List, Union
from fastapi import FastAPI
from google.cloud import bigquery
import pandas as pd

app = FastAPI()

@app.on_event('startup')
def set_credentials() -> None:
  """
  instantiate client object.
  Args:
    (empty)
  Returns:
    (None)
  """

  global client
  client = bigquery.Client()

  return

@app.get("/get_all_chicago_crimes")
def get_all_chicago_crimes() -> Dict[str, List[Any]]:
  """
    Retrieves all crime locations.
    Args:
        (empty)
    Returns:
        (Dict[str, List[Any]]): A list of dictionnaries containing the location info of all crimes of the form:
        [{"latitude":0, "longitude":0}, {"latitude":1, "longitude":1}..etc]
  """

  sql_query = """
  SELECT latitude, longitude FROM `bigquery-public-data.chicago_crime.crime`
  WHERE latitude IS NOT NULL
  AND latitude IS NOT NULL
  LIMIT 100
  """
  data = pd.read_gbq(sql_query).to_dict('records')

  return {'records': data}


@app.get("/query")
def filter(
    primary_type: Union[str, None] = None,
    start_date: Union[date, None] = None,
    end_date: Union[date, None] = None
  ) -> Dict[str, List[Any]]:
  """
    Queries data by providing the type of the crime and the interval of time in which it happened.
    Args:
        - primary_type (str): type of crime committed.
        - start_date (date): date at which we consider crimes.
        - end_date (date): date to which we consider crimes.
    Returns:
        (Dict[str, List[Any]]): A list of dictionnaries containing the location info of matching crimes of the form:
        [{"latitude":0, "longitude":0}, {"latitude":1, "longitude":1}..etc]
  """
  sql_query = f"""
  SELECT latitude, longitude FROM `bigquery-public-data.chicago_crime.crime`
  WHERE latitude IS NOT NULL
  AND latitude IS NOT NULL
  AND primary_type LIKE '{primary_type}'
  AND CAST(date AS date) BETWEEN '{start_date}' AND '{end_date}'
  LIMIT 100
  """
  data = pd.read_gbq(sql_query).to_dict('records')
  print('HEEELLO', data)

  return {'records': data}

@app.get("/get_meta_data")
def get_meta_data() -> Dict[str, Any]:
  all_types_query = """
  SELECT DISTINCT primary_type FROM `bigquery-public-data.chicago_crime.crime`
  """
  earliest_crime_query = """
  SELECT MIN(date) FROM `bigquery-public-data.chicago_crime.crime`
  """
  latest_crime_query = """
  SELECT MAX(date) FROM `bigquery-public-data.chicago_crime.crime`
  """

  primary_types = list(pd.read_gbq(all_types_query).primary_type)
  earliest_crime_date = pd.read_gbq(earliest_crime_query).iloc[0,0].strftime("%Y-%m-%d")
  latest_crime_date = pd.read_gbq(latest_crime_query).iloc[0,0].strftime("%Y-%m-%d")

  return {
    'primary_types': primary_types,
    'earliest_crime_date': earliest_crime_date,
    'latest_crime_date': latest_crime_date
  }