import streamlit as st
import plotly.express as px
import pandas as pd
import requests
import numpy as np
from datetime import datetime
from web3 import Web3

st.set_page_config(page_title="CAKE Analysis", layout="wide", page_icon="pancake")
st.title("PancakeSwap CAKE Analysis – Clone gratuit & illimité")
st.markdown("Clone parfait de https://dune.com/sebabess/cake-analysis · 0 € · refresh toutes les 5 min")

# Extract sheet_id from your Google Sheet URL: https://docs.google.com/spreadsheets/d/SHEET_ID/edit
sheet_id = "1r23_C9_tfjeO-M8dHUn45Avsoq2BE9iBCw3lyU4f5iw"
sheet_name = "Sheet1"  # Replace with your tab name (URL-encoded if spaces, e.g., "My%20Sheet")

# Reliable format (works as of 2025)
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

df = pd.read_csv(url)

print(df.head())
st.caption(str(df.head()))



# ------------------------------------------------------------------
# @st.cache_data(ttl=300)
# def get_cake_data():
#     # CoinGecko live
#     try:
#         # Fetch on-chain token data for CAKE on BSC
#         r = requests.get(
#             "https://api.coingecko.com/api/v3/onchain/networks/bsc/tokens/0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82",
#             timeout=10
#         )
#         js = r.json()
#         total_supply_raw = js["total_supply"]  # Raw integer (e.g., with decimals factored in)
#         decimals = js["decimals"]  # e.g., 18
#         total_supply_readable = total_supply_raw / (10 ** decimals) if decimals else total_supply_raw
#         holders = js.get("holders", "N/A")  # Approximate holder count
#     except:
#         total_supply_readable=0
#     return total_supply_readable

    
#     try:
#         r = requests.get("https://api.coingecko.com/api/v3/coins/pancakeswap-token", timeout=10)
#         js = r.json()["market_data"]
#         price = js["current_price"]["usd"]
#         market_cap = js["market_cap"]["usd"]
#     except:
#         price, market_cap = 2.18, 330_000_000

#     # Dates + simulation ultra-réaliste (compatible pandas 2.3)
#     dates = pd.date_range("2023-01-01", datetime.now(), freq="W")
#     n = len(dates)
#     rng = np.random.default_rng(seed=42)

#     # On convertit explicitement en array numpy pour éviter le bug .clip sur Index
#     days = (dates - dates[0]).days.values  # ← la ligne qui fix tout

#     tvl_base = 1.25e9 - days * 18000
#     tvl_noise = rng.normal(0, 1, n).cumsum() * 8e6
#     tvl = np.clip(tvl_base + tvl_noise, 5e8, None)  # ← np.clip au lieu de .clip

#     volume_base = 2.8e8
#     volume_noise = rng.normal(0, 1, n).cumsum() * 3e7
#     volume = np.clip(volume_base + volume_noise, 5e7, None)

#     price_trend = price * (1 + rng.normal(0, 0.015, n).cumsum() / 400)
#     users = np.clip(85_000 + rng.normal(0, 1500, n).cumsum(), 30_000, None)

#     df = pd.DataFrame({
#         "date": dates,
#         "tvl": tvl,
#         "volume_24h": volume,
#         "price": price_trend,
#         "daily_users": users
#     })

#     return {"price": price, "market_cap": market_cap, "df": df}

# # ------------------------------------------------------------------
# BSC public RPC endpoint (free and reliable)
# bsc_rpc = "https://bsc-dataseed.binance.org"  # Or use: https://bsc-rpc.publicnode.com

# # Connect to BSC
# web3 = Web3(Web3.HTTPProvider(bsc_rpc))

# if not web3.is_connected():
#     raise Exception("Failed to connect to BSC RPC")

# # Minimal ABI for ERC20/BEP20 functions we need (totalSupply, decimals, name, symbol)
# minimal_abi = [
#     {
#         "constant": True,
#         "inputs": [],
#         "name": "totalSupply",
#         "outputs": [{"name": "", "type": "uint256"}],
#         "type": "function"
#     },
#     {
#         "constant": True,
#         "inputs": [],
#         "name": "decimals",
#         "outputs": [{"name": "", "type": "uint8"}],
#         "type": "function"
#     },
#     {
#         "constant": True,
#         "inputs": [],
#         "name": "name",
#         "outputs": [{"name": "", "type": "string"}],
#         "type": "function"
#     },
#     {
#         "constant": True,
#         "inputs": [],
#         "name": "symbol",
#         "outputs": [{"name": "", "type": "string"}],
#         "type": "function"
#     }
# ]

# # Replace with your token contract address
# token_address = "0xe9e7CEA3DedcA5984780Bafc599bd69ADd087D56"  # Example: BUSD on BSC

# # Checksum the address
# token_address = web3.to_checksum_address(token_address)

# # Create contract instance
# contract = web3.eth.contract(address=token_address, abi=minimal_abi)

# # Read totalSupply (raw value in wei-like units)
# raw_supply = contract.functions.totalSupply().call()

# # Get decimals to convert to human-readable
# decimals = contract.functions.decimals().call()

# # Human-readable total supply
# total_supply = raw_supply / (10 ** decimals)

# # Optional: get name and symbol
# name = contract.functions.name().call()
# symbol = contract.functions.symbol().call()

# # print(f"Token: {name} ({symbol})")
# # print(f"Total Supply: {total_supply} {symbol}")
# # print(f"Raw Supply: {raw_supply}")



# # data = get_cake_data()
# st.caption(str(total_supply))
# print(f"Total Supply (readable): {data}")
# df = data["df"]

# # ------------------------------------------------------------------
# # Metrics
# c1, c2, c3, c4 = st.columns(4)
# c1.metric("TVL", f"${df['tvl'].iloc[-1]/1e9:.2f} B")
# c2.metric("Volume 24h", f"${df['volume_24h'].iloc[-1]/1e6:.1f} M")
# c3.metric("Prix CAKE", f"${data['price']:.4f}")
# c4.metric("Daily Users", f"{int(df['daily_users'].iloc[-1]):,}")

# # ------------------------------------------------------------------
# # Charts
# col1, col2 = st.columns(2)
# with col1:
#     fig = px.area(df, x="date", y="tvl", title="TVL PancakeSwap")
#     fig.update_layout(template="plotly_dark")
#     st.plotly_chart(fig, use_container_width=True)

# with col2:
#     fig = px.bar(df.tail(30), x="date", y="volume_24h", title="Volume 24h (30 jours)")
#     fig.update_layout(template="plotly_dark")
#     st.plotly_chart(fig, use_container_width=True)

# col3, col4 = st.columns(2)
# with col3:
#     fig = px.line(df, x="date", y="price", title="Prix CAKE")
#     fig.update_layout(template="plotly_dark")
#     st.plotly_chart(fig, use_container_width=True)

# with col4:
#     fig = px.line(df, x="date", y="daily_users", title="Daily Active Users")
#     fig.update_layout(template="plotly_dark")
#     st.plotly_chart(fig, use_container_width=True)

# # ------------------------------------------------------------------
# st.caption("Données live CoinGecko + simulation réaliste · Refresh auto 5 min · 100 % gratuit")
