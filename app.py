from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Union
import pandas as pd
import json

from travel_app_backend.utils import get_distance
from travel_app_backend.mst import mst, plot_map

app = FastAPI()

with open("./data/distance_between_cities.json", "r") as f:
    data = json.load(f)
    f.close()

df = pd.read_csv("./data/backpacking_cities_processed.csv")

class citiesList(BaseModel):
    selected_cities: list[str]

@app.get("/get_route", response_class=HTMLResponse)
def get_route(cities: citiesList):

    sub_df = df[df["City"].isin(cities.selected_cities)]
    query_term = list(sub_df["query_term"])

    subset_data = list(filter(lambda x: (x["city_1"] in query_term) & (x["city_2"] in query_term), data))

    driving_distance = get_distance(subset_data)

    T = mst(driving_distance)
    map_route = plot_map(T, data)

    return map_route.get_root().render()
