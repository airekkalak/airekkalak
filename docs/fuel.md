# Buying fuel well — Brisbane

## Monday vs Thursday is probably the wrong question

The "petrol is cheap on Tuesday, dear on Thursday" rule comes from when
Australian capital cities ran a **weekly** price cycle. Brisbane hasn't for
years. Cycles here have stretched out to roughly a month: a sharp spike of
20–40c over a day or two, then a slow grind back down over several weeks.

**Caveat as at September 2026:** the regular Brisbane cycle appears to have
been disrupted for much of this year, with reports that cycles largely stopped
running from around February. Check a live cycle graph (PetrolSpy publishes one
for Brisbane) before assuming there is a trough to wait for. When cycles are
not running, "wait for the dip" simply means buying later at whatever the
market has done since — the station you choose matters, the day does not.

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

## The only honest leading indicator

Nobody can forecast retail petrol a week ahead. The closest legitimate signal
is the **Terminal Gate Price** — the daily wholesale price published by the oil
companies and the Australian Institute of Petroleum. Retail follows it with
roughly a one-to-two week lag, so a TGP climbing this week usually means retail
climbing next week. It tells you which way things are heading, not what any
particular station will charge.

Treat anything more specific than that as guesswork.

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

0. **Choosing the right station.** Where prices across a city span 40c or more
   between the cheapest and dearest sites, this is the biggest lever available
   and it works every single fill, regardless of what the market is doing.
1. **Buying at the bottom of the cycle** — 20c+/L, *when a cycle is running*.
2. **Timing within the week** — a few cents, and only worth acting on if it
   costs you nothing to shift the day.
3. **Supermarket dockets, 4c/L** — real, but small, and only if the docket
   station isn't already dearer than the independent down the road.
4. **Loyalty apps** — a cent or two, sometimes points.

A 4c docket at a station 5c dearer than the independent leaves you worse off.
Compare the price after the discount, not the discount.
