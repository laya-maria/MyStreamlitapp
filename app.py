import pandas as pd
import plotly.express as px
import streamlit as st

# Configure page layout
st.set_page_config(
    page_title="Global Literacy & Socioeconomic Dashboard",
    page_icon="🌍",
    layout="wide",
)

# --- 1. DATA LOADING & CACHING ---
@st.cache_data
def load_data():
    # Publicly accessible clean dataset combining country metrics and literacy rates
    url = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Literacy%20rates%20-%20CIA%20World%20Factbook/Literacy%20rates%20-%20CIA%20World%20Factbook.csv"
    df = pd.read_csv(url)
    # Clean column names for easier handling
    df.columns = [col.strip() for col in df.columns]
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# --- 2. SIDEBAR CONFIGURATION (INTERACTIVE WIDGETS) ---
st.sidebar.header("🎛️ Dashboard Controls")

st.sidebar.markdown("""
Use the controls below to filter countries and customize the visualization parameters.
""")

# Widget 1: Slider for minimum literacy rate threshold
min_literacy = st.sidebar.slider(
    "Minimum Literacy Rate (%)",
    min_value=0.0,
    max_value=100.0,
    value=50.0,
    step=5.0
)

# Filter dataframe based on slider
filtered_df = df[df[df.columns[1]] >= min_literacy].dropna(subset=[df.columns[1]])

# Widget 2: Checkbox to show raw data table
show_raw_data = st.sidebar.checkbox("Show Raw Data Table", value=False)


# --- 3. MAIN APP LAYOUT & SECTIONS ---

# Section 1: Overview
st.title("🌍 Global Literacy & Socioeconomic Insights")
st.markdown("""
Welcome to the **Global Literacy Dashboard**. This interactive web application investigates global literacy rates across different countries and regions. 
Use this platform to examine disparities, analyze distributions, and uncover developmental trends worldwide.
""")

st.divider()

# Section 2: Data Display & Metrics
st.header("📊 Dataset Overview & Summary Metrics")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Countries Analyzed", value=len(df))
with col2:
    avg_literacy = df[df.columns[1]].mean()
    st.metric(label="Average Global Literacy Rate", value=f"{avg_literacy:.1f}%")
with col3:
    st.metric(label="Countries Meeting Filter", value=len(filtered_df))

if show_raw_data:
    st.subheader("Raw Dataset Preview")
    st.dataframe(filtered_df, use_container_width=True)

st.divider()

# Section 3: Interactive Visualizations (Plotly)
st.header("📈 Interactive Data Visualizations")

st.markdown("""
The chart below illustrates the distribution of literacy rates across countries. You can hover over individual data points or bars to inspect specific national statistics.
""")

# Plotly Visualization: Bar/Scatter chart
fig = px.bar(
    filtered_df.sort_values(by=filtered_df.columns[1], ascending=False).head(30),
    x=filtered_df.columns[0],
    y=filtered_df.columns[1],
    title=f"Top 30 Countries by Literacy Rate (Min: {min_literacy}%)",
    labels={filtered_df.columns[0]: "Country", filtered_df.columns[1]: "Literacy Rate (%)"},
    color=filtered_df.columns[1],
    color_continuousscale="Viridis"
)

fig.update_layout(
    xaxis_tickangle=-45,
    template="plotly_white",
    height=550
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Section 4: Key Insights & Takeaways
st.header("💡 Key Insights")
st.markdown("""
* **Regional Disparities:** Significant gaps persist between developed economies and developing regions regarding baseline educational access.
* **Data-Driven Policy:** Tracking metrics like literacy rates allows international organizations and educational planners to target funding and literacy initiatives where they are most needed.
* **Interactive Exploration:** Adjusting the sidebar threshold instantly updates the dataset view, demonstrating reactive state management in Streamlit.
""")
