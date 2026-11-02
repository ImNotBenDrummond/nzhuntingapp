# NZ hunting app data

The NZ hunting app reads `rules.json` from this repository, so rule text, game bird seasons and alerts can change without an App Store update. The app ships with a built-in copy and uses that until it finds a valid newer one here.

This repository holds data only. New screens or features still need an app update and App Review.

## How to make a change

1. Open `rules.json` on github.com and click the pencil icon (**Edit this file**).
2. Make the change.
3. Add 1 to `dataVersion`, and set `checked` to today's date (`yyyy-MM-dd`).
4. Click **Commit changes...**, then **Commit changes**.
5. Click the **Actions** tab. A green tick means the file is fine. A red cross means the app will ignore it: click the run to see what is wrong, then fix it.

Phones pick up the change the next time the app is opened, at most every 6 hours.

## Adding game bird seasons each year

When Fish & Game publishes the new regulations (usually April), for each region add entries to its `seasons` list, set `seasonLabel` to the year, and change `status` from `pending` to `published`. Example:

```json
{ "id": "otago", "name": "Otago", "seasons": [
  { "species": "Mallard and grey duck", "opens": "2027-05-01", "closes": "2027-07-25", "dailyBag": 10, "note": "" }
] }
```

`dailyBag` is a number, or `null` if there is no limit. Copy the numbers from the region's booklet on the Fish & Game regulations page linked in the file.

## Alerts

Add an entry to `alerts` to show a notice on the app's home screen:

```json
{ "id": "2027-tahr-cull", "title": "Tahr control in progress", "message": "DOC is running aerial tahr control in the Rangitata.", "url": "https://www.doc.govt.nz/", "from": "2027-01-10", "until": "2027-02-28" }
```

- `id`: unique. Use a new one for every alert, or people who dismissed an old one will not see it.
- `url`, `from`, `until`: optional. Dates are NZ time.

## Fields

- `schemaVersion`: leave at 1. Only changes when the app is updated to read a new layout.
- `doc.conditions`: the DOC standard permit conditions, in plain English.
- `herdsOfSpecialInterest`: herds designated by the Minister for Hunting and Fishing.
- `gameBirds.regions`: the 12 Fish & Game regions and their seasons.

## Checking locally

```
python3 tools/check.py
```

## Sources

All rule text is a plain-English summary of the official pages linked in `rules.json`. Recheck them before changing anything.
