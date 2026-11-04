# Stockholm Property Guide

A single-page web app that helps people buying a home in Stockholm choose where to live. It matches areas to a buyer's budget, household and commute, shows what each neighbourhood is like and what is nearby, and works out monthly costs and taxes. Underneath it still tracks prices against news, police incidents, planning and interest rates, with a 6–24 month price forecast.

Hosted version: https://claude.ai/artifact/P9oxqbjC66vXB5SqyMte3A

## Features
- **Prices:** kr/kvm, an index or 12-month change for 24 Stockholm areas, with an optional policy-rate overlay.
- **News & signals:** Swedish word-list sentiment scoring, optional scoring by Claude, and manual corrections.
- **Correlation:** lagged cross-correlation from −12 to +12 months, pooled across areas and per area. Negative lags show prices moving before the news.
- **Forecast:** a pooled ridge regression on price momentum, rates and lagged news, police and planning signals. Uses 400 Monte Carlo paths with a 10–90% range, and is backtested against a model without news.

- **Map & commute:** a map of all 25 areas, coloured by price, travel time, income, families, schools or largest party. Shows distance and travel time to T-Centralen by public transport, car and bike.
- **Where should I live?:** an English matcher. Enter budget, size, household, home type, commute mode and priorities, and get the areas ranked with reasons for each.
- **Neighbourhoods:** two sub-sections.
  - *Area guide:* detailed profiles with official statistics, the 2026 election and a written overview.
  - *Explore neighbourhood:* a street-level map of one area with ~18,000 OpenStreetMap places: cafés, grocery stores, restaurants, parks, playgrounds, schools, preschools, sports and swimming, health, culture and stations. Categories can be toggled, markers cluster when zoomed out, and each category is compared per 1,000 residents with the average of the 25 areas.
- **Languages:** English, Swedish, French and German.

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

The app loads real data by default: Svensk Mäklarstatistik prices for 25 Stockholm districts and municipalities, plus the Riksbank policy rate. See [`data/`](data/README.md) for sources and how to refresh them. Synthetic demo data is still available under Data & sources, with a deliberately built-in news effect for trying out the analysis.

## Languages

The app is available in English, Swedish, French and German (switcher top right; the choice is remembered, and `?lang=sv|fr|de` works in the URL). Translations live in `i18n/*.json`, keyed by the English text with numbers, area names and transit lines replaced by placeholders (`{n0}`, `{a0}`, `{r0}`). News headlines, police reports and place names are deliberately left untranslated.
