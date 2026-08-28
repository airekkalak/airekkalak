# Everything Car

A plain-text record of everything about the car: what it is, what it drinks,
what's been done to it, what it costs, and what's coming up.

Records live in `data/*.csv` — readable, greppable, and diffable in git.
`car.py` is a small stdlib-only CLI that writes those records and reads them
back as a summary. Nothing to install.

## The four modules

| Module | Lives in | What it holds |
|---|---|---|
| Fuel & economy | `data/fuel.csv` | Fill-ups, odometer, litres, price, station |
| Service & maintenance | `data/service.csv` | Services, repairs, parts, workshop, next due |
| Costs & ownership | `data/costs.csv` | Rego, insurance, tyres, tolls, finance — anything else |
| Documents & details | `vehicle.md` | VIN, rego, engine, tyre sizes, fluid specs, policies |
| Reminders | `data/reminders.csv` | Anything due by date or by odometer |
| Odometer | `data/odometer.csv` | Standalone readings between fill-ups |
| Insurance quotes | `data/insurance_quotes.csv` | Quotes to compare — see `docs/insurance.md` |
| Fuel prices | `data/fuel_prices.csv` | Prices seen at the pump — see `docs/fuel.md` |
| Tyres | `data/tyres.csv` | Pressure and tread checks, rotations |

## Recording

```bash
# A fill-up. Date defaults to today. Give --cost or --price, it works out the other.
./car.py fuel --odo 84120 --litres 46.2 --cost 82.15 --station "BP" --fuel-type 95

# A splash that didn't fill the tank — flagged so economy maths stays honest.
./car.py fuel --odo 84500 --litres 20 --cost 36.40 --partial

# A service. Next-due details automatically become a reminder.
./car.py service --odo 84120 --type "Minor service" --workshop "Local mechanic" \
    --cost 340 --parts "oil, oil filter" --next-due-km 94120 --next-due-date 2027-08-24

# Any other cost.
./car.py cost --category rego --amount 890 --description "12 months"
./car.py cost --category insurance --amount 1240
./car.py cost --category tyres --amount 960 --odo 84200 --description "4x Michelin"

# A tyre check. The placard pressure comes from vehicle.md; out-of-spec
# corners are flagged. Pass --target to check against a different figure.
./car.py tyres --odo 190000 --fl 32 --fr 33 --rl 33 --rr 31 \
    --tread-fl 4.5 --spare 58

# Just an odometer reading, no spend attached.
./car.py odo --odo 190000

# A reminder, by date, by odometer, or both.
./car.py remind --item "Registration renewal" --due-date 2027-03-31 --recurrence yearly
```

## Reading back

```bash
./car.py report              # everything: economy, service history, cost split, what's due
./car.py due                 # due within 60 days or 1,500 km
./car.py due --days 180      # look further ahead
./car.py cycle               # price by day of week, cycle position, by station
./car.py compare             # rank insurance quotes by premium + excess
./car.py log fuel            # raw records for one module
```

## How the economy figure is worked out

Full-to-full: distance between two full tanks, divided into every litre put in
across that stretch — including partial fills in between. A tank is treated as
full unless you pass `--partial`. Two full fill-ups with odometer readings are
needed before a figure appears, and it gets more accurate with each one after.

Cost per km in the ownership section covers the whole recorded odometer span,
so it includes rego and insurance, not just fuel.

## Conventions

- Dates are `YYYY-MM-DD`. Distances are kilometres, volumes litres.
- Odometer readings are what makes the maths work — record one with every entry.
- Edit the CSVs by hand any time; the CLI only appends and re-sorts.
