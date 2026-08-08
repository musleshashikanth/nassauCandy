import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import os
import random

st.set_page_config(page_title="Nassau Candy Logistics Dashboard", layout="wide", page_icon="🍬")

# Premium UI CSS
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #fafafa;
    }
    h1, h2, h3 {
        color: #ff4b4b;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .stPlotlyChart {
        background: transparent;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    if os.path.exists("nassau_candy_sales.csv"):
        df = pd.read_csv("nassau_candy_sales.csv")
    else:
        # Generate on the fly if missing
        np.random.seed(42)
        random.seed(42)
        factories = {
            "Lot's O' Nuts": {"lat": 32.881893, "lon": -111.768036},
            "Wicked Choccy's": {"lat": 32.076176, "lon": -81.088371},
            "Sugar Shack": {"lat": 48.11914, "lon": -96.18115},
            "Secret Factory": {"lat": 41.446333, "lon": -90.565487},
            "The Other Factory": {"lat": 35.1175, "lon": -89.971107}
        }
        products = [
            {"Division": "Chocolate", "Product Name": "Wonka Bar - Nutty Crunch Surprise", "Factory": "Lot's O' Nuts", "Base Cost": 1.5, "Base Price": 3.0},
            {"Division": "Chocolate", "Product Name": "Wonka Bar - Milk Chocolate", "Factory": "Wicked Choccy's", "Base Cost": 1.2, "Base Price": 2.5},
            {"Division": "Sugar", "Product Name": "Laffy Taffy", "Factory": "Sugar Shack", "Base Cost": 0.5, "Base Price": 1.5},
            {"Division": "Sugar", "Product Name": "Everlasting Gobstopper", "Factory": "Secret Factory", "Base Cost": 1.0, "Base Price": 2.5},
            {"Division": "Sugar", "Product Name": "Hair Toffee", "Factory": "The Other Factory", "Base Cost": 0.9, "Base Price": 2.2},
        ]
        regions = {
            "West": ["CA", "WA", "OR", "NV", "AZ"],
            "Midwest": ["IL", "OH", "MI", "IN", "WI"],
            "South": ["TX", "FL", "GA", "NC", "VA"],
            "Northeast": ["NY", "PA", "MA", "NJ", "CT"]
        }
        states_cities = {
            "CA": ["Los Angeles"], "WA": ["Seattle"], "OR": ["Portland"], "NV": ["Las Vegas"], "AZ": ["Phoenix"],
            "IL": ["Chicago"], "OH": ["Columbus"], "MI": ["Detroit"], "IN": ["Indianapolis"], "WI": ["Milwaukee"],
            "TX": ["Houston"], "FL": ["Miami"], "GA": ["Atlanta"], "NC": ["Charlotte"], "VA": ["Richmond"],
            "NY": ["New York"], "PA": ["Philadelphia"], "MA": ["Boston"], "NJ": ["Newark"], "CT": ["Hartford"]
        }
        ship_modes = ["Standard", "Expedited"]
        data = []
        start_date = datetime(2023, 1, 1)
        for i in range(5000):
            order_date = start_date + timedelta(days=random.randint(0, 365))
            prod = random.choice(products)
            region = random.choice(list(regions.keys()))
            state = random.choice(regions[region])
            ship_mode = random.choices(ship_modes, weights=[0.7, 0.3])[0]
            
            base_lead = 3 if ship_mode == "Standard" else 1
            if state in ["CA", "NY"]: base_lead += random.randint(1, 4)
            if prod["Factory"] == "Sugar Shack" and region == "South": base_lead += random.randint(2, 5)
                
            lead_time = base_lead + random.randint(0, 3)
            ship_date = order_date + timedelta(days=lead_time)
            
            units = random.randint(10, 500)
            cost = round(prod["Base Cost"] * units, 2)
            sales = round(prod["Base Price"] * units * random.uniform(0.9, 1.1), 2)
            
            data.append({
                "Order Date": order_date.strftime("%Y-%m-%d"),
                "Ship Date": ship_date.strftime("%Y-%m-%d"),
                "Ship Mode": ship_mode,
                "State/Province": state,
                "Region": region,
                "Factory": prod["Factory"],
                "Shipping Lead Time": lead_time,
                "Route": f"{prod['Factory']} \u2192 {state}",
                "Sales": sales,
                "Units": units,
                "Gross Profit": sales - cost
            })
        df = pd.DataFrame(data)
        df.to_csv("nassau_candy_sales.csv", index=False)
        
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    if 'Shipping Lead Time' not in df.columns:
        df['Shipping Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    if 'Route' not in df.columns:
        df['Route'] = df['Factory'] + ' \u2192 ' + df['State/Province']
    return df

st.title("🍬 Nassau Candy Distributor: Logistics Intelligence")
st.markdown("Analyze factory-to-customer shipping route efficiency to optimize deliveries.")

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
selected_region = st.sidebar.multiselect("Select Customer Region", df['Region'].unique(), default=df['Region'].unique())
selected_mode = st.sidebar.multiselect("Select Ship Mode", df['Ship Mode'].unique(), default=df['Ship Mode'].unique())
lead_time_threshold = st.sidebar.slider("Lead Time Threshold (Days)", min_value=0, max_value=20, value=5)

filtered_df = df[(df['Region'].isin(selected_region)) & (df['Ship Mode'].isin(selected_mode))]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"<div class='metric-card'><h3>Avg Lead Time</h3><h2>{filtered_df['Shipping Lead Time'].mean():.2f} days</h2></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-card'><h3>Total Shipments</h3><h2>{len(filtered_df):,}</h2></div>", unsafe_allow_html=True)
delay_pct = (len(filtered_df[filtered_df['Shipping Lead Time'] > lead_time_threshold]) / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
col3.markdown(f"<div class='metric-card'><h3>Delay Frequency</h3><h2>{delay_pct:.1f}%</h2></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='metric-card'><h3>Unique Routes</h3><h2>{filtered_df['Route'].nunique()}</h2></div>", unsafe_allow_html=True)

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Route Efficiency", "Geographic Bottlenecks", "Ship Mode Analysis"])

with tab1:
    st.header("Route Performance Leaderboard")
    route_stats = filtered_df.groupby('Route').agg(
        Avg_Lead_Time=('Shipping Lead Time', 'mean'),
        Total_Shipments=('Shipping Lead Time', 'count')
    ).reset_index()
    
    col_top, col_bottom = st.columns(2)
    with col_top:
        st.subheader("Top 10 Most Efficient Routes")
        st.dataframe(route_stats.sort_values('Avg_Lead_Time').head(10), use_container_width=True)
    with col_bottom:
        st.subheader("Bottom 10 Least Efficient Routes")
        st.dataframe(route_stats.sort_values('Avg_Lead_Time', ascending=False).head(10), use_container_width=True)

with tab2:
    st.header("Geographic Shipping Heatmap")
    state_stats = filtered_df.groupby('State/Province').agg(Avg_Lead_Time=('Shipping Lead Time', 'mean')).reset_index()
    fig = px.choropleth(state_stats, locations='State/Province', locationmode="USA-states", color='Avg_Lead_Time',
                        scope="usa", color_continuous_scale="Reds", title="Average Lead Time by State")
    fig.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'), paper_bgcolor='rgba(0,0,0,0)', font_color='white')
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Lead Time by Shipping Method")
    fig2 = px.box(filtered_df, x="Ship Mode", y="Shipping Lead Time", color="Ship Mode",
                  title="Distribution of Shipping Lead Times by Mode", template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)
