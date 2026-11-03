# Stockholm Property Signals

A single-page web app for analysing Stockholm housing prices at neighbourhood (stadsdel) level. It looks for links between price changes and local news, police incidents, planning and infrastructure, and macro factors such as the policy rate and mortgage rates. It then forecasts prices 6–24 months ahead.

Hosted version: https://claude.ai/artifact/P9oxqbjC66vXB5SqyMte3A

## Features
- **Prices:** kr/kvm, an index or 12-month change for 24 Stockholm areas, with an optional policy-rate overlay.
- **News & signals:** Swedish word-list sentiment scoring, optional scoring by Claude, and manual corrections.
- **Correlation:** lagged cross-correlation from −12 to +12 months, pooled across areas and per area. Negative lags show prices moving before the news.
- **Forecast:** a pooled ridge regression on price momentum, rates and lagged news, police and planning signals. Uses 400 Monte Carlo paths with a 10–90% range, and is backtested against a model without news.

## Data inputs
The data is imported as files. The page doesn't fetch any websites itself.

| Data | Source | Format |
|---|---|---|
| Prices | Svensk Mäklarstatistik, or Booli/Hemnet sold listings | CSV: `month,area,price_per_sqm,n_sales`, or individual sales |
| News | Google News RSS per area | RSS XML or CSV: `date,area,headline,source,category,score` |
| Police | `https://polisen.se/api/events` | JSON |
| Macro | Riksbanken, SCB | CSV: `month,policy_rate,mortgage_rate_3m,cpif,unemployment` |

## Run locally
Open `index.html` in a browser. Chart.js and PapaParse load from a CDN. Saving data and scoring with Claude work only in the hosted version on claude.ai.

The built-in demo data is synthetic. Its news effect is deliberately built in to show how the analysis works.
