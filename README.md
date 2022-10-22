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
