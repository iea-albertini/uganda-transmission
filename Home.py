import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="National Grid Tool", layout="wide")

# Create two tabs
tab1, tab2, tab3, tab4 = st.tabs(["📘 Project Overview","📊 Input layers" ,"📊 Scenario Results", "📊 Investment planning"])

with tab1:
    st.title("🔌 Ugandan National Grid Extension Planning Tool")

    st.markdown("""
    Welcome to the **National Grid Extension Planning Platform**.

    This application supports strategic planning by visualizing scenarios for extending the national electricity grid using geospatial data and model outputs.

    ### 🧭 Objectives
    - Analyze geographic and infrastructure constraints
    - Visualize model-based scenarios for grid expansion
    - Compare coverage efficiency across different scenarios
    - Empower planners with interactive map tools
    """)

    st.markdown("---")

    st.markdown(
        "#### Project Summary\n"
        "This project examines the intersection of electricity infrastructure expansion plans with critical mineral operations, productive uses, and other relevant future access plans. The analysis is based on ATMS STRATEGY. "
        "This includes an assessment of the historical investment into Uganda’s transmission grid infrastructure, cost of capital of transmission projects and multi criteria analysis. "
        "The project brings this together with a prioritisation of future grid projects and provide policy recommendations to the Government on how to scale investment, including international case studies of best practice."
    )

    st.markdown("---")

    # Button to download report
    with open("Report.pdf", "rb") as file:
        report_bytes = file.read()

    st.download_button(
        label="📥 Download Project Report",
        data=report_bytes,
        file_name="Uganda_Grid_Extension_Report.pdf",
        mime="application/pdf"
    )

    # Button to download GIS inputs as a ZIP file
    with open("input.zip", "rb") as file:
        gis_zip = file.read()

    st.download_button(
        label="📥 Download GIS Input Files",
        data=gis_zip,
        file_name="Uganda_Grid_GIS_Inputs.zip",
        mime="application/zip"
    )

    # Optional: Add contact or resources
    st.markdown("""
    ---
    For questions or support, please contact [lorenzo.albertini@iea.org](mailto:lorenzo.albertini@iea.org) or [adam.ward@iea.org](mailto:adam.ward@iea.org).
    """)

    # Optional: Add a small logo/image
    # st.image("path/to/logo.png", width=150)

    def zip_gis_files(folder_path):
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, "w") as z:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    # Save file preserving folder structure inside zip
                    arcname = os.path.relpath(full_path, start=folder_path)
                    z.write(full_path, arcname)
        buffer.seek(0)
        return buffer

    with tab1:
        if st.button("Prepare and Download GIS Inputs"):
            gis_zip_buffer = zip_gis_files("data")
            st.download_button(
                label="Download GIS Data ZIP",
                data=gis_zip_buffer,
                file_name="GIS_Inputs.zip",
                mime="application/zip"
            )

    import zipfile
    import os
    from io import BytesIO

    with tab1:
        with st.expander("❓ Frequently Asked Questions (FAQ)"):
            st.write("**Q:** What data sources are used?\n\nA: Data comes from Uganda’s Ministry of Energy and Water.")
            st.write("**Q:** How often is data updated?\n\nA: Annually or as new surveys are released.")
            # Add more Q&A here

        with st.expander("💡 Tips for Using the Tool"):
            st.write("- Use checkboxes to toggle GIS layers on the map.")
            st.write("- Hover over lines and points for attribute details.")
            st.write("- Download reports and GIS files for offline analysis.")

# ----------------------
# 📊 Input tab
# ----------------------
import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

with tab2:
    st.title("📊 Input Layers Overview")

    st.markdown("""
    This page is used to show and analyse all the inputs included in the multi-criteria analysis.
    Power sector information, as well as socio-economic indicators are displayed.
    Use the checkboxes below to select GIS layers to display and explore.
    """)

    # Load GIS data (adjust paths as needed)
    transmission_lines_gdf = gpd.read_file(r"data/Transmission_lines.gpkg")
    substations_gdf = gpd.read_file(r"data/Substations.gpkg")
    trainlines_gdf = gpd.read_file(r"data/SGR trainlines.gpkg")
    industries_gdf = gpd.read_file(r"data/industrial_parks.gpkg")

    # Checkboxes for each layer
    show_transmission_lines = st.checkbox("Transmission Lines")
    show_substations = st.checkbox("Substations")
    show_trainlines = st.checkbox("Standard Gauge Railway Uganda")
    show_industrial_parks = st.checkbox("Industrial parks")

    # Create base map
    m = folium.Map(location=[1.3733, 32.2903], zoom_start=7)

        # Add layers to map based on checkbox
        # Ask user how to color transmission lines
    color_by = st.radio(
        "Color Transmission Lines by:",
        options=["voltage_kv", "status"]
    )

    # Define color maps for voltage or status
    def style_function(feature):
        if color_by == "voltage_kv":
            voltage = feature['properties'].get('voltage_kv', 0)
            # Example: assign color by voltage ranges
            if voltage >= 220:
                color = "red"
            elif voltage >= 110:
                color = "orange"
            else:
                color = "green"
        else:  # color_by == "status"
            status = feature['properties'].get('status', '').lower()
            if status == "existing":
                color = "green"
            elif status == "under construction":
                color = "orange"
            else:
                color = "gray"
        return {
            "color": color,
            "weight": 3,
            "opacity": 0.8
        }

    if show_transmission_lines:
        folium.GeoJson(
            transmission_lines_gdf.to_crs(epsg=4326).to_json(),
            name="Transmission Lines",
            tooltip=folium.GeoJsonTooltip(fields=["voltage_kv", "status"], aliases=["Voltage (kV):", "Status:"]),
            style_function=style_function
        ).add_to(m)
    
    if show_substations:
        folium.GeoJson(
            substations_gdf.to_crs(epsg=4326).to_json(),
            name="Substations",
            tooltip=folium.GeoJsonTooltip(fields=["Voltage_kV", "status"], aliases=["Voltage (kV):", "Status:"])
        ).add_to(m)

    if show_trainlines:
        folium.GeoJson(
            trainlines_gdf.to_crs(epsg=4326).to_json(),
            name="Standard Gauge Railway Uganda"
        ).add_to(m)

    if show_industrial_parks:
        folium.GeoJson(
            industries_gdf.to_crs(epsg=4326).to_json(),
            name="Industrial Parks",
            tooltip=folium.GeoJsonTooltip(fields=["Name", "Status", "Type"], aliases=["Name:", "Status:", "Typology:"])
        ).add_to(m)

    # Display the map in Streamlit
    st_folium(m, width=900, height=500)

    # Show summary statistics for Transmission Lines if selected
    if show_transmission_lines:
        st.markdown("### Transmission Lines Summary")
        st.write(f"Total km of lines: XXXXX km")
        st.write(f"Under construction km: YYYYY km")
        st.write(f"Existing km: ZZZZZ km")
        
    if show_substations:
        st.markdown("### Substations Summary")
        st.write(f"Total of XXX operational substations for a total of ZZZ kW")
        st.write(f"Total of XXX under construction substations for a total of ZZZ kW")

# ----------------------
# 📊 Results of optimisation
# ----------------------
import geopandas as gpd
import branca.colormap as cm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import folium
from streamlit_folium import st_folium

with tab3:
    st.title("📊 Scenario Results")

    st.sidebar.header("🔎 Filter Options")
    scenario = st.sidebar.selectbox(
        "Choose a Scenario",
        ["Base Case", "Industrial scenario", "Socio-environmental scenario"],
        key="scenario1"
    )

    st.markdown(f"### Scenario: **{scenario}**")

    # Load grid_normalised layer
    grid_path = r"data/grid_normalised.gpkg"
    grid_gdf = gpd.read_file(grid_path)

    # Convert to WGS84 for folium
    grid_gdf = grid_gdf.to_crs(epsg=4326)

    # Map scenario selection to column names
    scenario_to_col = {
        "Base Case": "scenario_1",
        "Industrial scenario": "scenario_2",
        "Socio-environmental scenario": "scenario_3"
    }
    value_col = scenario_to_col.get(scenario, "scenario_1")

    # Prepare color scale
    min_val = grid_gdf[value_col].min()
    max_val = grid_gdf[value_col].max()
    colormap = cm.LinearColormap(colors=["white", "red"], vmin=min_val, vmax=max_val)
    colormap.caption = f"{scenario} - Grid Normalized Value"

    # Threshold slider for filtering "high-value" areas
    threshold = st.slider(
        "Set threshold to highlight high-value areas",
        min_value=float(min_val),
        max_value=float(max_val),
        value=float(min_val + (max_val - min_val)*0.8),
        step=0.01
    )

    def style_function(feature):
        val = feature['properties'][value_col]
        fill_color = colormap(val)
        # Optionally highlight polygons above threshold with thicker border or different color
        border_color = 'black' if val >= threshold else fill_color
        weight = 1.5 if val >= threshold else 0.2
        return {
            'fillColor': fill_color,
            'color': border_color,
            'weight': weight,
            'fillOpacity': 0.7,
        }

    # Create folium map
    m = folium.Map(location=[1.3733, 32.2903], zoom_start=7)

    folium.GeoJson(
        grid_gdf.to_json(),
        name="Grid Normalized Pixels",
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=[value_col], aliases=["Value:"])
    ).add_to(m)

    # Add dynamic legend
    colormap.add_to(m)

    st_folium(m, width=900, height=500)

    # Summary statistics below map
    st.markdown("### 📊 Scenario Summary Statistics")

    mean_val = grid_gdf[value_col].mean()
    median_val = grid_gdf[value_col].median()
    max_val = grid_gdf[value_col].max()
    min_val = grid_gdf[value_col].min()
    count_above_threshold = (grid_gdf[value_col] >= threshold).sum()

    st.markdown(f"""
    - **Mean value:** {mean_val:.3f}  
    - **Median value:** {median_val:.3f}  
    - **Maximum value:** {max_val:.3f}  
    - **Minimum value:** {min_val:.3f}  
    - **Number of areas above threshold ({threshold:.3f}):** {count_above_threshold}
    """)

    st.markdown("""
    This summary provides a quick overview of the distribution of normalized grid values for the selected scenario. 
    Areas with values above the threshold are highlighted on the map and counted here.
    """)

    # Histogram chart with random data (replace with actual data later)
    st.markdown("### 📈 Histogram of Grid Values (Sample Data) NUMBER ARE RANDOM FOR NOW")

    # For now, generate random data matching grid size for demo
    sample_data = np.random.normal(loc=mean_val, scale=(max_val - min_val)/4, size=len(grid_gdf))
    fig, ax = plt.subplots()
    ax.hist(sample_data, bins=30, color='red', alpha=0.7)
    ax.set_xlabel('Grid Normalized Value')
    ax.set_ylabel('Frequency')
    ax.set_title(f"Histogram of {scenario} Grid Values")

    st.pyplot(fig)


# ----------------------
# 📊 Investment planning Tab
# ----------------------
with tab4:
    st.title("📊 Investment Planning")

    st.markdown(f"### Investment Scenario: **{scenario}**")

    import geopandas as gpd
    import pandas as pd
    import numpy as np

    # File path to transmission lines
    lines_path = r"data/greenfield_lines_prior.gpkg"
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
        else:
            return "#f03b20"  # High (catch all above 0.000007093)

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
    <i style="background:#ffffcc; width:10px; height:10px; display:inline-block;"></i> Low priority<br>
    <i style="background:#ffeda0; width:10px; height:10px; display:inline-block;"></i> Mid priority<br>
    <i style="background:#feb24c; width:10px; height:10px; display:inline-block;"></i> Mid-High priority<br>
    <i style="background:#f03b20; width:10px; height:10px; display:inline-block;"></i> High priority<br>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Display map
    st_folium(m, width=900, height=500)

    # === New summary table by priority ===
    bins = [-np.inf, 0, 0.000001161, 0.000004681, 0.000007093, np.inf]
    labels = [
        "No priority",
        "Low priority",
        "Mid priority",
        "Mid-High priority",
        "High priority"
    ]

    lines_gdf['priority_category'] = pd.cut(lines_gdf['line_prior'], bins=bins, labels=labels)

    # Dummy data if missing — replace with real columns if you have them
    if 'investment_cost_million' not in lines_gdf.columns:
        np.random.seed(42)
        lines_gdf['investment_cost_million'] = np.random.uniform(0.1, 1.0, size=len(lines_gdf))

    if 'expected_new_connections' not in lines_gdf.columns:
        np.random.seed(24)
        lines_gdf['expected_new_connections'] = np.random.randint(100, 1000, size=len(lines_gdf))

    summary_df = lines_gdf.groupby('priority_category').agg(
        total_investment_cost_million=pd.NamedAgg(column='investment_cost_million', aggfunc='sum'),
        total_expected_connections=pd.NamedAgg(column='expected_new_connections', aggfunc='sum'),
        line_count=pd.NamedAgg(column='line_prior', aggfunc='count')
    ).reset_index()

    st.markdown("### 📄 Investment Summary Data by Priority - NUMBER ARE NOT CORRECT")
    st.dataframe(summary_df)
