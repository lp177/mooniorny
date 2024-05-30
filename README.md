# Mooiorny: market data tracker

This project monitors stock prices in real-time using the [yfinance](https://github.com/ranaroussi/yfinance) library, displaying their historical and current values in an interactive GUI built with [DearPyGui](https://github.com/hoffstadt/DearPyGui).
Users can configure the refresh interval, way to notify on price events, have multiple profils, view price data for multiple stocks with different time periods...
The GUI also highlights price changes with custom colors based on user specified conditions.

This an alpha preview, many features are again in devellopement.

## Summary

- [Installation](#installation)
- [Configuration](#configuration)
- [Notification](#Notification)


## Installation

```bash
pip install requirement.txt
# If you are on Microsoft system install also requirement specific for this OS:
pip install requirement_windows.txt
# And finally launch the app with:
python main.py
```

## Configuration

You can set stock/crypto/currency to track in the default profil (multi profile / ui work in progress) in file at profils/default/stocks.py  
UI settings in file at profils/default/ui.py  
Alerts at profils/default/ui.py