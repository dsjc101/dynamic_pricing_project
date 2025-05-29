import streamlit as st
import pandas as pd
import numpy as np

# Load final price recommendation
recommendation_df = pd.read_csv(r"C:\Users\divya\OneDrive\Desktop\dynamic_pricing_project\data\final_price_recommendations.csv")

# Load price simulation per product
simulation_df = pd.read_csv("C:\\Users\\divya\\OneDrive\\Desktop\\dynamic_pricing_project\\data\\price_simulation_results.csv")

st.set_page_config(page_title="Dynamic Pricing Simulator", layout="wide")
st.title("💰 Dynamic Pricing Engine — Revenue Simulator")

# Sidebar: Select StockCode
stockcode_list = recommendation_df['StockCode'].unique()
selected_code = st.sidebar.selectbox("Select a Product (StockCode)", stockcode_list)

# Current product info
product = recommendation_df[recommendation_df['StockCode'] == selected_code].iloc[0]
sim_data = simulation_df[simulation_df['StockCode'] == selected_code].sort_values("SimulatedPrice")

st.subheader(f"Product: {selected_code}")

# Show current vs optimal price and metrics
col1, col2, col3 = st.columns(3)
col1.metric("Current Price", f"${product['CurrentPrice']:.2f}")
col2.metric("Optimal Price", f"${product['OptimalPrice']:.2f}", delta=f"{product['PriceChange(%)']:.2f}%")
col3.metric("Elasticity", f"{product['Elasticity']:.2f}")

st.markdown("---")

# Interactive slider to simulate new price
st.subheader("📈 Simulate Revenue from Different Prices")

# Define buffer zone (±30%)
buffer = 0.3
current_price = float(product['CurrentPrice'])
optimal_price = float(product['OptimalPrice'])

# Compute min and max across current and optimal price buffers
min_range = min(current_price * (1 - buffer), optimal_price * (1 - buffer))
max_range = max(current_price * (1 + buffer), optimal_price * (1 + buffer))

# Load simulation data for selected StockCode
sim_data = simulation_df[simulation_df['StockCode'] == selected_code]

# Constrain to available simulated price range
min_price = min(min_range, sim_data["SimulatedPrice"].min())
max_price = min(max_range, sim_data["SimulatedPrice"].max())

# Create a sorted list of only the simulated prices (discrete slider values)

available_prices = sorted(sim_data['SimulatedPrice'].unique())
available_prices = [round(p, 2) for p in available_prices]
closest_default = min(available_prices, key=lambda x: abs(x - optimal_price))
price_slider = st.select_slider(
    "Set a new price:",
    options=available_prices,
    value=closest_default
)


# Lookup simulated quantity/revenue for selected price
closest_row = sim_data.iloc[(sim_data['SimulatedPrice'] - price_slider).abs().argsort().iloc[0]]

# Show simulation results
estimated_quantity = closest_row['SimulatedQuantity']
estimated_revenue = closest_row['SimulatedRevenue']
revenue_gain = estimated_revenue - product['CurrentRevenue']
revenue_gain_pct = (revenue_gain / product['CurrentRevenue']) * 100

col4, col5, col6 = st.columns(3)
col4.metric("Estimated Quantity", f"{estimated_quantity:,.0f}")
col5.metric("Estimated Revenue", f"${estimated_revenue:,.2f}")
col6.metric("Revenue Gain", f"${revenue_gain:,.2f}", delta=f"{revenue_gain_pct:.2f}%")

# Optional: Full row
with st.expander("🔍 View Full Data Row"):
    st.write(product)

st.markdown("---")
st.caption("Simulation based on actual price–demand forecasts, not just elasticity.")
