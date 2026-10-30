import pandas as pd
import plotly.express as px
import streamlit as st

# Configure page layout
st.set_page_config(
    page_title="Global Literacy and Socioeconomic Dashboard",
    layout="wide",
)

# --- 1. DATA LOADING AND CACHING ---
@st.cache_data
def load_data():
   # Load the CSV file directly from the project directory
    df = pd.read_csv("cross-country-literacy-rates.csv")
    df.columns = [col.strip() for col in df.columns]
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# Clean up column names and handle data structure
# The dataset typically contains: Entity, Code, Year, and the literacy rate column
literacy_col = [col for col in df.columns if "literacy" in col.lower() or "rate" in col.lower()]
if literacy_col:
    val_col = literacy_col[0]
else:
    val_col = df.columns[-1]

# Filter for the most recent year available per country to make a clean global ranking
if "Year" in df.columns and "Entity" in df.columns:
    latest_df = df.sort_values("Year").groupby("Entity").tail(1).reset_index(drop=True)
else:
    latest_df = df

# --- 2. SIDEBAR CONFIGURATION (INTERACTIVE WIDGETS) ---
st.sidebar.header("Dashboard Controls")

st.sidebar.markdown(
    "Use the controls below to filter countries and customize visualization parameters."
)

# Widget 1: Slider for minimum literacy rate threshold
min_literacy = st.sidebar.slider(
    "Minimum Literacy Rate (%)",
    min_value=0.0,
    max_value=100.0,
    value=50.0,
    step=5.0
)

# Filter dataframe based on slider and drop nulls
filtered_df = latest_df[latest_df[val_col] >= min_literacy].dropna(subset=[val_col])

# Widget 2: Checkbox to show raw data table
show_raw_data = st.sidebar.checkbox("Show Raw Data Table", value=False)


# --- 3. MAIN APP LAYOUT AND SECTIONS ---

# Section 1: Overview
st.title("Global Literacy and Socioeconomic Insights")
st.markdown("""
Welcome to the Global Literacy Dashboard. This interactive web application investigates global literacy rates across different countries and regions. 
Use this platform to examine disparities, analyze distributions, and uncover developmental trends worldwide.
""")

st.divider()

# Section 2: Data Display and Summary Metrics
st.header("Dataset Overview and Summary Metrics")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Records Analyzed", value=len(latest_df))
with col2:
    avg_literacy = latest_df[val_col].mean()
    st.metric(label="Average Global Literacy Rate", value=f"{avg_literacy:.1f}%")
with col3:
    st.metric(label="Countries Meeting Filter", value=len(filtered_df))

if show_raw_data:
    st.subheader("Raw Dataset Preview")
    st.dataframe(filtered_df.head(100), use_container_width=True)

st.divider()

# Section 3: Interactive Visualizations (Plotly)
st.header("Interactive Data Visualizations")

st.markdown("""
The chart below illustrates the distribution of literacy rates across countries. You can hover over individual bars to inspect specific national statistics.
""")

# Plotly Visualization: Bar chart with proper axes, title, and legend
chart_data = filtered_df.sort_values(by=val_col, ascending=False).head(30)

fig = px.bar(
    chart_data,
    x="Entity",
    y=val_col,
    title=f"Top Countries by Literacy Rate (Min: {min_literacy}%)",
    labels={"Entity": "Country", val_col: "Literacy Rate (%)"},
    color=val_col,
    color_continuous_scale="Viridis",
)

fig.update_layout(
    xaxis_tickangle=-45,
    template="plotly_white",
    height=550
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Section 4: Key Insights
st.header("Key Insights")
st.markdown("""
* **Regional Disparities:** Significant gaps persist between developed economies and developing regions regarding baseline educational access.
* **Data-Driven Policy:** Tracking metrics like literacy rates allows international organizations and educational planners to target funding and literacy initiatives where they are most needed.
* **Interactive Exploration:** Adjusting the sidebar threshold instantly updates the dataset view, demonstrating reactive state management in Streamlit.
""")
