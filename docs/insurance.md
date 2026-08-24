# Comparing car insurance — 2019 Honda HR-V VTi, rego 197ZLG

Premiums are personalised, so no one can quote you without your details.
What this file does is make the comparison honest: what to hold constant,
what actually differs between insurers, and what to record.

Record each quote with `./car.py quote`, then run `./car.py compare`.

## Fix this before you get a single quote

The registration record shows **purpose of use: DEALER**. Two consequences:

1. Every quote form asks how the car is used. Answer it truthfully. If your
   answer ("private") disagrees with the registration record, an insurer can
   raise that at claim time — which is exactly when you can least afford it.
2. Quotes based on the wrong use class aren't comparable to ones you'd
   actually be able to claim on.

Sort the purpose of use with TMR first. Everything below assumes private use.

## Hold these constant across every quote

Change one of these and you are no longer comparing like with like:

- **Value basis and sum insured.** Agreed value fixes the payout now; market
  value is whatever the car is worth the day you write it off. On a 2019 with
  190,000 km these can differ meaningfully, and market value only ever falls.
- **Excess.** The single easiest way for a quote to look cheap. A $1,500
  excess against a $700 one is roughly $800 of hidden cost the moment you claim.
- **Listed drivers and their ages.** Adding a young driver moves the premium
  more than switching insurer usually does.
- **Annual, not monthly.** Monthly is a payment plan with a surcharge —
  typically several percent. `compare` shows what it costs you.
- **Kilometres per year and parking.** Estimate honestly; both are rated.

## Where insurers genuinely differ

| Item | Why it matters |
|---|---|
| Agreed vs market value | Agreed removes the argument at claim time |
| Choice of repairer | Without it, the insurer picks; parts and quality can follow |
| Rating 1 / no-claim protection | Whether one at-fault claim resets your discount |
| Windscreen excess | Chips are the most common claim; nil windscreen excess earns its keep |
| Hire car after an at-fault claim | Often only included in the pricier products |
| Total-loss payout terms | New-for-old age limits won't apply at this age |
| Excess structure | Age, inexperienced-driver and unlisted-driver excesses stack |
| Claims handling | The part that only matters once, and matters a lot |

## Getting a spread of real quotes

Many brands share an underwriter — same risk carrier, often the same claims
operation behind a different name and price. Worth knowing so that "five
quotes" isn't really two.

- **Suncorp**: AAMI, GIO, Bingle, Apia, Shannons, Vero
- **IAG**: NRMA, CGU, SGIO, SGIC, ROLLiN', Swann, WFI; IAG also took a 90%
  stake in **RACQ** insurance in 2024 — relevant in Queensland
- **Auto & General**: Budget Direct, and policies branded Qantas and Virgin Money
- **Hollard**: Real, Australian Seniors, Everyday Insurance and other partner brands
- **Allianz**, **QBE**, **Youi** underwrite in their own names

Coles-branded insurance is attributed to different groups by different
sources — ask who the underwriter is before treating it as a separate quote.

Aim for four to six quotes across *different* underwriters, all on the same
day (prices move), same excess, same value basis.

## Queensland CTP is a separate thing

CTP covers injury to people and is bundled into your registration, not your
comprehensive policy. Queensland regulates CTP premiums within a set band, so
the difference between CTP insurers is small — you can pick one at renewal, but
it isn't where savings are. Comprehensive is where the money is.

## Recording quotes

```bash
./car.py quote --brand "Budget Direct" --underwriter "Auto & General" \
    --value-basis agreed --sum-insured 19500 --annual 890 --monthly 82 \
    --excess 800 --repairer no --windscreen 0 --rating-one "add-on"

./car.py compare
```

`compare` ranks by the cost of a year in which you claim once — premium plus
excess — because that is the number that decides whether a cheap policy was
actually cheap. It also flags the monthly surcharge and any two brands you
quoted that share an underwriter.

## Before you sign

- Read the PDS section on total loss and on excesses — not the marketing page.
- Check whether the discount is first-year-only.
- Confirm what the agreed value will be at *renewal*, not just year one.
- Check the excess that applies to a windscreen-only claim.
