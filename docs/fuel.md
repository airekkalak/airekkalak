# Buying fuel well — Brisbane

## Monday vs Thursday is probably the wrong question

The "petrol is cheap on Tuesday, dear on Thursday" rule comes from when
Australian capital cities ran a **weekly** price cycle. Brisbane hasn't for
years. Cycles here have stretched out to roughly a month: a sharp spike of
20–40c over a day or two, then a slow grind back down over several weeks.

That means where you are **in the cycle** is worth far more than which day of
the week it is. Filling on the "right" weekday at the top of a cycle costs you
much more than filling on the "wrong" weekday at the bottom.

There is still a weekday effect — prices tend to firm up ahead of weekends —
but it is worth a few cents a litre, where cycle timing is worth twenty or
more. On a 40 L tank:

- Winning the weekday: roughly $1–2 a tank.
- Winning the cycle: roughly $8–12 a tank.

Track both, act on the second. `./car.py cycle` reports the weekday averages
*and* where the latest price sits in the recent range, so the cycle stays in
front of you.

## Verify it against your own data

Don't take the above on trust — the cycle changes. Log prices you drive past:

```bash
./car.py price --station "United Zillmere" --suburb Zillmere --price 172.7
./car.py price --station "Coles Express Aspley" --price 176.9 --date 2026-08-20
./car.py cycle --tank 40
```

Ten readings and the picture starts forming; a month and it's reliable. Log
the same stations on the same days where you can — otherwise a station that
looks cheap may simply have been priced on cheaper days.

The tool folds your actual fill-ups into the same analysis, so every
`./car.py fuel` entry counts as a data point too.

## Live prices without leaving the house

Queensland runs a mandatory price reporting scheme: stations must report price
changes within 30 minutes, and the data is published. Free apps read it:

- **RACQ Fair Fuel Prices**
- **PetrolSpy**, **Fuel Map Australia**, **FuelPrice Australia**
- **Google Maps** shows prices on station listings
- **7-Eleven fuel app** — lets you lock a price for a period, which pairs well
  with a long cycle: lock near the bottom, use it on the way back up

Check one before a long trip or a big fill. Two minutes is worth more than any
loyalty discount.

## Discounts, in order of what they're actually worth

1. **Buying at the bottom of the cycle** — 20c+/L.
2. **Choosing the right station** — independents and warehouse sites often run
   several cents under the majors. Your own log will show which.
3. **Supermarket dockets, 4c/L** — real, but small, and only if the docket
   station isn't already dearer than the independent down the road.
4. **Loyalty apps** — a cent or two, sometimes points.

A 4c docket at a station 5c dearer than the independent leaves you worse off.
Compare the price after the discount, not the discount.
