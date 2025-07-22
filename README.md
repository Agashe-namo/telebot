# BingX Multi-Pair Spot Trading Notification Bot

A Python bot that monitors BTC-USDT, ETH-USDT, and XRP-USDT on BingX exchange and sends Telegram notifications when SMA-10 crossover signals occur.

## Features

- 📊 **Multi-pair monitoring**: BTC-USDT, ETH-USDT, XRP-USDT
- 🎯 **SMA-10 crossover strategy**: Detects when price crosses above/below 10-period moving average
- 📱 **Telegram notifications**: Real-time alerts with entry price, stop loss, and take profit
- 🔒 **Read-only**: Bot only monitors and notifies - you place trades manually
- ⚡ **Real-time**: Checks prices every 60 seconds
- 🛡️ **Risk management**: Automatic stop loss (3%) and take profit (5%) calculations

## Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Edit `config.py` and add your credentials:

**BingX API Keys:**
1. Log into BingX
2. Go to Account Settings → API Management
3. Create new API key with "Read" permissions
4. Copy API Key and Secret to config.py

**Telegram Bot:**
1. Message @BotFather on Telegram
2. Create new bot with `/newbot` command
3. Copy the bot token to config.py
4. Message @userinfobot to get your chat ID
5. Add chat ID to config.py

### 3. Run the Bot
```bash
python main.py
```

## Sample Notification

```
🚨 BUY Signal • BTC-USDT
📈 Entry: 67,485.2340
📊 SMA-10: 67,200.1580
🛑 Stop Loss: 65,460.6770 (-3%)
🎯 Take Profit: 70,859.4957 (5%)
⏰ 2025-07-22 18:30:45 UTC
```

## Customization

### Change Monitored Pairs
Edit `PAIRS` list in `main.py`:
```python
PAIRS = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "ADA-USDT"]
```

### Adjust Risk Management
Modify stop loss/take profit percentages in `_stops()` method:
```python
@staticmethod
def _stops(px: float, side: str, sl_pct=3, tp_pct=5):  # Change these values
```

### Change SMA Period
Modify the SMA period in `_sma()` calls:
```python
sma = self._sma(h, period=20)  # Change from 10 to 20
```

### Adjust Check Frequency
Change the delay parameter in main execution:
```python
asyncio.run(BingXBot().run(delay=30))  # Check every 30 seconds instead of 60
```

## Free Hosting Options

Deploy your bot on these free platforms:

- **Replit**: Free tier with 24/7 hosting
- **Railway**: Free tier with good uptime
- **Render**: Free web services
- **PythonAnywhere**: Free tier for simple bots
- **Heroku**: Free dyno hours (limited)

## Security Notes

- ⚠️ Never share your API keys
- ✅ Use read-only API permissions
- ✅ Keep config.py private (added to .gitignore)
- ✅ Bot cannot place trades - notifications only

## Troubleshooting

**"Unexpected price structure" error:**
- BingX API format may have changed
- Check logs for the actual response structure

**No notifications:**
- Verify Telegram bot token and chat ID
- Check if SMA crossover conditions are met
- Ensure API keys have proper permissions

**Connection errors:**
- Check internet connection
- Verify BingX API endpoints are accessible

## Strategy Details

The bot uses a **Simple Moving Average (SMA-10) Crossover Strategy**:

- **BUY Signal**: Price crosses from below to above the SMA-10
- **SELL Signal**: Price crosses from above to below the SMA-10
- **Stop Loss**: 3% away from entry price
- **Take Profit**: 5% away from entry price

This is a trend-following strategy best suited for:
- 1-hour to 4-hour timeframes
- Trending markets
- Medium-term position holding

## Support

For issues or questions:
1. Check the logs for error messages
2. Verify all configuration settings
3. Test with a single pair first
4. Ensure all dependencies are installed

---

**Disclaimer**: This bot is for educational purposes. Cryptocurrency trading involves risk. Always do your own research and trade responsibly.
