"""Checks rules.json before it reaches phones. Run: python3 tools/check.py"""
import datetime
import json
import sys

errors = []


def need(cond, msg):
    if not cond:
        errors.append(msg)


def is_date(value):
    try:
        datetime.date.fromisoformat(value)
        return True
    except (TypeError, ValueError):
        return False


with open("rules.json", encoding="utf-8") as f:
    data = json.load(f)

need(data.get("schemaVersion") == 1, "schemaVersion must be 1")
need(isinstance(data.get("dataVersion"), int), "dataVersion must be a whole number")
need(is_date(data.get("checked")), "checked must be a date like 2026-11-02")

ids = set()
for a in data.get("alerts", []):
    need(a.get("id") and a["id"] not in ids, f"alert id missing or repeated: {a.get('id')}")
    ids.add(a.get("id"))
    need(a.get("title") and a.get("message"), f"alert {a.get('id')} needs title and message")
    for key in ("from", "until"):
        if key in a:
            need(is_date(a[key]), f"alert {a.get('id')}: {key} must be a date")

for c in data["doc"]["conditions"]:
    need(c.get("id") and c.get("group") and c.get("title") and c.get("text"), f"condition incomplete: {c}")

for c in data["doc"].get("otherPermits", []):
    need(c.get("id") and c.get("title") and c.get("text"), f"other permit incomplete: {c}")
need(isinstance(data.get("herdsOfSpecialInterestNote"), str), "herdsOfSpecialInterestNote is missing")
need(isinstance(data.get("firearmsNote"), str), "firearmsNote is missing")

gb = data["gameBirds"]
need(gb.get("status") in ("pending", "published"), "gameBirds.status must be pending or published")
for r in gb["regions"]:
    for s in r.get("seasons", []):
        where = f"{r['id']} {s.get('species')}"
        need(s.get("species"), f"{r['id']}: season needs species")
        need(is_date(s.get("opens")) and is_date(s.get("closes")), f"{where}: opens and closes must be dates")
        if is_date(s.get("opens")) and is_date(s.get("closes")):
            need(s["opens"] <= s["closes"], f"{where}: opens is after closes")
        need(isinstance(s.get("dailyBag"), int) or s.get("dailyBag") is None, f"{where}: dailyBag must be a number")

text = json.dumps(data, ensure_ascii=False)
need("—" not in text, "contains an em dash")

if errors:
    print("rules.json has problems:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("rules.json looks good")
