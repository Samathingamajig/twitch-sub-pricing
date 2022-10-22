# Twitch Sub Pricing

Twitch doesn't charge the same amount of money per sub in each country, but they don't publish them all in the same currency so to determine the cheapest prices, I scraped the data from Twitch and a currency converter "api" to normalize the prices to USD.

It's against the TOS to lie about your location to get cheaper prices, so this is for educational purposes only. If you want to move to any of the cheap countries, that's cool too.

## How to use

1. Clone the repo
2. Run `pip install -r requirements.txt` (wherever your pip is, such as `py -3 -m pip install -r requirements.txt` on Windows)
3. Run `python main.py`

## Results (as of 2022-10-22)

### The 3 Cheapest Countries

| Country | Price (USD) |
| :-----: | :---------: |
| Turkey  |    $0.53    |
| Ukraine |    $0.97    |
|  India  |    $1.33    |

### The 3 Most Expensive Countries

|   Country   | Price (USD) |
| :---------: | :---------: |
| New Zealand |    $4.59    |
|   Kuwait    |    $4.81    |
|  Australia  |    $5.01    |

\* Does not include North American countries

## Implementation Details

- I used [pyppeteer](https://pypi.org/project/pyppeteer/) to scrape the data from Twitch, since it's a single page app and I didn't want to deal with the API (loads the data from a GraphQL API with weird permissions, not server rendered).
- I used [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) to parse the HTML.
- I used asyncio with [aiohttp](https://pypi.org/project/aiohttp/) to make the requests to the currency converter API in parallel (and also asyncio was used for pyppeteer).
- Outputs to a CSV file (`./prices.csv`).
