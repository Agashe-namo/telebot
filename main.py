"""
BingX Spot Trading Notification Bot (Multi-Pair)

Monitors BTC-USDT, ETH-USDT and XRP-USDT.
Sends Telegram alerts with entry price, SMA-10 value,
stop-loss (-3%) and take-profit (+5%).

Add your keys in config.py, install requirements,
then run: python main.py
"""

import asyncio
import logging
import time
import requests
from datetime import datetime
from typing import List, Optional

try:
    from telegram import Bot
except ImportError:
    Bot = None  # allows code to run even before deps installed

from config import (
    BINGX_API_KEY,
    BINGX_API_SECRET,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


class BingXBot:
    BASE = "https://open-api.bingx.com"
    PAIRS = ["BTC-USDT", "ETH-USDT", "XRP-USDT"]

    def __init__(self):
        self.bot = Bot(TELEGRAM_BOT_TOKEN) if Bot else None
        self.hist: dict[str, List[float]] = {p: [] for p in self.PAIRS}
        self.last_signal: dict[str, Optional[str]] = {p: None for p in self.PAIRS}

    @staticmethod
    def _ts() -> int:
        return int(time.time() * 1000)

    def _get(self, ep: str, params=None):
        try:
            r = requests.get(f"{self.BASE}{ep}",
                             params=params or {},
                             headers={"X-BX-APIKEY": BINGX_API_KEY},
                             timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            log.warning("HTTP error: %s", e)
            return None

    def _price(self, symbol: str) -> Optional[float]:
        data = self._get("/openApi/spot/v1/ticker/price",
                         {"symbol": symbol, "timestamp": self._ts()})
        if not data:
            return None

        # Handle several possible response formats
        if isinstance(data, dict):
            if "price" in data:
                return float(data["price"])
            if "data" in data:
                payload = data["data"]
                if isinstance(payload, dict) and "price" in payload:
                    return float(payload["price"])
                if isinstance(payload, list) and payload:
                    first = payload[0]
                    if "price" in first:
                        return float(first["price"])
                    if "trades" in first and first["trades"]:
                        return float(first["trades"][0]["price"])
        if isinstance(data, list) and data and "price" in data[0]:
            return float(data[0]["price"])

        log.warning("Unrecognized price structure: %s", data)
        return None

    @staticmethod
    def _sma(vals: List[float], period=10) -> Optional[float]:
        return sum(vals[-period:]) / period if len(vals) >= period else None

    @staticmethod
    def _stops(px: float, side: str, sl_pct=3, tp_pct=5):
        if side == "BUY":
            return round(px * (1 - sl_pct/100), 4), round(px * (1 + tp_pct/100), 4)
        return round(px * (1 + sl_pct/100), 4), round(px * (1 - tp_pct/100), 4)

    async def _notify(self, msg: str):
        log.info("Notify: %s", msg.replace("\n", " | "))
        if self.bot:
            await self.bot.send_message(TELEGRAM_CHAT_ID, msg, parse_mode="HTML")

    async def run(self, delay=60):
        await self._notify("<b>BingX Multi-Pair Bot Started</b>\nMonitoring: BTC-USDT, ETH-USDT, XRP-USDT")

        while True:
            for pair in self.PAIRS:
                px = self._price(pair)
                if not px:
                    log.warning(f"Failed to get price for {pair}")
                    continue

                h = self.hist[pair]
                h.append(px)
                h[:] = h[-50:]  # Keep last 50 prices only

                sma = self._sma(h)
                if sma is None or len(h) < 11:
                    continue

                prev = h[-2]
                side = None

                # Detect SMA crossover
                if px > sma and prev <= sma:
                    side = "BUY"
                elif px < sma and prev >= sma:
                    side = "SELL"

                # Send notification if signal changed
                if side and side != self.last_signal[pair]:
                    sl, tp = self._stops(px, side)
                    txt = (f"<b>🚨 {side} Signal • {pair}</b>\n"
                           f"📈 Entry: {px:.4f}\n"
                           f"📊 SMA-10: {sma:.4f}\n"
                           f"🛑 Stop Loss: {sl:.4f} ({-3 if side=='BUY' else 3}%)\n"
                           f"🎯 Take Profit: {tp:.4f} ({5 if side=='BUY' else -5}%)\n"
                           f"⏰ {datetime.utcnow():%Y-%m-%d %H:%M:%S} UTC")

                    await self._notify(txt)
                    self.last_signal[pair] = side

            await asyncio.sleep(delay)


if __name__ == "__main__":
    try:
        asyncio.run(BingXBot().run())
    except KeyboardInterrupt:
        log.info("Bot stopped by user")
    except Exception as e:
        log.error(f"Bot error: {e}")
