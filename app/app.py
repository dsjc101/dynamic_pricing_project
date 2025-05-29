import streamlit as st
import pandas as pd
import os

file_path = os.path.join('path', 'to', 'your', 'C:\\Users\\divya\\OneDrive\\Desktop\\dynamic_pricing_project\\data\\final_price_recommendations.csv')
df = pd.read_csv(file_path)


st.set_page_config(page_title="Dynamic Pricing Simulator", layout="wide")
st.title(" Dynamic Pricing Engine — Revenue Simulator")

# Sidebar: Select StockCode
stockcode_list = df['StockCode'].unique()
selected_code = st.sidebar.selectbox("Select a Product (StockCode)", stockcode_list)

# Filter data for selected product
product = df[df['StockCode'] == selected_code].iloc[0]

st.subheader(f"Product: {selected_code}")

# Show current vs optimal price and metrics
col1, col2, col3 = st.columns(3)
col1.metric("Current Price", f"${product['CurrentPrice']:.2f}")
col2.metric("Optimal Price", f"${product['OptimalPrice']:.2f}", delta=f"{product['PriceChange(%)']:.2f}%")
col3.metric("Elasticity", f"{product['Elasticity']:.2f}")

st.markdown("---")

# Interactive slider to simulate new price
st.subheader("Simulate New Price & Revenue Impact")
price_slider = st.slider(
    "Set a new price:",
    min_value=float(product['CurrentPrice']) * 0.7,
    max_value=float(product['CurrentPrice']) * 1.3,
    value=float(product['OptimalPrice']),
    step=0.01
)

# Elasticity-based estimation
current_price = product['CurrentPrice']
current_quantity = product['CurrentQuantity']
elasticity = product['Elasticity']

price_change_pct = (price_slider - current_price) / current_price
estimated_quantity = current_quantity * (1 + elasticity * price_change_pct)
estimated_revenue = estimated_quantity * price_slider
revenue_gain = estimated_revenue - product['CurrentRevenue']
revenue_gain_pct = (revenue_gain / product['CurrentRevenue']) * 100

# Show simulation results
col4, col5, col6 = st.columns(3)
col4.metric("Estimated Quantity", f"{estimated_quantity:,.0f}")
col5.metric("Estimated Revenue", f"${estimated_revenue:,.2f}")
col6.metric("Revenue Gain", f"${revenue_gain:,.2f}", delta=f"{revenue_gain_pct:.2f}%")

# Show full row for debugging or inspection
with st.expander("🔍 View Full Data Row"):
    st.write(product)

st.markdown("---")
st.caption("Simulation based on elasticity formula: Q_new = Q_current × (1 + E × ΔP/P)")
