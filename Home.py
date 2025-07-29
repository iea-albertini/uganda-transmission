import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="National Grid Tool", layout="wide")

# Create two tabs
tab1, tab2, tab3 = st.tabs(["📘 Project Overview", "📊 Scenario Results", "📊 Investment planning"])

# ----------------------
# 📘 Project Overview Tab
# ----------------------
with tab1:
    st.title("🔌Ugandan National Grid Extension Planning Tool")

    st.markdown("""
    Welcome to the **National Grid Extension Planning Platform**.

    This application supports strategic planning by visualizing scenarios for extending the national electricity grid using geospatial data and model outputs.

    ### 🧭 Objectives
    - Analyze geographic and infrastructure constraints
    - Visualize model-based scenarios for grid expansion
    - Compare coverage efficiency across different scenarios
    - Empower planners with interactive map tools
    """)

# ----------------------
# 📊 Scenario Results Tab
# ----------------------
import geopandas as gpd
import branca.colormap as cm

with tab2:
    st.title("📊 Scenario Results")

    st.sidebar.header("🔎 Filter Options")
    scenario = st.sidebar.selectbox("Choose a Scenario", ["Base Case", "Industrial scenario", "Socio-enviornmental scenario"], key="scenario1")

    st.markdown(f"### Scenario: **{scenario}**")

    # Load grid_normalised layer
    grid_path = r"G:\EO2025\Analysis\Investment\Africa\1_Country Studies\Uganda\GIS\_Layers LA\Output\grid_normalised.gpkg"
    grid_gdf = gpd.read_file(grid_path)

    # Check columns and CRS
    st.write("Columns:", grid_gdf.columns)
    st.write("CRS:", grid_gdf.crs)

    # Convert to WGS84 (EPSG:4326) for folium
    grid_gdf = grid_gdf.to_crs(epsg=4326)

    # Assume 'value' is the pixel attribute column - replace with actual column name if different
    value_col = "scenario_1"  # <-- change this if needed, e.g. "pixel_val", "grid_value"

    # Prepare color scale (white to red)
    min_val = grid_gdf[value_col].min()
    max_val = grid_gdf[value_col].max()

    colormap = cm.LinearColormap(colors=["white", "red"], vmin=min_val, vmax=max_val)
    colormap.caption = "Grid Normalized Value"

    def style_function(feature):
        val = feature['properties'][value_col]
        return {
            'fillColor': colormap(val),
            'color': colormap(val),
            'weight': 0.2,
            'fillOpacity': 0.7,
        }

    # Create Folium map centered on Uganda
    m = folium.Map(location=[1.3733, 32.2903], zoom_start=7)

    # Add GeoJson layer with styled pixels
    folium.GeoJson(
        grid_gdf.to_json(),
        name="Grid Normalized Pixels",
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=[value_col], aliases=["Value:"])
    ).add_to(m)

    # Add color legend
    colormap.add_to(m)

    st_folium(m, width=900, height=500)

    # Add summary data below map
    st.markdown("### 📄 Summary Data")
    df = pd.DataFrame({
        "Region": ["North", "East", "South", "West"],
        "New Connections": [14000, 12500, 16000, 9800],
        "Cost (M$)": [15.2, 12.8, 18.1, 10.9]
    })
    st.dataframe(df)

# ----------------------
# 📊 Investment planning Tab
# ----------------------
with tab3:
    st.title("📊 Investment Planning")

    st.markdown(f"### Investment Scenario: **{scenario}**")

    import geopandas as gpd

    # File path to transmission lines
    lines_path = r"G:\EO2025\Analysis\Investment\Africa\1_Country Studies\Uganda\GIS\_Layers LA\Output\greenfield_lines_prior.gpkg"
    lines_gdf = gpd.read_file(lines_path)

    # Convert CRS if needed
    lines_gdf = lines_gdf.to_crs(epsg=4326)

    # Define color mapping function based on 'line_prior'
    def get_priority_color(val):
        if val == 0:
            return "#D3D3D3"  # Light gray - no priority
        elif val <= 0.000001161:
            return "#ffffcc"  # Light yellow - low
        elif val <= 0.000004681:
            return "#ffeda0"  # Mid
        elif val <= 0.000007093:
            return "#feb24c"  # Mid-high
        elif val <= 0.000012036:
            return "#f03b20"  # High
        else:
            return "#bd0026"  # Extreme (if above range)

    # Folium map setup
    m = folium.Map(location=[1.3733, 32.2903], zoom_start=7)

    # Add styled transmission lines
    folium.GeoJson(
        lines_gdf.to_json(),
        name="Transmission Lines",
        style_function=lambda feature: {
            'color': get_priority_color(feature['properties']['line_prior']),
            'weight': 3,
            'opacity': 0.9,
        },
        tooltip=folium.GeoJsonTooltip(fields=["line_prior"], aliases=["Line Priority:"])
    ).add_to(m)

    # Add legend manually using HTML
    legend_html = """
    <div style="
        position: fixed; 
        bottom: 30px; left: 30px; width: 220px; height: 160px; 
        background-color: white;
        border:2px solid grey;
        z-index:9999;
        font-size:14px;
        padding: 10px;
    ">
    <b>Line Priority Legend</b><br>
    <i style="background:#D3D3D3; width:10px; height:10px; display:inline-block;"></i> No priority<br>
    <i style="background:#ffffcc; width:10px; height:10px; display:inline-block;"></i> Low<br>
    <i style="background:#ffeda0; width:10px; height:10px; display:inline-block;"></i> Mid<br>
    <i style="background:#feb24c; width:10px; height:10px; display:inline-block;"></i> Mid-High<br>
    <i style="background:#f03b20; width:10px; height:10px; display:inline-block;"></i> High<br>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Display map
    st_folium(m, width=900, height=500)

    # Summary table
    st.markdown("### 📄 Investment Summary Data")
    df = pd.DataFrame({
        "Region": ["North", "East", "South", "West"],
        "Investment Cost (M$)": [20.1, 18.3, 22.5, 15.7],
        "Expected New Connections": [15000, 13000, 17000, 10500]
    })
    st.dataframe(df)