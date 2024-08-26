import geopandas as gpd
from sqlalchemy import create_engine
import streamlit as st
import json
import pydeck as pdk



try:
    rm_engine = create_engine("postgresql://avnadmin:AVNS_drnigVKFhgmc5xXyLik@pg-feb329b-students-d10e.h.aivencloud.com:22970/defaultdb")
    print("DB Connected !!")
except Exception as e:
    print("DB Connection Error: ", e)

# load data from remote server
gdf = gpd.read_postgis("SELECT * FROM us_states;", rm_engine)

# convert gj str 
gj_str = gdf.to_json()

gj = json.loads(gj_str)
# print(gj)

st.markdown(""" ## Application """)

st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=32.76,
            longitude=-105.4,
            zoom=3,
        ),
        layers=[
            pdk.Layer(
            "GeoJsonLayer",
            gj,
            opacity=0.8,
            stroked=False,
            filled=True,
            extruded=True,
            wireframe=True,
            get_elevation="properties.valuePerSqm / 20",
            get_fill_color="[255, 255, properties.growth * 255]",
            get_line_color=[255, 255, 255],
        )
        ],
    )
)