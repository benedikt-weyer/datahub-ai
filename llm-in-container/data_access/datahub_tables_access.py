import requests as r
from sqlalchemy import create_engine, inspect
import pandas as pd
import json as j
import pprint as pp


def get_table_names(without_docker = False):
    #create database engine
    database_url = f'postgresql://didex:didex@postgis:5432/didex'
    engine = create_engine(database_url)

    # Get the inspector
    inspector = inspect(engine)

    return inspector.get_table_names()


def get_datahub_tables():
    
    url = "http://localhost:8000/api/datalayers/datalayer/?format=json"
    
    json_response = r.get(url=url)
    rows = json_response.json()['data']
    
    columns_to_keep = ["id", "key", "name", "category", "related_to", "description", "database_unit", "temporal_coverage"]

    final_data = []

    for i,row in enumerate(rows):
        
        final_data.append(dict())
        data = {}
        for col in columns_to_keep:
            if row[col] == '' or []:
                data[col] =  'not available'
            else:
                data[col] = row[col]
        
        final_data[i] = data
    return final_data
## new func to pull data from datahub for datalayers