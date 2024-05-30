# Mooniorny: market data tracker

## Summary

- [Screenshoots](#screenshoots)
- [Presentation](#presentation)
- [Installation](#installation)
- [Configuration](#configuration)


<div align="center"><img src="https://github.com/lp177/mooniorny/blob/master/images/mooniorny.png?raw=true" alt="Logo"></div><br>

## Presentation

This project monitors stock prices in real-time using the [yfinance](https://github.com/ranaroussi/yfinance) library, displaying their historical and current values in an interactive GUI built with [DearPyGui](https://github.com/hoffstadt/DearPyGui).
Users can configure the refresh interval, way to notify on price events, have multiple profils, view price data for multiple stocks with different time periods...  
The GUI also highlights price changes with custom colors based on user specified conditions.

This an alpha preview, many features are again in devellopement.

## Screenshoots

<img src="https://github.com/lp177/mooniorny/blob/master/images/screenshoots/default_dash.png">  
<img src="https://github.com/lp177/mooniorny/blob/master/images/screenshoots/settings.png">

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