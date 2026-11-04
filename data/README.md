# Data

All data here comes from free, openly published sources. It was fetched on 2026-11-03.

| File | Source | Contents |
|---|---|---|
| `maklarstatistik_monthly_bostadsratter.csv` | [Svensk Mäklarstatistik](https://www.maklarstatistik.se/omrade/riket/stockholms-lan/stockholm/) | Bostadsrätter, kr/kvm (3-month rolling average, as published) and the number sold per month. Oct 2022 – Sep 2026, for Stockholm city, Centrala Stockholm, 12 districts (stadsdelsområden) and 13 municipalities in Stockholm County. |
| `maklarstatistik_yearly_bostadsratter.csv` | Svensk Mäklarstatistik | Annual average kr/kvm for the same areas: from 1996 for municipalities and from 2005 for Stockholm districts. |
| `polisen_events_stockholms_lan.json` | [Polisen open API](https://polisen.se/api/events) | 1,177 police events in Stockholm County, 3 May – 3 Nov 2026. About 734 of them can be matched to one of the 25 areas. |
| `google_news_stockholm.csv` | [Google News RSS](https://news.google.com) | 31,869 headlines, Oct 2021 – Nov 2026. Made from one search per area per month that combines the area's main neighbourhood names (1,550 searches, 46,961 raw results). Kept only where the headline names a place in the area or the source is a hyperlocal outlet (Mitt i, Bättre stadsdel and similar). Sports listings and foreign sources were dropped. `place_in_headline` marks the stricter subset. |
| `riksbank_policy_rate.csv` | [Sveriges Riksbank API](https://api.riksbank.se/swea/v1/Observations/SECBREPOEFF/2015-01-01/2026-11-03) | Policy rate (styrränta), last value of each month, 2015 onwards. |

All of this data is also built into `index.html`, and the app loads it by default. The aggregates "Stockholm" and "Centrala Stockholm" are left out of the analysis so that areas aren't double-counted.

## Neighbourhood profiles
| File | Source | Contents |
|---|---|---|
| `area_profiles_stats.json` | Computed | Per-area figures shown in the app. |
| `scb_area_stats_raw.json` | [SCB PxWeb API v2](https://api.scb.se/ov0104/v2beta/api/v2/) | Raw figures from SCB tables TAB6574 (age, 2025 and 2015), TAB6568 (households), TAB6065 (house type), TAB6253 (tenure), TAB6540 (building age), TAB6534 (education) and TAB5750 (median disposable income for ages 20–64, 2023). |
| `regso_to_district_map.json` | Own mapping | Which of Stockholm's 127 RegSO small areas belong to each Mäklarstatistik district. Based on parish (församling) boundaries, the same grouping Stockholm's polling districts use. |
| `election_2026_riksdag_by_area.json` | [Valmyndigheten](https://resultat.val.se/val2026) | Final Riksdag 2026 results with 2022 votes. Stockholm polling districts are grouped by parish prefix; 6 collection districts (uppsamlingsdistrikt) can't be placed and are left out. Municipalities use their full totals. |
| `area_profiles_text.json` | Written by Claude | Overview text per area (character, who it suits, local scene, what's changing), based on the figures above and general knowledge. Not official descriptions. |

## Map, commute and schools
| File | Source | Contents |
|---|---|---|
| `map_geo.json` | SCB RegSO 2025 boundaries (geodata.scb.se WFS), grouped into districts; municipality borders from [okfse/sweden-geojson](https://github.com/okfse/sweden-geojson) | Simplified outlines of the 25 areas and their neighbours, with label points. |
| `commute_to_tcentralen.json` | Points: OpenStreetMap Nominatim. Car: [OSRM](https://router.project-osrm.org). Bike: [routing.openstreetmap.de](https://routing.openstreetmap.de). Public transport: [SL Journey Planner v2](https://www.trafiklab.se) (no API key needed) | From each area's main centre to T-Centralen: straight-line km; car minutes and road km (no traffic); bike minutes and km; fastest SL trip arriving by 08:00 on Tue 10 Nov 2026, with route and number of changes. |
| `schools_by_area.json` | [Skolverket planned-educations API v3](https://api.skolverket.se/planned-educations/v3/api-docs): compact school units + SALSA | Per area: number of compulsory schools; for schools with year 9, the average merit value, share eligible for upper secondary, SALSA deviation (result vs expected given pupil background), and the top 3 schools. Schools were placed by coordinates using RegSO and municipality boundaries. |

Not yet included: counts of restaurants, bars and playgrounds from OpenStreetMap (Overpass was unreachable from the browser used); Brå crime statistics; housing-association (BRF) finances.

## Taxes and fees

- `taxes_2026.json` — per area: municipal and region income tax, burial fee, total excluding church fee, church fee by parish (Svenska kyrkan members only), and the 2025 municipal + region total for comparison. Source: Skatteverket's open dataset "Skattesatser per församling" (2026), cross-checked against SCB's municipal tax table. Stockholm city's 12 districts share one rate; the parishes give the church fee range.
- National rules shown in the app (property fee caps, lagfart, pantbrev, capital gains, interest deduction) come from Skatteverket and Lantmäteriet and are the same in every area.

## Monthly costs, house prices and BRF check

- `villa_prices_scb.json` — SCB table TAB1169: number of sold houses (permanent living, excluding ground lease) and average purchase price per municipality, 2015 and 2020–2025. Stockholm city's 12 districts share the city figure.
- Monthly cost model: loan = price × (1 − down payment, min 10%); amortisation 2% above 70% loan-to-value, 1% at 50–70% (Lag 2026:226, from 1 April 2026); interest deduction 30% up to 100 000 kr interest a year and 21% above; BRF fee default 830 kr/m²/year (Stockholm average); house running costs default 3 750 kr/month plus the capped property fee. Default rate 2.70% (median average 3-month rate, big banks, September 2026).
- BRF health check thresholds (rules of thumb): debt < 5 000 kr/m² good, > 10 000 high; savings ≥ 150 kr/m² good, < 75 thin; fee 700–900 kr/m² normal; rate sensitivity < 5% good, > 10% high; energy < 100 kr/m² good, > 150 high.

## Map

- `map_basemap.json` — the vector basemap and area shapes used by the map tab, in projected integer units (1 unit = 0.0001° latitude; x scaled by cos 59.3°). Water, parks/forest, motorways/trunk/primary roads, rail and place names come from OpenStreetMap via OpenFreeMap vector tiles (zoom 12, OpenMapTiles schema). Municipal shapes are rebuilt from OpenStreetMap admin_level 7 boundaries; Stockholm's 12 districts are SCB RegSO small areas fitted to the OSM city boundary. Everything is clipped to land so borders follow the shoreline.
- `build_map.py` — the script that produced it (shapely). Map data © OpenStreetMap contributors (ODbL).

## Explore neighbourhood (`explore/`)
One file per area (`explore/<slug>.json`, 25 files, ~4.6 MB in total). The page loads a file only when that area is opened.
- `pois`: `[category, x, y, name, OSM subclass]`, in the same projected units as the basemap. The category codes are c cafés & bakeries, g grocery, r restaurants & bars, p parks, y playgrounds, s schools, k preschools, f sports & swimming, h health & pharmacy, l library & culture, t stations.
- `s` / `n`: SVG paths for secondary/tertiary and minor streets, clipped to the area.
- Source: OpenFreeMap vector tiles (OpenMapTiles schema, © OpenStreetMap contributors). POIs come from the z14 `poi` layer and streets from `transportation`, assigned to areas with the land-clipped polygons in `map_basemap.json`. Built by `build_explore.py`. Per-area counts and km² are embedded in the page as `XIDX`.
- Coverage follows OSM. Schools, preschools, parks, playgrounds and stations are well mapped; small shops and cafés are less complete.

## Refreshing the data
Mäklarstatistik updates around the 8th of each month. Open their Stockholm page in a browser, paste `fetch_maklarstatistik.js` into the developer console and press Enter. The script downloads fresh CSV files, which you then drop into the app.

## Refreshing police events
The police API only keeps about 6 months of events. Run `fetch_polisen.js` in the console on polisen.se/api/events every month or two, then drop the file into the app. Duplicates are removed automatically.

## News scoring
The app scores headlines with a Swedish word list (−1…1). It catches clear cases well, such as shootings, explosions and closures (negative) and openings, renovations and new parks (positive). About two-thirds of headlines score neutral. The app's "Score with Claude" button gives more accurate scores in batches.

## Limits
- Free monthly data only goes back 48 months. Older history is annual only.
- The data covers bostadsrätter only. Villa (house) prices are also on Mäklarstatistik, but aren't fetched here.
- Police events are the incidents the police choose to publish, not complete crime statistics. Brå (statistik.bra.se) publishes reported crimes per municipality with longer history.
- Events from Stockholm city are matched to districts using place names in the summary. About 1 in 6 name no recognisable place and stay unassigned.
- SCB's open database only has annual figures at county level, so it isn't used.
- Check Svensk Mäklarstatistik's terms before using the data commercially or republishing it.
