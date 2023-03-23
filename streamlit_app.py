import geopandas as gpd
import pydeck as pdk
import streamlit as st
import leafmap.foliumap as leafmap

from __version__ import version

URL_GEO = "https://github.com/renswvw/CircularCityIndexSpain/blob/main/data/processed/CCI/03_index/CCI_Index.gpkg?raw=true"
URL_DATA = "https://raw.githubusercontent.com/renswvw/CircularCityIndexSpain/main/data/processed/CCI/03_index/CCI_Index.csv"

DEFAULT_OPTION_AREA = "Spain"
DEFAULT_OPTION_FEATURE = "CCI"

AREA_TO_PREDICT_dict = {
    "Andalusia": "01", 
    "Aragon": "02",
    "Asturias": "03", 
    "Balearic Islands": "04",
    "Canarias": "05", 
    "Cantabria": "06",
    "Castile and Leon": "07", 
    "Castille-La Mancha": "08",
    "Catalonia": "09", 
    "Valencia": "10",
    "Extremadura": "11", 
    "Galicia": "12",
    "Madrid": "13", 
    "Murcia": "14",
    "Navarre": "15", 
    "Basque Country": "16",
    "La Rioja": "17",
    "Ceuta": "18",
    "Melilla": "19",
    "Minor Plazas de Soberanía": "20",
    }

header = st.container()
features_container = st.container()
dataset = st.container()
descriptive = st.container()
mapping = st.container()

# Header
with header:
    st.title(f"Circular City Index data")
    st.text(f"In this project a visualization tool is developed for the Circular City Index.\nThis index is applied on the case study of Spain.")

# Features
with features_container: 
    st.header(f"CCI features")

    feature = gpd.read_file(URL_GEO)
    feature = feature.iloc[: , 2:7] 
    features = feature.columns.values

    area_list = ["Spain", "Iberian Pensinula"] + list(AREA_TO_PREDICT_dict.keys())

    # select features for elevation & color
    option_area = st.selectbox(
        "Which area do you like to visualize?",
        area_list,
        index=area_list.index(DEFAULT_OPTION_AREA),
    )
    option_feature = st.selectbox(
        "Which feature do you like to visualize?",
        features,
        index=features.tolist().index(DEFAULT_OPTION_FEATURE),
    )

# Dataset
with dataset: 
    st.header(f"Dataset of {option_feature} in {option_area}")

    # Data
    gdf = gpd.read_file(URL_GEO)

    # Choose Study Area
    if option_area in AREA_TO_PREDICT_dict:
        gdf = gdf[gdf["CTOT"].str.contains(r'^' + AREA_TO_PREDICT_dict[option_area])]
    elif option_area == "Iberian Pensinula":
        gdf = gdf[~gdf.CTOT.str.contains(r'^04|^05|^18|^19|^20')] 
    elif option_area == "Spain":
        pass

    # Finalize dataframe
    gdf.set_index("CTOT", inplace=True)
    df = gdf.iloc[: , :-15] 

    st.dataframe(df)

# Dataset
with descriptive: 
    st.header(f"Descriptive statistics of {option_feature} in {option_area}")
    
    # Descriptive data
    st.subheader('Data summary')
    st.write(df.describe())

    # Bar Chart    
    st.subheader('Bar chart')
    st.bar_chart(df[option_feature])  

    #Line Chart        
    st.subheader('Line chart')
    st.line_chart(df[option_feature])    

# Map
with mapping: 
    st.header(f"Map of {option_feature} in {option_area}")
    
    m = leafmap.Map(minimap_control=True,
                    layers_control=True, 
                    measure_control=False, 
                    attribution_control=False)
    m.add_basemap("Stamen.TonerLite")
    m.add_data(gdf, 
               column=option_feature, 
               scheme='Quantiles', 
               cmap='coolwarm', 
               legend_title='CCI Score')
    m.zoom_to_gdf(gdf)
    m.to_streamlit(height=500)

# credits and version
st.markdown(
    f"Based on [streamlit-CircularCityIndexSpain](https://github.com/renswvw/streamlit-circularcityindexspain), v{version}"
)