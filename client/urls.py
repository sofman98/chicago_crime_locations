import os

SERVER_URL = os.environ["SERVER_URL"]

GET_META_DATA_URL = f"{SERVER_URL}/get_meta_data"
GET_ALL_CRIMES_URL = f"{SERVER_URL}/get_all_chicago_crime_locations"
QUERY_CRIMES_URL = SERVER_URL + "/query"
