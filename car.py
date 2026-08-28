#!/usr/bin/env python3
"""Everything Car — record and manage fuel, servicing, costs and reminders.

Records live in data/*.csv so they stay readable and diffable in git.

    ./car.py fuel    --date 2026-08-24 --odo 84120 --litres 46.2 --cost 82.15
    ./car.py service --date 2026-08-24 --odo 84120 --type "Minor service" --cost 320
    ./car.py cost    --date 2026-08-24 --category rego --amount 890
    ./car.py remind  --item "Registration" --due-date 2027-03-31
    ./car.py report
    ./car.py due
"""

import argparse
import csv
import datetime as dt
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")

FUEL = os.path.join(DATA, "fuel.csv")
SERVICE = os.path.join(DATA, "service.csv")
COSTS = os.path.join(DATA, "costs.csv")
REMINDERS = os.path.join(DATA, "reminders.csv")
ODOMETER = os.path.join(DATA, "odometer.csv")
QUOTES = os.path.join(DATA, "insurance_quotes.csv")
PRICES = os.path.join(DATA, "fuel_prices.csv")
TYRES = os.path.join(DATA, "tyres.csv")

CURRENCY = "$"

FIELDS = {
    FUEL: ["date", "odometer_km", "litres", "total_cost", "price_per_litre",
           "station", "fuel_type", "full_tank", "notes"],
    SERVICE: ["date", "odometer_km", "type", "description", "workshop", "cost",
              "parts", "next_due_date", "next_due_km", "notes"],
    COSTS: ["date", "category", "description", "amount", "odometer_km", "notes"],
    REMINDERS: ["item", "due_date", "due_km", "recurrence", "notes"],
    ODOMETER: ["date", "odometer_km", "notes"],
    QUOTES: ["brand", "underwriter", "date_quoted", "cover_type", "value_basis",
             "sum_insured", "annual_premium", "monthly_premium", "basic_excess",
             "extra_excess", "windscreen_excess", "choice_of_repairer", "hire_car",
             "roadside", "rating_one_protection", "notes"],
    PRICES: ["date", "station", "suburb", "brand", "fuel_type", "price_cents",
             "source", "notes"],
    TYRES: ["date", "odometer_km", "pressure_fl", "pressure_fr", "pressure_rl",
            "pressure_rr", "pressure_spare", "tread_fl", "tread_fr", "tread_rl",
            "tread_rr", "rotated", "notes"],
}

# Cost categories that are also captured in their own ledger, so the
# report does not count them twice.
LEDGER_CATEGORIES = {"fuel", "service"}


# ---------------------------------------------------------------- storage

def read(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="") as fh:
        return [row for row in csv.DictReader(fh) if any(v.strip() for v in row.values() if v)]


def append(path, row):
    exists = os.path.exists(path)
    with open(path, "a", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS[path])
        if not exists or os.path.getsize(path) == 0:
            writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in FIELDS[path]})


def rewrite(path, rows):
    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS[path])
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in FIELDS[path]})


def sort_by_date(path):
    rows = read(path)
    rows.sort(key=lambda r: (r.get("date") or "9999-99-99", num(r.get("odometer_km")) or 0))
    rewrite(path, rows)


# ---------------------------------------------------------------- helpers

def num(value):
    try:
        return float(str(value).replace(",", "").replace("$", "").strip())
    except (TypeError, ValueError):
        return None


def today():
    return dt.date.today().isoformat()


def parse_date(value):
    try:
        return dt.date.fromisoformat((value or "").strip())
    except ValueError:
        return None


def money(value):
    return f"{CURRENCY}{value:,.2f}"


def truthy(value):
    return str(value).strip().lower() in {"y", "yes", "true", "1"}


# ---------------------------------------------------------------- commands

def cmd_fuel(args):
    litres, cost = args.litres, args.cost
    ppl = args.price
    if ppl and litres and not cost:
        cost = round(ppl / 100 * litres, 2) if ppl > 20 else round(ppl * litres, 2)
    if litres and cost and not ppl:
        ppl = round(cost / litres, 3)
    append(FUEL, {
        "date": args.date, "odometer_km": args.odo, "litres": litres,
        "total_cost": cost, "price_per_litre": ppl, "station": args.station or "",
        "fuel_type": args.fuel_type or "", "full_tank": "no" if args.partial else "yes",
        "notes": args.notes or "",
    })
    sort_by_date(FUEL)
    print(f"Logged fill-up: {args.date}  {litres} L  {money(cost)} @ {args.odo} km")


def cmd_service(args):
    append(SERVICE, {
        "date": args.date, "odometer_km": args.odo, "type": args.type,
        "description": args.description or "", "workshop": args.workshop or "",
        "cost": args.cost, "parts": args.parts or "",
        "next_due_date": args.next_due_date or "", "next_due_km": args.next_due_km or "",
        "notes": args.notes or "",
    })
    sort_by_date(SERVICE)
    print(f"Logged service: {args.type} on {args.date} @ {args.odo} km")
    if args.next_due_date or args.next_due_km:
        append(REMINDERS, {
            "item": f"Next service (after {args.type})",
            "due_date": args.next_due_date or "", "due_km": args.next_due_km or "",
            "recurrence": "", "notes": f"set from service on {args.date}",
        })
        print("  → reminder added for the next service")


def cmd_cost(args):
    append(COSTS, {
        "date": args.date, "category": args.category,
        "description": args.description or "", "amount": args.amount,
        "odometer_km": args.odo or "", "notes": args.notes or "",
    })
    sort_by_date(COSTS)
    print(f"Logged cost: {args.category} {money(args.amount)} on {args.date}")


def to_cents(value):
    """Accept 179.9 or 1.799 and normalise to cents per litre."""
    v = num(value)
    if v is None:
        return None
    return round(v * 100, 1) if v < 20 else round(v, 1)


LEGAL_TREAD_MM = 1.5
PROFILE = os.path.join(ROOT, "vehicle.md")
CORNERS = [("fl", "Front left"), ("fr", "Front right"),
           ("rl", "Rear left"), ("rr", "Rear right")]


def placard_pressure():
    """The cold pressure recorded on the profile's tyre row, in psi."""
    if not os.path.exists(PROFILE):
        return None
    for raw in open(PROFILE):
        if "Pressure (front / rear" not in raw:
            continue
        value = raw.split("|")[2] if raw.count("|") >= 3 else ""
        match = re.search(r"(\d+(?:\.\d+)?)\s*psi", value)
        if match:
            return float(match.group(1))
    return None


def cmd_tyres(args):
    """Log a pressure/tread check and flag anything out of spec."""
    row = {"date": args.date, "odometer_km": args.odo or "",
           "pressure_spare": args.spare or "", "rotated": "yes" if args.rotated else "",
           "notes": args.notes or ""}
    for key, _ in CORNERS:
        row[f"pressure_{key}"] = getattr(args, key) or ""
        row[f"tread_{key}"] = getattr(args, f"tread_{key}") or ""
    append(TYRES, row)
    sort_by_date(TYRES)
    print(f"Tyre check logged for {args.date}")

    target = args.target or placard_pressure()
    if target:
        if not args.target:
            print(f"  Checked against the {target:.0f} psi placard figure in vehicle.md")
        for key, label in CORNERS:
            psi = num(getattr(args, key))
            if psi is None:
                continue
            delta = psi - target
            if abs(delta) >= 3:
                verb = "under" if delta < 0 else "over"
                print(f"  {label}: {psi:.0f} psi is {abs(delta):.0f} psi {verb} "
                      f"the {target:.0f} psi target")
    else:
        print("  No target pressure available, so pressures were not checked.")
        print("  Record the placard figure in vehicle.md, or pass --target.")

    for key, label in CORNERS:
        tread = num(getattr(args, f"tread_{key}"))
        if tread is None:
            continue
        if tread <= LEGAL_TREAD_MM:
            print(f"  {label}: {tread:.1f} mm tread is at or under the "
                  f"{LEGAL_TREAD_MM} mm legal minimum — replace before driving far")
        elif tread < 3.0:
            print(f"  {label}: {tread:.1f} mm tread — wet grip falls off below 3 mm, "
                  f"start budgeting")


def cmd_price(args):
    cents = to_cents(args.price)
    append(PRICES, {
        "date": args.date, "station": args.station, "suburb": args.suburb or "",
        "brand": args.brand or "", "fuel_type": args.fuel_type or "91",
        "price_cents": cents, "source": args.source or "observed",
        "notes": args.notes or "",
    })
    sort_by_date(PRICES)
    day = parse_date(args.date)
    when = day.strftime("%a") if day else args.date
    print(f"Price recorded: {args.station} {cents:.1f}c/L on {args.date} ({when})")


def cmd_quote(args):
    append(QUOTES, {
        "brand": args.brand, "underwriter": args.underwriter or "",
        "date_quoted": args.date, "cover_type": args.cover or "comprehensive",
        "value_basis": args.value_basis or "", "sum_insured": args.sum_insured or "",
        "annual_premium": args.annual or "", "monthly_premium": args.monthly or "",
        "basic_excess": args.excess or "", "extra_excess": args.extra_excess or "",
        "windscreen_excess": args.windscreen or "",
        "choice_of_repairer": args.repairer or "", "hire_car": args.hire_car or "",
        "roadside": args.roadside or "", "rating_one_protection": args.rating_one or "",
        "notes": args.notes or "",
    })
    print(f"Quote recorded: {args.brand}")


def cmd_odo(args):
    append(ODOMETER, {"date": args.date, "odometer_km": args.odo, "notes": args.notes or ""})
    sort_by_date(ODOMETER)
    print(f"Odometer reading: {args.odo:,.0f} km on {args.date}")


def cmd_remind(args):
    append(REMINDERS, {
        "item": args.item, "due_date": args.due_date or "", "due_km": args.due_km or "",
        "recurrence": args.recurrence or "", "notes": args.notes or "",
    })
    print(f"Reminder added: {args.item}")


# ---------------------------------------------------------------- analysis

def fuel_stats(rows):
    """Full-to-full economy. Litres between two full tanks / distance covered."""
    rows = [r for r in rows if num(r.get("odometer_km")) and num(r.get("litres"))]
    rows.sort(key=lambda r: num(r["odometer_km"]))
    legs, pending, last_full = [], 0.0, None
    for row in rows:
        pending += num(row["litres"])
        if truthy(row.get("full_tank")):
            odo = num(row["odometer_km"])
            if last_full is not None and odo > last_full:
                legs.append({"distance": odo - last_full, "litres": pending,
                             "date": row.get("date", ""), "odometer": odo})
            last_full = odo
            pending = 0.0
    return legs


def summarise(as_of=None):
    fuel, service = read(FUEL), read(SERVICE)
    costs, reminders = read(COSTS), read(REMINDERS)
    readings = read(ODOMETER)
    odos = [num(r.get("odometer_km")) for r in fuel + service + costs + readings]
    odos = [o for o in odos if o]
    latest_odo = max(odos) if odos else None
    span_km = (max(odos) - min(odos)) if len(odos) > 1 else 0

    fuel_spend = sum(num(r.get("total_cost")) or 0 for r in fuel)
    litres = sum(num(r.get("litres")) or 0 for r in fuel)
    service_spend = sum(num(r.get("cost")) or 0 for r in service)
    other = [r for r in costs if (r.get("category") or "").strip().lower() not in LEDGER_CATEGORIES]
    other_spend = sum(num(r.get("amount")) or 0 for r in other)

    legs = fuel_stats(fuel)
    tracked_km = sum(l["distance"] for l in legs)
    tracked_l = sum(l["litres"] for l in legs)

    return {
        "fuel": fuel, "service": service, "costs": costs, "reminders": reminders,
        "readings": readings,
        "latest_odo": latest_odo, "span_km": span_km,
        "fuel_spend": fuel_spend, "litres": litres,
        "service_spend": service_spend, "other": other, "other_spend": other_spend,
        "total": fuel_spend + service_spend + other_spend,
        "legs": legs, "tracked_km": tracked_km, "tracked_l": tracked_l,
        "as_of": as_of or dt.date.today(),
    }


def due_items(reminders, latest_odo, as_of, horizon_days=60, horizon_km=1500):
    out = []
    for row in reminders:
        due_date, due_km = parse_date(row.get("due_date")), num(row.get("due_km"))
        days = (due_date - as_of).days if due_date else None
        km = (due_km - latest_odo) if (due_km and latest_odo) else None
        flagged = (days is not None and days <= horizon_days) or (km is not None and km <= horizon_km)
        if flagged:
            out.append({"item": row.get("item", ""), "days": days, "km": km,
                        "due_date": row.get("due_date", ""), "due_km": row.get("due_km", ""),
                        "notes": row.get("notes", "")})
    out.sort(key=lambda r: (r["days"] if r["days"] is not None else 10**6,
                            r["km"] if r["km"] is not None else 10**6))
    return out


def line(char="-", width=62):
    return char * width


DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def price_observations(fuel_type=None):
    """Every price point we have: standalone observations plus actual fill-ups."""
    points = []
    for row in read(PRICES):
        day = parse_date(row.get("date"))
        cents = to_cents(row.get("price_cents"))
        if day and cents:
            points.append({"date": day, "cents": cents, "station": row.get("station", ""),
                           "suburb": row.get("suburb", ""), "type": row.get("fuel_type", ""),
                           "source": "observed"})
    for row in read(FUEL):
        day = parse_date(row.get("date"))
        cents = to_cents(row.get("price_per_litre"))
        if day and cents:
            points.append({"date": day, "cents": cents, "station": row.get("station", ""),
                           "suburb": "", "type": row.get("fuel_type", ""), "source": "fill-up"})
    if fuel_type:
        points = [p for p in points if str(p["type"]).strip() == str(fuel_type)]
    points.sort(key=lambda p: p["date"])
    return points


def mean(values):
    return sum(values) / len(values) if values else None


def cmd_cycle(args):
    points = price_observations(args.fuel_type)
    if not points:
        print("No prices recorded yet.\n\n"
              "  ./car.py price --station \"Coles Express Aspley\" --price 179.9\n\n"
              "Log a price whenever you drive past one. Ten or so readings and this\n"
              "starts telling you something; a month of them tells you a lot.")
        return

    print()
    print(line("=", 70))
    print(f"  FUEL PRICES — {len(points)} readings, "
          f"{points[0]['date']} to {points[-1]['date']}")
    print(line("=", 70))

    # By weekday — the Monday-versus-Thursday question.
    by_day = {d: [] for d in DAYS}
    for p in points:
        by_day[DAYS[p["date"].weekday()]].append(p["cents"])
    print()
    print("  BY DAY OF WEEK")
    print(line("-", 70))
    averages = {d: mean(v) for d, v in by_day.items() if v}
    if averages:
        lo, hi = min(averages.values()), max(averages.values())
        for day in DAYS:
            vals = by_day[day]
            if not vals:
                print(f"  {day}    {'no readings':>28}")
                continue
            avg = mean(vals)
            span = (hi - lo) or 1
            bar = "#" * int(round((avg - lo) / span * 34)) or "|"
            flag = "  <- cheapest" if avg == lo else ("  <- dearest" if avg == hi else "")
            print(f"  {day}  {avg:6.1f}c  n={len(vals):<3} {bar}{flag}")
        print()
        print(f"  Spread between best and worst day: {hi - lo:.1f}c/L")
        tank = args.tank
        print(f"  On a {tank:.0f} L fill that is {money((hi - lo) * tank / 100)} a tank.")
        thin = [d for d, v in by_day.items() if 0 < len(v) < 3]
        if thin or len(points) < 14:
            print()
            print("  Careful: this is a small sample. Day-of-week differences need a few")
            print("  weeks of readings before they mean anything — a price cycle moving")
            print("  underneath will otherwise look like a weekday effect.")

    # The cycle itself matters more than the weekday.
    print()
    print("  RECENT TREND")
    print(line("-", 70))
    recent = points[-args.recent:]
    lo_p = min(recent, key=lambda p: p["cents"])
    hi_p = max(recent, key=lambda p: p["cents"])
    for p in recent[-12:]:
        mark = " lowest" if p is lo_p else (" highest" if p is hi_p else "")
        label = (p["station"] or p["suburb"] or p["source"])[:24]
        print(f"  {p['date']}  {DAYS[p['date'].weekday()]}  {p['cents']:6.1f}c  "
              f"{label:<24}{mark}")
    print()
    print(f"  Range over last {len(recent)} readings: {lo_p['cents']:.1f}c "
          f"({lo_p['date']}) to {hi_p['cents']:.1f}c ({hi_p['date']}) "
          f"— {hi_p['cents'] - lo_p['cents']:.1f}c")
    latest = points[-1]
    position = (latest["cents"] - lo_p["cents"]) / ((hi_p["cents"] - lo_p["cents"]) or 1)
    verdict = ("near the bottom — fill now" if position < 0.25 else
               "near the top — buy only what you need" if position > 0.75 else
               "mid-cycle")
    print(f"  Latest reading {latest['cents']:.1f}c sits {position*100:.0f}% up that "
          f"range: {verdict}.")

    # Which station is actually cheapest.
    by_station = {}
    for p in points:
        if p["station"]:
            by_station.setdefault(p["station"], []).append(p["cents"])
    if len(by_station) > 1:
        print()
        print("  BY STATION")
        print(line("-", 70))
        ranked = sorted(((s, mean(v), len(v)) for s, v in by_station.items()),
                        key=lambda r: r[1])
        for station, avg, n in ranked:
            print(f"  {station[:38]:<38} {avg:6.1f}c   n={n}")
        best, worst = ranked[0], ranked[-1]
        gap = worst[1] - best[1]
        print()
        print(f"  {best[0]} averages {gap:.1f}c less than {worst[0]}"
              f" — {money(gap * args.tank / 100)} a tank.")
        print("  Only meaningful if you priced them on the same days.")
    print()


def cmd_compare(args):
    """Compare recorded quotes on cost, not just headline premium."""
    rows = read(QUOTES)
    if not rows:
        print("No quotes recorded yet. Add them with:  ./car.py quote --brand ... --annual ...")
        return

    scored = []
    for row in rows:
        annual = num(row.get("annual_premium"))
        monthly = num(row.get("monthly_premium"))
        if not annual and monthly:
            annual = monthly * 12
        if not annual:
            continue
        basic = num(row.get("basic_excess")) or 0
        extra = num(row.get("extra_excess")) or 0
        insured = num(row.get("sum_insured"))
        scored.append({
            "brand": row.get("brand", ""),
            "underwriter": row.get("underwriter", ""),
            "basis": (row.get("value_basis") or "").lower(),
            "insured": insured,
            "annual": annual,
            "monthly_total": monthly * 12 if monthly else None,
            "excess": basic + extra,
            "one_claim": annual + basic + extra,
            "rate": (annual / insured * 100) if insured else None,
            "row": row,
        })
    if not scored:
        print("Quotes are recorded but none have a premium — add --annual or --monthly.")
        return

    scored.sort(key=lambda q: q["one_claim"])
    cheapest_premium = min(q["annual"] for q in scored)

    print()
    print(line("=", 78))
    print("  INSURANCE QUOTES — ranked by cost of a year with one at-fault claim")
    print(line("=", 78))
    print(f"  {'Brand':<20} {'Basis':<9} {'Insured':>10} {'Premium':>10} {'Excess':>9} {'1 claim':>10}")
    print(line("-", 78))
    for q in scored:
        insured = f"{CURRENCY}{q['insured']:,.0f}" if q["insured"] else "—"
        print(f"  {q['brand'][:20]:<20} {q['basis'][:9]:<9} {insured:>10} "
              f"{money(q['annual']):>10} {money(q['excess']):>9} {money(q['one_claim']):>10}")
    print(line("-", 78))

    best = scored[0]
    print(f"  Lowest cost if you claim once: {best['brand']} at {money(best['one_claim'])}")
    by_premium = min(scored, key=lambda q: q["annual"])
    if by_premium["brand"] != best["brand"]:
        print(f"  Note: {by_premium['brand']} has the cheaper premium "
              f"({money(by_premium['annual'])}) but a {money(by_premium['excess'])} excess, "
              f"so one claim costs {money(by_premium['one_claim'] - best['one_claim'])} more.")
    spread = max(q["annual"] for q in scored) - cheapest_premium
    print(f"  Premium spread across {len(scored)} quotes: {money(spread)}")

    # Paying monthly is a loan; show what it costs.
    surcharges = [(q["brand"], q["monthly_total"] - q["annual"])
                  for q in scored if q["monthly_total"] and q["monthly_total"] > q["annual"] + 1]
    if surcharges:
        print()
        print("  Cost of paying monthly instead of annually:")
        for brand, extra in sorted(surcharges, key=lambda s: -s[1]):
            print(f"    {brand:<20} +{money(extra)} per year")

    # Same underwriter means the same claims process behind different names.
    groups = {}
    for q in scored:
        if q["underwriter"]:
            groups.setdefault(q["underwriter"].strip().title(), []).append(q["brand"])
    shared = {k: v for k, v in groups.items() if len(v) > 1}
    if shared:
        print()
        print("  Same underwriter behind different brands:")
        for uw, brands in shared.items():
            print(f"    {uw}: {', '.join(brands)}")

    print()
    print("  Features")
    print(line("-", 78))
    width = max(10, min(13, (78 - 24) // max(1, len(scored))))
    header = "".join(f"{q['brand'][:width-1]:<{width}}" for q in scored)
    print(f"  {'':<22}{header}")
    feats = [("choice_of_repairer", "Choice of repairer"), ("hire_car", "Hire car"),
             ("roadside", "Roadside"), ("rating_one_protection", "Rating 1 protection"),
             ("windscreen_excess", "Windscreen excess")]
    for key, label in feats:
        cells = "".join(f"{((q['row'].get(key) or chr(8212)).strip())[:width-1]:<{width}}"
                        for q in scored)
        print(f"  {label:<22}{cells}")
    print()
    print("  Excess figures are what you pay per claim. Confirm any age, inexperienced-")
    print("  driver or unlisted-driver excess applies on top before you rely on these.")
    print()


def cmd_report(args):
    s = summarise()
    print()
    print(line("="))
    print("  EVERYTHING CAR — summary")
    print(line("="))

    if s["latest_odo"]:
        print(f"  Latest odometer   {s['latest_odo']:,.0f} km")
    print(f"  Records           {len(s['fuel'])} fill-ups · {len(s['service'])} services · "
          f"{len(s['costs'])} other costs")

    print()
    print("  FUEL & ECONOMY")
    print(line())
    if s["fuel"]:
        prices = [num(r.get("price_per_litre")) for r in s["fuel"]]
        prices = [p for p in prices if p]
        print(f"  Fill-ups          {len(s['fuel'])}   ·   {s['litres']:,.1f} L   ·   {money(s['fuel_spend'])}")
        if prices:
            print(f"  Price per litre   avg {CURRENCY}{sum(prices)/len(prices):.3f}   "
                  f"(low {CURRENCY}{min(prices):.3f} / high {CURRENCY}{max(prices):.3f})")
        if s["legs"]:
            l100 = s["tracked_l"] / s["tracked_km"] * 100
            print(f"  Economy           {l100:.2f} L/100km   ·   {235.215/l100:.1f} mpg (US)   "
                  f"·   {282.481/l100:.1f} mpg (imp)")
            print(f"  Measured over     {s['tracked_km']:,.0f} km across {len(s['legs'])} full-to-full tanks")
            cost_km = s["fuel_spend"] / s["tracked_km"]
            print(f"  Fuel cost         {CURRENCY}{cost_km:.3f}/km   ·   {money(cost_km*100)} per 100 km")
            best = min(s["legs"], key=lambda l: l["litres"] / l["distance"])
            worst = max(s["legs"], key=lambda l: l["litres"] / l["distance"])
            print(f"  Best tank         {best['litres']/best['distance']*100:.2f} L/100km ({best['date']})")
            print(f"  Worst tank        {worst['litres']/worst['distance']*100:.2f} L/100km ({worst['date']})")
        else:
            print("  Economy           needs two full-tank fill-ups with odometer readings")
    else:
        print("  No fill-ups logged yet.")

    print()
    print("  SERVICE & MAINTENANCE")
    print(line())
    if s["service"]:
        for row in s["service"][-6:]:
            cost = num(row.get("cost"))
            odo = num(row.get("odometer_km"))
            print(f"  {row.get('date',''):<12} {(row.get('type') or '')[:26]:<26} "
                  f"{(f'{odo:,.0f} km' if odo else ''):>11}  {money(cost) if cost else '':>10}")
        print(f"  {'':<12} {'total':<26} {'':>11}  {money(s['service_spend']):>10}")
    else:
        print("  No services logged yet.")

    print()
    print("  COST OF OWNERSHIP")
    print(line())
    buckets = {"Fuel": s["fuel_spend"], "Service": s["service_spend"]}
    for row in s["other"]:
        key = (row.get("category") or "other").strip().title()
        buckets[key] = buckets.get(key, 0) + (num(row.get("amount")) or 0)
    for key, value in sorted(buckets.items(), key=lambda kv: -kv[1]):
        if value:
            share = value / s["total"] * 100 if s["total"] else 0
            bar = "#" * int(round(share / 4))
            print(f"  {key:<16} {money(value):>12}  {share:5.1f}%  {bar}")
    print(f"  {'TOTAL':<16} {money(s['total']):>12}")
    if s["span_km"] and s["total"]:
        per_km = s["total"] / s["span_km"]
        print(f"  {'Per km':<16} {CURRENCY + format(per_km, '.3f'):>12}"
              f"  over {s['span_km']:,.0f} km recorded")

    print()
    print("  COMING UP")
    print(line())
    due = due_items(s["reminders"], s["latest_odo"], s["as_of"])
    if due:
        for row in due:
            when = []
            if row["days"] is not None:
                when.append(f"{row['due_date']} ({row['days']:+d} days)")
            if row["km"] is not None:
                when.append(f"{row['due_km']} km ({row['km']:+,.0f} km)")
            flag = "OVERDUE" if (row["days"] is not None and row["days"] < 0) or \
                                (row["km"] is not None and row["km"] < 0) else "due"
            print(f"  [{flag:^7}] {row['item'][:28]:<28} {' · '.join(when)}")
    elif s["reminders"]:
        print("  Nothing due in the next 60 days or 1,500 km.")
    else:
        print("  No reminders set.")
    print()


def cmd_due(args):
    s = summarise()
    due = due_items(s["reminders"], s["latest_odo"], s["as_of"],
                    horizon_days=args.days, horizon_km=args.km)
    if not due:
        print(f"Nothing due within {args.days} days or {args.km:,} km.")
        return
    for row in due:
        parts = [p for p in (row["due_date"], f"{row['due_km']} km" if row["due_km"] else "") if p]
        print(f"{row['item']:<34} {' · '.join(parts)}")


def cmd_log(args):
    """Show the raw ledger for one module."""
    path = {"fuel": FUEL, "service": SERVICE, "cost": COSTS,
            "reminders": REMINDERS, "odo": ODOMETER, "quotes": QUOTES, "prices": PRICES, "tyres": TYRES}[args.module]
    rows = read(path)
    if not rows:
        print(f"No {args.module} records yet.")
        return
    for row in rows[-args.limit:]:
        print(" | ".join(f"{k}={v}" for k, v in row.items() if v))


# ---------------------------------------------------------------- cli

def build_parser():
    p = argparse.ArgumentParser(prog="car.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command", required=True)

    f = sub.add_parser("fuel", help="log a fill-up")
    f.add_argument("--date", default=today())
    f.add_argument("--odo", type=float, required=True, help="odometer in km")
    f.add_argument("--litres", type=float, required=True)
    f.add_argument("--cost", type=float, help="total paid")
    f.add_argument("--price", type=float, help="price per litre (or cents/L)")
    f.add_argument("--station")
    f.add_argument("--fuel-type", dest="fuel_type", help="e.g. 91, 95, 98, diesel")
    f.add_argument("--partial", action="store_true", help="not a full tank")
    f.add_argument("--notes")
    f.set_defaults(func=cmd_fuel)

    s = sub.add_parser("service", help="log a service or repair")
    s.add_argument("--date", default=today())
    s.add_argument("--odo", type=float, required=True)
    s.add_argument("--type", required=True, help="e.g. Minor service, Brake pads")
    s.add_argument("--description")
    s.add_argument("--workshop")
    s.add_argument("--cost", type=float, default=0)
    s.add_argument("--parts")
    s.add_argument("--next-due-date", dest="next_due_date")
    s.add_argument("--next-due-km", dest="next_due_km")
    s.add_argument("--notes")
    s.set_defaults(func=cmd_service)

    c = sub.add_parser("cost", help="log any other cost")
    c.add_argument("--date", default=today())
    c.add_argument("--category", required=True,
                   help="rego, insurance, tyres, repair, finance, tolls, parking, cleaning, accessories")
    c.add_argument("--amount", type=float, required=True)
    c.add_argument("--description")
    c.add_argument("--odo", type=float)
    c.add_argument("--notes")
    c.set_defaults(func=cmd_cost)

    r = sub.add_parser("remind", help="add a reminder")
    r.add_argument("--item", required=True)
    r.add_argument("--due-date", dest="due_date")
    r.add_argument("--due-km", dest="due_km")
    r.add_argument("--recurrence", help="e.g. yearly, 10000km, 6 months")
    r.add_argument("--notes")
    r.set_defaults(func=cmd_remind)

    t = sub.add_parser("tyres", help="log a pressure and tread check")
    t.add_argument("--date", default=today())
    t.add_argument("--odo", type=float)
    t.add_argument("--target", type=float,
                   help="placard pressure in psi (defaults to vehicle.md)")
    for key, label in CORNERS:
        t.add_argument(f"--{key}", type=float, help=f"{label.lower()} pressure, psi")
        t.add_argument(f"--tread-{key}", dest=f"tread_{key}", type=float,
                       help=f"{label.lower()} tread depth, mm")
    t.add_argument("--spare", type=float, help="spare pressure, psi")
    t.add_argument("--rotated", action="store_true", help="tyres were rotated")
    t.add_argument("--notes")
    t.set_defaults(func=cmd_tyres)

    pr = sub.add_parser("price", help="record a fuel price you saw")
    pr.add_argument("--station", required=True)
    pr.add_argument("--price", type=float, required=True, help="cents/L or $/L")
    pr.add_argument("--date", default=today())
    pr.add_argument("--suburb")
    pr.add_argument("--brand")
    pr.add_argument("--fuel-type", dest="fuel_type", default="91")
    pr.add_argument("--source", help="observed, app, sign")
    pr.add_argument("--notes")
    pr.set_defaults(func=cmd_price)

    cy = sub.add_parser("cycle", help="price by day of week, trend, and by station")
    cy.add_argument("--fuel-type", dest="fuel_type", help="filter to one grade")
    cy.add_argument("--recent", type=int, default=30, help="readings in the trend window")
    cy.add_argument("--tank", type=float, default=40.0, help="litres per fill")
    cy.set_defaults(func=cmd_cycle)

    q = sub.add_parser("quote", help="record an insurance quote")
    q.add_argument("--brand", required=True)
    q.add_argument("--underwriter", help="who actually carries the risk")
    q.add_argument("--date", default=today())
    q.add_argument("--cover", help="comprehensive, third party property, etc.")
    q.add_argument("--value-basis", dest="value_basis", help="agreed or market")
    q.add_argument("--sum-insured", dest="sum_insured", type=float)
    q.add_argument("--annual", type=float, help="annual premium")
    q.add_argument("--monthly", type=float, help="monthly premium")
    q.add_argument("--excess", type=float, help="basic excess")
    q.add_argument("--extra-excess", dest="extra_excess", type=float,
                   help="age/inexperienced/unlisted driver excess that would apply")
    q.add_argument("--windscreen", help="windscreen excess or 'nil'")
    q.add_argument("--repairer", help="choice of repairer: yes/no/optional")
    q.add_argument("--hire-car", dest="hire_car")
    q.add_argument("--roadside")
    q.add_argument("--rating-one", dest="rating_one")
    q.add_argument("--notes")
    q.set_defaults(func=cmd_quote)

    cmp_ = sub.add_parser("compare", help="compare recorded insurance quotes")
    cmp_.set_defaults(func=cmd_compare)

    o = sub.add_parser("odo", help="record an odometer reading")
    o.add_argument("--date", default=today())
    o.add_argument("--odo", type=float, required=True)
    o.add_argument("--notes")
    o.set_defaults(func=cmd_odo)

    rep = sub.add_parser("report", help="full summary")
    rep.set_defaults(func=cmd_report)

    d = sub.add_parser("due", help="what is coming up")
    d.add_argument("--days", type=int, default=60)
    d.add_argument("--km", type=int, default=1500)
    d.set_defaults(func=cmd_due)

    l = sub.add_parser("log", help="print raw records")
    l.add_argument("module", choices=["fuel", "service", "cost", "reminders", "odo", "quotes", "prices", "tyres"])
    l.add_argument("--limit", type=int, default=20)
    l.set_defaults(func=cmd_log)

    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    sys.exit(args.func(args))
