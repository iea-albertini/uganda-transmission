import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from urllib.parse import urlencode

st.set_page_config(page_title="Scenario Results", layout="wide")

st.title("📊 Scenario Results – National Grid Extension")

# Navigation back to Home
if st.button("🏠 Back to Home Page"):
    query_params = urlencode({"page": "home"})
    st.markdown(f'<meta http-equiv="refresh" content="0;URL=/?{query_params}">', unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("Filter Options")
scenario = st.sidebar.selectbox("Choose a Scenario", ["Base Case", "High Demand", "Renewables Priority"])
year = st.sidebar.slider("Year", 2023, 2040, 2025)

# Map and summary
st.markdown(f"### Scenario: **{scenario}** | Year: **{year}**")

m = folium.Map(location=[9.145, 40.4897], zoom_start=6)
folium.Marker([9.145, 40.4897], tooltip="Proposed Substation").add_to(m)
folium.Circle([9.0, 40.0], radius=30000, color="blue", fill=True, tooltip="Grid Coverage").add_to(m)
st_folium(m, width=900, height=500)

st.markdown("### 📄 Summary Data")
df = pd.DataFrame({
    "Region": ["North", "East", "South", "West"],
    "New Connections": [14000, 12500, 16000, 9800],
    "Cost (M$)": [15.2, 12.8, 18.1, 10.9]
})
st.dataframe(df)