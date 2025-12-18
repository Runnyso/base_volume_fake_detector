import requests, time

def fake_volume():
    print("Base — Fake Volume Detector (high volume but tiny trades)")
    seen = set()

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/transactions/base?limit=300")
            for pair_addr, group in groupby(sorted(r.json().get("transactions", []), key=lambda x: x["pairAddress"]), key=lambda x: x["pairAddress"]):
                txs = list(group)
                if len(txs) < 50: continue

                vol_usd = sum(t["valueUSD"] for t in txs if t.get("valueUSD"))
                avg_trade = vol_usd / len(txs) if len(txs) > 0 else 0

                if vol_usd > 100_000 and avg_trade < 200:  # $100k+ vol but <$200 avg trade
                    token = txs[0]["token0"]["symbol"] if "WETH" in txs[0]["token1"]["symbol"] else txs[0]["token1"]["symbol"]
                    print(f"FAKE VOLUME EXPOSED\n"
                          f"{token} ${vol_usd:,.0f} volume\n"
                          f"Avg trade: ${avg_trade:.0f} ({len(txs)} trades)\n"
                          f"https://dexscreener.com/base/{pair_addr}\n"
                          f"→ Wash trading or bot spam\n"
                          f"→ Chart looks alive — but it's illusion\n"
                          f"{'FAKE'*30}")

        except:
            pass
        time.sleep(5.6)

from itertools import groupby

if __name__ == "__main__":
    fake_volume()
