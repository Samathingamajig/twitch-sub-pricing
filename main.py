from bs4 import BeautifulSoup
from dataclasses import dataclass
from pprint import pprint
from pyppeteer import launch
from typing import Dict, Set
import aiohttp
import asyncio
import csv

# None, Stats, or Debug
LOG_LEVELS = {
    "None": 0,
    "Stats": 1,
    "Debug": 2,
}
LOG_LEVEL = LOG_LEVELS["Debug"]


@dataclass
class PreConversionPrice:
    country: str
    local_currency: str
    price_local_cents: int


@dataclass
class Price(PreConversionPrice):
    conversion_factor: float
    price_usd_cents: float
    price_usd: float


def log(msg, level_str, pretty=False):
    if LOG_LEVEL >= LOG_LEVELS[level_str]:
        if pretty:
            pprint(msg)
        else:
            print(msg)


async def get_html(url: str, wait_for_selector: str = None):
    log("Launching browser", "Debug")
    browser = await launch()
    page = await browser.newPage()
    log("Navigating to page", "Debug")
    await page.goto(url)
    if wait_for_selector is not None:
        log("Waiting for selector", "Debug")
        await page.waitForSelector(wait_for_selector)
    log("Getting html", "Debug")
    html = await page.content()
    log("Closing browser", "Debug")
    await browser.close()
    return html


def split_list_by_n(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


async def get_currency_to_usd_factor(all_currencies: Set[str]) -> Dict[str, int]:
    currency_to_usd_factor = {}
    async with aiohttp.ClientSession() as session:
        for c in all_currencies:
            url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{c.lower()}/usd.json"
            async with session.get(url) as resp:
                data = await resp.json()
                currency_to_usd_factor[c] = data["usd"] if "usd" in data else -1
    return currency_to_usd_factor


async def main():
    log("Getting html", "Debug")
    html = await get_html(
        "https://help.twitch.tv/s/article/local-sub-price-countries?language=en_US",
        "#article",
    )

    log("Parsing html", "Debug")
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.select("#article .table")
    all_pre_prices = []
    for t in tables:
        cells = t.select(".cell:not(.title)")
        entries = list(split_list_by_n(cells, 4))
        prices = [
            PreConversionPrice(
                country=e[0].text,
                local_currency=e[1].text,
                price_local_cents=int(float(e[3].text.replace(",", "")) * 100),
            )
            for e in entries
        ]
        all_pre_prices += prices

    all_currencies = set(p.local_currency for p in all_pre_prices)
    log("Getting currency to USD factors", "Debug")
    currency_to_usd_cents = await get_currency_to_usd_factor(all_currencies)
    all_prices = [
        Price(
            country=p.country,
            local_currency=p.local_currency,
            price_local_cents=p.price_local_cents,
            conversion_factor=currency_to_usd_cents[p.local_currency],
            price_usd_cents=p.price_local_cents
            * currency_to_usd_cents[p.local_currency],
            price_usd=round(
                p.price_local_cents * currency_to_usd_cents[p.local_currency] / 100, 2
            ),
        )
        for p in all_pre_prices
    ]
    all_prices.sort(key=lambda p: p.price_usd)

    log("Top 3 cheapest countries", "Stats")
    log(all_prices[:3], "Stats", pretty=True)
    log("", "Stats")

    log("Top 3 most expensive countries", "Stats")
    log(all_prices[-3:], "Stats", pretty=True)

    with open("prices.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            (
                "Country",
                "Local Currency",
                "Price (Local Cents)",
                "Conversion Factor",
                "Price (USD Cents)",
                "Price (USD)",
            )
        )
        writer.writerows(
            (
                p.country,
                p.local_currency,
                p.price_local_cents,
                p.conversion_factor,
                p.price_usd_cents,
                p.price_usd,
            )
            for p in all_prices
        )


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
