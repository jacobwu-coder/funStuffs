#!/usr/bin/env python3
"""Minimal CCXT grid-demo (testnet-friendly)

Usage:
  python3 demo_grid.py --symbol BTC/USDT --steps 5 --step-size 50 --amount 0.001

Notes:
- Default exchange: a placeholder 'mexc' example. Many exchanges support testnets differently; read the comments and adjust.
- The script by default only simulates grid placements and prints what it would do. To enable live testnet orders, set LIVE=1 and provide TESTNET_API_KEY/TESTNET_SECRET env vars.
- NEVER run with live keys until you understand the code.
"""
import os
import argparse
import ccxt
import time
from dotenv import load_dotenv

load_dotenv()

LIVE = os.getenv('LIVE', '0') == '1'
API_KEY = os.getenv('TESTNET_API_KEY')
API_SECRET = os.getenv('TESTNET_SECRET')

def make_exchange():
    # Example: MEXC (spot) - CCXT may require special flags for testnet/sandbox. Replace with your exchange of choice.
    exchange_id = 'mexc'  # change if you want another exchange
    exchange_class = getattr(ccxt, exchange_id)
    params = {}
    # Example for exchanges requiring sandbox=True in params:
    # params = { 'enableRateLimit': True, 'options': { 'defaultType': 'spot' }, 'urls': { 'api': { 'public': 'https://www.mexc.com/open/api/v2' } } }
    if LIVE and API_KEY and API_SECRET:
        ex = exchange_class({ 'apiKey': API_KEY, 'secret': API_SECRET, 'enableRateLimit': True })
    else:
        # unauthenticated instance for market data only
        ex = exchange_class({ 'enableRateLimit': True })
    return ex


def fetch_market(exchange, symbol):
    ticker = exchange.fetch_ticker(symbol)
    book = exchange.fetch_order_book(symbol)
    mid_price = (ticker['bid'] + ticker['ask']) / 2 if ticker.get('bid') and ticker.get('ask') else ticker['last']
    spread = (book['asks'][0][0] - book['bids'][0][0]) if book['asks'] and book['bids'] else None
    return { 'ticker': ticker, 'book': book, 'mid': mid_price, 'spread': spread }


def simulate_grid(mid, steps, step_size, amount):
    # Build symmetric grid around mid price
    buys = [mid - (i+1)*step_size for i in range(steps)]
    sells = [mid + (i+1)*step_size for i in range(steps)]
    grid = []
    for price in buys:
        grid.append({'side':'buy','price':price,'amount':amount})
    for price in sells:
        grid.append({'side':'sell','price':price,'amount':amount})
    grid_sorted = sorted(grid, key=lambda x: x['price'])
    return grid_sorted


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--symbol', default='BTC/USDT')
    p.add_argument('--steps', type=int, default=5)
    p.add_argument('--step-size', type=float, default=50.0)
    p.add_argument('--amount', type=float, default=0.001)
    args = p.parse_args()

    ex = make_exchange()
    print('Exchange:', ex.id)
    print('LIVE mode:', LIVE)

    market = fetch_market(ex, args.symbol)
    print('Mid price:', market['mid'])
    print('Spread:', market['spread'])

    grid = simulate_grid(market['mid'], args.steps, args.step_size, args.amount)
    print('\nSimulated grid orders:')
    for o in grid:
        print(f"{o['side'].upper():4} price={o['price']:.2f} amt={o['amount']}")

    # Example: show what we would submit (live disabled by default)
    if LIVE and API_KEY and API_SECRET:
        print('\nPlacing testnet orders (LIVE mode)')
        for o in grid:
            try:
                if o['side']=='buy':
                    # uncomment to actually create limit buy orders
                    # order = ex.create_limit_buy_order(args.symbol, o['amount'], o['price'])
                    print('Would place BUY', o)
                else:
                    # order = ex.create_limit_sell_order(args.symbol, o['amount'], o['price'])
                    print('Would place SELL', o)
                time.sleep(0.2)
            except Exception as e:
                print('Order failed:', e)
    else:
        print('\nLIVE mode disabled. To enable, set environment LIVE=1 and provide TESTNET_API_KEY and TESTNET_SECRET.')

if __name__ == '__main__':
    main()
