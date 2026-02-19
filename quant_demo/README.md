Quant demo (CCXT) — testnet-friendly

This demo is a minimal CCXT-based scaffold to experiment with a grid strategy on testnet/sandbox. It does NOT run live trades by default; create a .env file with TESTNET_API_KEY and TESTNET_SECRET if you want to connect to a testnet exchange that supports CCXT.

Files:
- demo_grid.py — small script demonstrating: fetch_ticker, fetch_order_book, compute spread, simulate a simple grid on recent price, and (optionally) place limit orders (commented out).
- requirements.txt — ccxt

How to run (recommended, testnet only):
1) Create a virtualenv: python3 -m venv .venv && source .venv/bin/activate
2) pip install -r requirements.txt
3) If you have testnet API keys, place them in environment variables: TESTNET_API_KEY, TESTNET_SECRET
4) Run: python3 demo_grid.py --symbol BTC/USDT --steps 5 --step-size 50 --amount 0.001

Notes:
- This script is educational. Read the code before using any live API keys.
- Edit exchange selection in demo_grid.py to point to an exchange that supports testnet via CCXT and set exchange-specific flags (see comments).
