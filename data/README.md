# Data

All data here comes from free, openly published sources. It was fetched on 2026-11-03.

| File | Source | Contents |
|---|---|---|
| `maklarstatistik_monthly_bostadsratter.csv` | [Svensk Mäklarstatistik](https://www.maklarstatistik.se/omrade/riket/stockholms-lan/stockholm/) | Bostadsrätter, kr/kvm (3-month rolling average, as published) and the number sold per month. Oct 2022 – Sep 2026, for Stockholm city, Centrala Stockholm, 12 districts (stadsdelsområden) and 13 municipalities in Stockholm County. |
| `maklarstatistik_yearly_bostadsratter.csv` | Svensk Mäklarstatistik | Annual average kr/kvm for the same areas: from 1996 for municipalities and from 2005 for Stockholm districts. |
| `polisen_events_stockholms_lan.json` | [Polisen open API](https://polisen.se/api/events) | 1,177 police events in Stockholm County, 3 May – 3 Nov 2026. About 734 of them can be matched to one of the 25 areas. |
| `riksbank_policy_rate.csv` | [Sveriges Riksbank API](https://api.riksbank.se/swea/v1/Observations/SECBREPOEFF/2015-01-01/2026-11-03) | Policy rate (styrränta), last value of each month, 2015 onwards. |

All of this data is also built into `index.html`, and the app loads it by default. The aggregates "Stockholm" and "Centrala Stockholm" are left out of the analysis so that areas aren't double-counted.

## Refreshing the data
Mäklarstatistik updates around the 8th of each month. Open their Stockholm page in a browser, paste `fetch_maklarstatistik.js` into the developer console and press Enter. The script downloads fresh CSV files, which you then drop into the app.

## Refreshing police events
The police API only keeps about 6 months of events. Run `fetch_polisen.js` in the console on polisen.se/api/events every month or two, then drop the file into the app. Duplicates are removed automatically.

## Limits
- Free monthly data only goes back 48 months. Older history is annual only.
- The data covers bostadsrätter only. Villa (house) prices are also on Mäklarstatistik, but aren't fetched here.
- Police events are the incidents the police choose to publish, not complete crime statistics. Brå (statistik.bra.se) publishes reported crimes per municipality with longer history.
- Events from Stockholm city are matched to districts using place names in the summary. About 1 in 6 name no recognisable place and stay unassigned.
- SCB's open database only has annual figures at county level, so it isn't used.
- Check Svensk Mäklarstatistik's terms before using the data commercially or republishing it.
