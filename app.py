from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from pydantic import BaseModel
from typing import Union, List
import pandas as pd
import json

from travel_app_backend.utils import get_distance
from travel_app_backend.mst import mst, plot_map

app = FastAPI()

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


with open("./data/distance_between_cities.json", "r") as f:
    data = json.load(f)
    f.close()

df = pd.read_csv("./data/backpacking_cities_processed.csv")

class citiesList(BaseModel):
    selected_cities: List[str]

@app.get("/get_route")
async def get_route(cities: citiesList = Query(...)):

    sub_df = df[df["City"].isin(cities.selected_cities)]
    query_term = list(sub_df["query_term"])

    subset_data = list(filter(lambda x: (x["city_1"] in query_term) & (x["city_2"] in query_term), data))

    mean_latitude = sub_df['latitude'].mean()
    mean_longitude = sub_df['longitude'].mean()

    driving_distance = get_distance(subset_data)

    T = mst(driving_distance)
    map_route = plot_map(T, subset_data, mean_longitude, mean_latitude)

    map_html = map_route.get_root().render()

    return map_html
