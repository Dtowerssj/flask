# TradingView to MetaTrader 5 Bot

A Python bot that receives TradingView webhook alerts and turns them into orders on a MetaTrader 5 account, sizing every trade by a configurable percentage of risk.

> This project places real orders. Test it on a demo account first. It is provided as-is, with no warranty and no financial advice.

## Features

- Opens **BUY** and **SELL** market orders with the stop loss and take profit taken from the alert.
- **Risk-based position sizing**: the lot size is calculated from a percentage of the account balance and the distance to the stop loss.
- Closes positions and moves stop losses when the alert says so.
- A small **Tkinter control panel** to enter the account number, server, password and risk percentage, and to start or stop the bot.

## How it works

```
TradingView alert --POST /webhook--> Flask server (main.py) --MetaTrader5 API--> MT5 terminal
                                            ^
Control panel (gui.py) --POST /connect_mt5--+
```

| File | Role |
|---|---|
| `gui.py` | Control panel. Starts the server through `init.py` and sends the account details to `/connect_mt5`. |
| `init.py` | Launches the Flask server (`main.py`) as a background process. |
| `main.py` | Flask app with the `/connect_mt5` and `/webhook` endpoints and the alert parsing. |
| `orders.py` | Lot size calculation and order handling (open, close, modify stop loss) through the `MetaTrader5` package. |

## Alert format

The webhook expects a `POST /webhook` with `Content-Type: text/plain`. The parsing was written for one specific TradingView strategy ("OMERTA"), so the alert text must contain:

| Event | Text the server looks for |
|---|---|
| New trade | A line containing `OMERTA` that ends with the symbol, a line containing `Opportunity` whose second-to-last word is `BUY` or `SELL`, and lines with `TP: <price>` and `SL: <price>` |
| Close position | A message containing `Closed`, plus the `OMERTA` symbol line |
| Move stop loss | A message containing `Stop Loss Modified`, plus the symbol line and a line with `SL` followed by the new price |

## Requirements

- **Windows** with the **MetaTrader 5** terminal installed (the `MetaTrader5` Python package only runs on Windows).
- Python 3.
- A public URL for port 5000 so TradingView can reach the webhook, for example through a tunnel such as ngrok (not included).

## Getting started

```bash
pip install -r requirements.txt
python gui.py
```

Enter the account number, server, password and risk percentage in the panel, then press **Correr Bot** (Run bot). The credentials are typed at run time and are never stored in the repository. The interface text is in Spanish.

## Tech stack

Python, Flask, MetaTrader5 API, Tkinter.
